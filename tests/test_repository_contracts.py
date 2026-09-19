"""Keep published commands and the checked-in CLI snapshot trustworthy."""
import ast
from pathlib import Path
import os
import re
import shlex
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


def package_files(root):
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in root.rglob('*')
        if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'
    }


def skill_dirs():
    return sorted(p for p in (ROOT / 'skills').iterdir() if (p / 'SKILL.md').is_file())


def imported_names(tree):
    """Map every imported name to the line it was imported on."""
    names = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names[(alias.asname or alias.name).split('.')[0]] = node.lineno
        elif isinstance(node, ast.ImportFrom):
            if node.module == '__future__':
                continue
            for alias in node.names:
                if alias.name != '*':
                    names[alias.asname or alias.name] = node.lineno
    return names


def used_names(tree):
    used = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used.add(node.id)
        elif isinstance(node, ast.Attribute):
            base = node
            while isinstance(base, ast.Attribute):
                base = base.value
            if isinstance(base, ast.Name):
                used.add(base.id)
    return used


def skill_docs():
    for skill in skill_dirs():
        yield from skill.rglob('*.md')


class RepositoryContractsTest(unittest.TestCase):
    def test_vendored_package_matches_source(self):
        source = package_files(ROOT / 'cabbage_cli')
        vendored = package_files(ROOT / '.cabbage/tooling/cabbage_cli')
        differences = sorted(
            p for p in source.keys() | vendored.keys()
            if source.get(p) != vendored.get(p)
        )
        self.assertEqual([], differences, 'Run python scripts/sync-vendor.py')

    def test_skill_frontmatter_and_links_resolve(self):
        self.assertTrue(skill_dirs(), 'no skills found under skills/')
        for skill in skill_dirs():
            with self.subTest(skill=skill.name):
                text = (skill / 'SKILL.md').read_text()
                self.assertTrue(text.startswith('---\n'), 'missing YAML frontmatter')
                frontmatter = text.split('---')[1]
                self.assertIn(f'name: {skill.name}', frontmatter)
                description = re.search(r'(?m)^description: (.+)$', frontmatter)
                self.assertIsNotNone(description, 'missing description')
                self.assertGreater(len(description.group(1)), 80, 'description too vague to trigger on')
            for path in skill.rglob('*.md'):
                prose = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
                prose = re.sub(r'`[^`\n]*`', '', prose)
                for target in re.findall(r'\]\(([^)#\s]+\.md)(?:#[^)\s]*)?\)', prose):
                    with self.subTest(path=path.relative_to(ROOT), target=target):
                        self.assertTrue((path.parent / target).resolve().is_file(),
                                        f'broken relative link: {target}')

    def test_router_routes_to_every_sibling_skill(self):
        names = {skill.name for skill in skill_dirs()}
        router = ROOT / 'skills/cabbage/SKILL.md'
        self.assertTrue(router.is_file(), 'missing the cabbage entry-point skill')
        text = router.read_text()
        routing = text.split('## 2. 选路')[1].split('## 3.')[0]
        targets = set(re.findall(r'(?m)^\|[^|]+\|\s*`(cabbage(?:-[a-z]+)?)`\s*\|$', routing))
        self.assertEqual(names - {'cabbage'}, targets,
                         'routing table must name every sibling skill exactly once')

    def test_router_references_only_existing_skills(self):
        names = {skill.name for skill in skill_dirs()}
        referenced = set(re.findall(r'`(cabbage(?:-[a-z]+)?)`',
                                    (ROOT / 'skills/cabbage/SKILL.md').read_text()))
        referenced.discard('cabbage')
        self.assertEqual(set(), referenced - names,
                         'router points at skills that do not exist')

    def test_exit_codes_are_documented_in_one_place(self):
        # Duplicated exit-code lines drift apart; cli.md is the single source.
        owners = []
        for path in skill_docs():
            if re.search(r'(?m)^-\s*`(1|2|130)`\s*:', path.read_text()):
                owners.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(['skills/cabbage-change/references/cli.md'], owners,
                         'exit-code reference belongs in cli.md only')

    def test_governance_codeowners_block_has_one_copy(self):
        lists = [p for p in skill_docs()
                 if '/.cabbage/config.yaml' in p.read_text()]
        self.assertEqual(['skills/cabbage-adopt/references/enforcement.md'],
                         [p.relative_to(ROOT).as_posix() for p in lists],
                         'governance CODEOWNERS paths must live in one file')

    def test_release_plan_guidance_is_linked_from_change_skill(self):
        guide = ROOT / 'skills/cabbage-change/references/release-plan.md'
        self.assertTrue(guide.is_file(), 'missing release-plan writing guidance')
        skill = (ROOT / 'skills/cabbage-change/SKILL.md').read_text()
        self.assertIn('references/release-plan.md', skill,
                      'the deployment flag must point at the release-plan guidance')
        for heading in ('Preconditions', 'Deployment', 'Rollback', 'Verification'):
            with self.subTest(heading=heading):
                self.assertIn(heading, guide.read_text())

    def test_no_unused_imports_in_cli_package(self):
        for path in sorted((ROOT / 'cabbage_cli').glob('*.py')):
            tree = ast.parse(path.read_text())
            imported = imported_names(tree)
            used = used_names(tree)
            # A package's __init__ re-exports for consumers.
            if path.name == '__init__.py':
                continue
            unused = sorted(n for n in imported if n not in used)
            with self.subTest(path=path.name):
                self.assertEqual([], unused, f'unused imports in {path.name}')

    def test_directory_guide_matches_sync_mapping(self):
        """The directory guide lists sync targets; keep it equal to the code."""
        from cabbage_cli.core import DEFAULT_STAGE_DOCS_MAPPING
        guide = (ROOT / 'skills/cabbage-docs/references/directory-structure.md').read_text()
        section = guide.split('## `sync` 写入的目录')[1].split('## 门禁检查的目录')[0]
        # Build the documented stage -> directory map, handling the combined row.
        rows = re.findall(r'(?m)^\|\s*`([a-z]+)`(?:\s*/\s*`([a-z]+)`)?\s*\|\s*`docs/([^`]+)/`\s*\|', section)
        documented = {}
        for stage, second, directory in rows:
            documented[stage] = directory
            if second:
                documented[second] = directory
        for stage, target in DEFAULT_STAGE_DOCS_MAPPING.items():
            directory = target.rsplit('/{change_id}', 1)[0]
            with self.subTest(stage=stage):
                self.assertEqual(directory, documented.get(stage),
                                 f'guide disagrees with sync mapping for `{stage}`')

    def test_directory_guide_matches_ci_rules(self):
        from cabbage_cli.scaffold import IMPACT_FIELDS
        cfg = yaml.safe_load((ROOT / '.cabbage/config.yaml').read_text())
        rules = cfg['ci']['current_state_rules']
        guide = (ROOT / 'skills/cabbage-docs/references/directory-structure.md').read_text()
        section = guide.split('## 门禁检查的目录')[1]
        for area in IMPACT_FIELDS:
            if area not in rules:
                continue
            expected = rules[area]
            with self.subTest(area=area):
                # Every configured directory must be named in the guide's table.
                for directory in expected:
                    self.assertIn(directory, section,
                                  f'guide omits `{directory}` for impact `{area}`')

    def test_no_legacy_skill_entrypoint_remains(self):
        self.assertFalse((ROOT / 'SKILL.md').exists(), 'use skills/<name>/SKILL.md instead')
        self.assertFalse((ROOT / 'references').exists(), 'reference docs live inside each skill')

    def test_documented_verify_stages_exist(self):
        stages = {
            stage['id']
            for directory in ('cabbage_cli/assets/workflows', '.cabbage/workflows')
            for path in (ROOT / directory).glob('*.yaml')
            for stage in yaml.safe_load(path.read_text())['stages']
        }
        paths = [ROOT / 'README.md', *skill_docs()]
        paths += list((ROOT / 'docs').glob('*/README.md'))
        for path in paths:
            for stage in re.findall(r'(?m)^[ \t]*cabbage verify[ \t]+[^\s`]+[ \t]+([a-z][a-z-]*)', path.read_text()):
                with self.subTest(path=path.relative_to(ROOT), stage=stage):
                    self.assertIn(stage, stages)

    def test_readme_command_examples_execute(self):
        commands = re.findall(r'(?m)^cabbage ([^\n]+)', (ROOT / 'README.md').read_text())
        self.assertTrue(commands)
        with TemporaryDirectory() as td:
            root = Path(td)
            env = {**os.environ, 'PYTHONPATH': str(ROOT)}
            def git(*args):
                subprocess.run(['git', *args], cwd=root, check=True, capture_output=True)
            git('init', '-b', 'main')
            git('config', 'user.name', 'tester')
            git('config', 'user.email', 'tester@example.com')
            for command in commands:
                args = shlex.split(command)
                if args[0] == 'verify':
                    # Stand in for the documented human editing and implementation steps.
                    workspace = root / '.cabbage/changes' / args[1]
                    spec = yaml.safe_load((workspace / 'change.yaml').read_text())
                    workflow_path = root / '.cabbage/workflows' / f"{spec['type']}.yaml"
                    workflow = yaml.safe_load(workflow_path.read_text())
                    stage = next(s for s in workflow['stages'] if s['id'] == args[2])
                    artifact = workspace / stage['artifact']
                    text = re.sub(r'<!--\s*CABBAGE:.*?-->', 'Executed regression with passing result.', artifact.read_text(), flags=re.S)
                    artifact.write_text(text.replace('- [ ]', '- [x]'))
                    if args[2] == 'implementation':
                        (root / 'app.py').write_text('print("fixed")\n')
                if args[0] == 'ci':
                    git('add', '.')
                    git('commit', '-m', 'verified implementation')
                result = subprocess.run([sys.executable, '-m', 'cabbage_cli', *args], cwd=root, env=env, text=True, capture_output=True)
                self.assertEqual(0, result.returncode, command + '\n' + result.stdout + result.stderr)
                if args[0] == 'init':
                    git('add', '.')
                    git('commit', '-m', 'baseline')
                    git('update-ref', 'refs/remotes/origin/main', 'HEAD')


if __name__ == '__main__':
    unittest.main()
