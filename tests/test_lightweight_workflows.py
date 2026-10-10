from pathlib import Path
import os
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from cabbage_cli.core import (
    CabbageError, ci_check, dump_yaml, gate, load_yaml, stage_statuses,
    validate_change, verify_stage,
)
from cabbage_cli.scaffold import ensure_artifacts, init_project, new_change, sync_vendored_cli

ROOT = Path(__file__).resolve().parents[1]


def complete(path):
    text = re.sub(r'<!--\s*CABBAGE:.*?-->', 'Verified behavior and regression evidence.', path.read_text(), flags=re.S)
    path.write_text(text.replace('- [ ]', '- [x]'))


class LightweightWorkflowTest(unittest.TestCase):
    def test_small_changes_need_one_record(self):
        for kind in ('change',):
            with self.subTest(kind=kind), TemporaryDirectory() as td:
                root = Path(td)
                init_project(root, vendor_cli=False)
                new_change(root, kind, 'small-change')
                workspace = root / '.cabbage/changes/small-change'
                self.assertEqual(['tasks.md'], sorted(p.name for p in workspace.glob('*.md')))
                self.assertEqual([], validate_change(root, 'small-change'))
                self.assertEqual([], gate(root, 'small-change', 'tasks'))
                self.assertTrue(gate(root, 'small-change', 'merge'))
                with self.assertRaisesRegex(CabbageError, 'placeholder'):
                    verify_stage(root, 'small-change', 'tasks')
                record = workspace / 'tasks.md'
                record.write_text(re.sub(r'<!--\s*CABBAGE:.*?-->', 'Real content.', record.read_text(), flags=re.S))
                with self.assertRaisesRegex(CabbageError, 'unchecked'):
                    verify_stage(root, 'small-change', 'tasks')
                complete(record)
                verify_stage(root, 'small-change', 'tasks')
                self.assertEqual([], gate(root, 'small-change', 'merge'))
                (workspace / 'tasks.md').write_text((workspace / 'tasks.md').read_text() + '\nChanged goal.\n')
                self.assertTrue(gate(root, 'small-change', 'merge'))

    def test_risks_add_only_the_relevant_document_and_gate(self):
        risks = {'design': ('design', 'tech-spec.md'), 'rfc': ('rfc', 'rfc.md'),
                 'architecture': ('adr', 'adr.md'), 'api': ('api', 'api-design.md'),
                 'database': ('database', 'database-design.md'),
                 'security': ('security', 'security-review.md'),
                 'deployment': ('release', 'release-plan.md')}
        for kind in ('change',):
            for risk, (stage, filename) in risks.items():
                with self.subTest(kind=kind, risk=risk), TemporaryDirectory() as td:
                    root = Path(td)
                    init_project(root, vendor_cli=False)
                    new_change(root, kind, 'risky-change')
                    workspace = root / '.cabbage/changes/risky-change'
                    spec_path = workspace / 'change.yaml'
                    spec = load_yaml(spec_path)
                    spec['impact'][risk] = True
                    dump_yaml(spec_path, spec)
                    ensure_artifacts(root, 'risky-change')
                    self.assertEqual(sorted(['tasks.md', filename]), sorted(p.name for p in workspace.glob('*.md')))
                    self.assertTrue(gate(root, 'risky-change', 'tasks'))
                    complete(workspace / 'tasks.md')
                    with self.assertRaisesRegex(CabbageError, 'dependency'):
                        verify_stage(root, 'risky-change', 'tasks')
                    complete(workspace / filename)
                    verify_stage(root, 'risky-change', stage)
                    self.assertEqual([], gate(root, 'risky-change', 'tasks'))
                    verify_stage(root, 'risky-change', 'tasks')
                    self.assertEqual([], gate(root, 'risky-change', 'merge'))
                    # Changing a reviewed risk document invalidates tasks too.
                    (workspace / filename).write_text((workspace / filename).read_text() + '\nChanged risk.\n')
                    statuses = {s['id']: s['status'] for s in stage_statuses(root, 'risky-change')}
                    self.assertEqual('stale', statuses['tasks'])
                    self.assertTrue(gate(root, 'risky-change', 'tasks'))

    def test_cli_lifecycle_and_ci_do_not_require_duplicate_small_change_docs(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            env = {**os.environ, 'PYTHONPATH': str(ROOT)}
            def cli(*args):
                result = subprocess.run([sys.executable, '-m', 'cabbage_cli', *args], cwd=root, env=env, text=True, capture_output=True)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                return result.stdout
            def git(*args):
                return subprocess.run(['git', *args], cwd=root, check=True, capture_output=True, text=True).stdout
            cli('init', '--no-vendor-cli')
            git('init', '-b', 'main')
            git('config', 'user.name', 'tester')
            git('config', 'user.email', 'tester@example.com')
            git('add', '.')
            git('commit', '-m', 'baseline')
            baseline = git('rev-parse', 'HEAD').strip()
            cli('new', 'change', 'small-change')
            cli('next', 'small-change')
            cli('gate', 'small-change', 'tasks')
            (root / 'app.py').write_text('print("hello")\n')
            complete(root / '.cabbage/changes/small-change/tasks.md')
            cli('verify', 'small-change', 'tasks')
            cli('tasks', 'small-change')
            cli('validate', 'small-change')
            cli('gate', 'small-change', 'merge')
            git('add', '.')
            git('commit', '-m', 'small change without duplicate docs')
            cli('ci', '--base', baseline)
            self.assertEqual([], ci_check(root, baseline))
            # High-risk changes still require the existing current-document rules.
            cli('impact', 'small-change', '--set', 'api=true')
            complete(root / '.cabbage/changes/small-change/api-design.md')
            cli('verify', 'small-change', 'api')
            cli('verify', 'small-change', 'tasks')
            git('add', '.')
            git('commit', '-m', 'API risk needs current docs')
            self.assertTrue(any('api=true' in e for e in ci_check(root, baseline)))
            cli('sync', 'small-change')
            git('add', '.')
            git('commit', '-m', 'publish API document')
            cli('ci', '--base', baseline)
            cli('archive', 'small-change')
            self.assertFalse((root / '.cabbage/changes/small-change').exists())
            self.assertEqual(1, len(list((root / '.cabbage/archive').glob('*/small-change/tasks.md'))))

    def test_combined_risks_block_until_all_are_verified(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            init_project(root, vendor_cli=False)
            new_change(root, 'change', 'combined-risk')
            workspace = root / '.cabbage/changes/combined-risk'
            spec = load_yaml(workspace / 'change.yaml')
            for risk in ('design', 'rfc', 'architecture', 'api', 'database', 'security', 'deployment'):
                spec['impact'][risk] = True
            dump_yaml(workspace / 'change.yaml', spec)
            ensure_artifacts(root, 'combined-risk')
            self.assertEqual(8, len(list(workspace.glob('*.md'))))
            stages = [s for s in stage_statuses(root, 'combined-risk') if s['id'] != 'tasks']
            for stage in stages:
                self.assertTrue(gate(root, 'combined-risk', 'tasks'))
                complete(workspace / stage['artifact'])
                verify_stage(root, 'combined-risk', stage['id'])
            self.assertEqual([], gate(root, 'combined-risk', 'tasks'))
            self.assertTrue(gate(root, 'combined-risk', 'merge'))

    def test_old_workflows_still_require_product_and_testing_docs(self):
        from support import init_legacy_project
        from unittest.mock import patch
        with TemporaryDirectory() as td:
            root = Path(td)
            init_legacy_project(root)
            new_change(root, 'feature', 'legacy-change')
            for stage in stage_statuses(root, 'legacy-change'):
                if stage['status'] == 'skipped':
                    continue
                complete(root / '.cabbage/changes/legacy-change' / stage['artifact'])
                verify_stage(root, 'legacy-change', stage['id'])
            with patch('cabbage_cli.core.git_changed_files', return_value=['app.py', '.cabbage/changes/legacy-change/tasks.md']):
                errors = ci_check(root, 'main')
            self.assertTrue(any('product=true' in e for e in errors))
            self.assertTrue(any('testing=true' in e for e in errors))

    def test_new_change_defaults_only_claim_impacts_the_workflow_can_back(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            init_project(root, vendor_cli=False)
            new_change(root, 'incident', 'incident-change')
            incident = load_yaml(root / '.cabbage/changes/incident-change/change.yaml')
            self.assertFalse(incident['impact']['testing'])
        with TemporaryDirectory() as td:
            root = Path(td)
            init_project(root, vendor_cli=False)
            new_change(root, 'change', 'ordinary-change')
            ordinary = load_yaml(root / '.cabbage/changes/ordinary-change/change.yaml')
            self.assertTrue(ordinary['impact']['testing'])
            self.assertTrue(ordinary['impact']['product'])
            self.assertFalse(ordinary['impact']['operations'])

    def test_unknown_change_type_lists_available_types(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            init_project(root, vendor_cli=False)
            with self.assertRaisesRegex(CabbageError, 'available: change, incident'):
                new_change(root, 'bugfix', 'old-name')

    def test_incident_and_change_defaults_do_not_block_ci(self):
        from unittest.mock import patch
        with TemporaryDirectory() as td:
            root = Path(td)
            init_project(root, vendor_cli=False)
            new_change(root, 'incident', 'outage')
            for stage in stage_statuses(root, 'outage'):
                complete(root / '.cabbage/changes/outage' / stage['artifact'])
                verify_stage(root, 'outage', stage['id'])
            with patch('cabbage_cli.core.git_changed_files', return_value=['app.py', '.cabbage/changes/outage/tasks.md']):
                errors = ci_check(root, 'main')
            self.assertFalse(any('testing=true' in e for e in errors), errors)
            self.assertFalse(any('operations=true' in e for e in errors), errors)
        with TemporaryDirectory() as td:
            root = Path(td)
            init_project(root, vendor_cli=False)
            new_change(root, 'change', 'ordinary')
            for stage in stage_statuses(root, 'ordinary'):
                if stage['status'] == 'skipped':
                    continue
                complete(root / '.cabbage/changes/ordinary' / stage['artifact'])
                verify_stage(root, 'ordinary', stage['id'])
            with patch('cabbage_cli.core.git_changed_files', return_value=['app.py', '.cabbage/changes/ordinary/tasks.md']):
                errors = ci_check(root, 'main')
            # record_covers 覆盖 product/testing：普通变更不要求重复产品和测试目录文档
            self.assertFalse(any('product=true' in e for e in errors), errors)
            self.assertFalse(any('testing=true' in e for e in errors), errors)
            self.assertFalse(any('operations=true' in e for e in errors), errors)

    def test_refresh_does_not_migrate_existing_workflows_or_state(self):
        from support import init_legacy_project
        with TemporaryDirectory() as td:
            root = Path(td)
            init_legacy_project(root)
            new_change(root, 'feature', 'legacy-change')
            complete(root / '.cabbage/changes/legacy-change/prd.md')
            verify_stage(root, 'legacy-change', 'requirement')
            paths = [root / '.cabbage/config.yaml', root / '.cabbage/workflows/feature.yaml',
                     root / '.cabbage/changes/legacy-change/state.json']
            before = [p.read_bytes() for p in paths]
            with self.assertRaises(CabbageError):
                init_project(root)
            sync_vendored_cli(root)
            self.assertEqual(before, [p.read_bytes() for p in paths])
            self.assertEqual('done', stage_statuses(root, 'legacy-change')[0]['status'])


if __name__ == '__main__':
    unittest.main()
