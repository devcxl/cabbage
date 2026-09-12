"""Keep published commands and the checked-in CLI snapshot trustworthy."""
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
