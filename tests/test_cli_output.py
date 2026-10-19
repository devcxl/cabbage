from pathlib import Path
import json
import os
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CliOutputTest(unittest.TestCase):
    def _project(self, td):
        root = Path(td)
        env = {**os.environ, 'PYTHONPATH': str(ROOT)}
        subprocess.run([sys.executable, '-m', 'cabbage_cli', 'init', '--no-vendor-cli'],
                       cwd=root, env=env, check=True, capture_output=True, text=True)
        return root, env

    def _cli(self, root, env, *args):
        return subprocess.run([sys.executable, '-m', 'cabbage_cli', *args],
                              cwd=root, env=env, text=True, capture_output=True)

    def test_empty_project_status_reports_no_active_changes(self):
        with TemporaryDirectory() as td:
            root, env = self._project(td)
            result = self._cli(root, env, 'status')
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn('no active changes', result.stdout)

    def test_status_lists_change_as_text_without_json(self):
        with TemporaryDirectory() as td:
            root, env = self._project(td)
            self._cli(root, env, 'new', 'change', 'demo')
            result = self._cli(root, env, 'status')
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn('demo', result.stdout)
            self.assertNotIn('{', result.stdout)

    def test_status_json_stays_parseable(self):
        with TemporaryDirectory() as td:
            root, env = self._project(td)
            self._cli(root, env, 'new', 'change', 'demo')
            result = self._cli(root, env, 'status', '--json')
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual('demo', json.loads(result.stdout)[0]['change'])

    def test_next_prints_ready_section(self):
        with TemporaryDirectory() as td:
            root, env = self._project(td)
            self._cli(root, env, 'new', 'change', 'demo')
            result = self._cli(root, env, 'next', 'demo')
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn('ready:', result.stdout)

    def test_impact_prints_fields_and_generates_artifact(self):
        with TemporaryDirectory() as td:
            root, env = self._project(td)
            self._cli(root, env, 'new', 'change', 'demo')
            result = self._cli(root, env, 'impact', 'demo', '--set', 'api=true')
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn('api', result.stdout)
            self.assertIn('Yes', result.stdout)
            self.assertTrue((root / '.cabbage/changes/demo/api-design.md').exists())

    def _verify_single_record(self, root, env):
        tasks = root / '.cabbage/changes/demo/tasks.md'
        text = re.sub(r'<!--\s*CABBAGE:.*?-->', '', tasks.read_text(), flags=re.S)
        tasks.write_text(text.replace('- [ ]', '- [x]'))
        return self._cli(root, env, 'verify', 'demo', 'tasks')

    def test_status_flags_fully_verified_change_as_ready_to_archive(self):
        with TemporaryDirectory() as td:
            root, env = self._project(td)
            self._cli(root, env, 'new', 'change', 'demo')
            verify = self._verify_single_record(root, env)
            self.assertEqual(0, verify.returncode, verify.stderr)
            result = self._cli(root, env, 'status')
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn('ready to archive', result.stdout)
            data = json.loads(self._cli(root, env, 'status', '--json').stdout)
            self.assertTrue(data[0]['ready_to_archive'])

    def test_status_does_not_flag_unfinished_change(self):
        with TemporaryDirectory() as td:
            root, env = self._project(td)
            self._cli(root, env, 'new', 'change', 'demo')
            result = self._cli(root, env, 'status')
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertNotIn('ready to archive', result.stdout)
            data = json.loads(self._cli(root, env, 'status', '--json').stdout)
            self.assertFalse(data[0]['ready_to_archive'])

    def test_status_does_not_flag_stale_change(self):
        with TemporaryDirectory() as td:
            root, env = self._project(td)
            self._cli(root, env, 'new', 'change', 'demo')
            verify = self._verify_single_record(root, env)
            self.assertEqual(0, verify.returncode, verify.stderr)
            tasks = root / '.cabbage/changes/demo/tasks.md'
            tasks.write_text(tasks.read_text() + '\nChanged after verification.\n')
            result = self._cli(root, env, 'status')
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertNotIn('ready to archive', result.stdout)
            data = json.loads(self._cli(root, env, 'status', '--json').stdout)
            self.assertFalse(data[0]['ready_to_archive'])
            self.assertEqual(1, data[0]['stale'])


if __name__ == '__main__':
    unittest.main()
