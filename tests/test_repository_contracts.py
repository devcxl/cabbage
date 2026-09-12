"""Keep published commands and the checked-in CLI snapshot trustworthy."""
from pathlib import Path
import re
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


def package_files(root):
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in root.rglob('*')
        if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'
    }


class RepositoryContractsTest(unittest.TestCase):
    def test_vendored_package_matches_source(self):
        source = package_files(ROOT / 'cabbage_cli')
        vendored = package_files(ROOT / '.cabbage/tooling/cabbage_cli')
        differences = sorted(
            p for p in source.keys() | vendored.keys()
            if source.get(p) != vendored.get(p)
        )
        self.assertEqual([], differences, 'Run python scripts/sync-vendor.py')

    def test_documented_verify_stages_exist(self):
        stages = {
            stage['id']
            for path in (ROOT / 'cabbage_cli/assets/workflows').glob('*.yaml')
            for stage in yaml.safe_load(path.read_text())['stages']
        }
        paths = [ROOT / 'README.md', ROOT / 'SKILL.md']
        paths += list((ROOT / 'references').glob('*.md'))
        for path in paths:
            for stage in re.findall(r'(?m)^[ \t]*cabbage verify[ \t]+[^\s`]+[ \t]+([a-z][a-z-]*)', path.read_text()):
                with self.subTest(path=path.relative_to(ROOT), stage=stage):
                    self.assertIn(stage, stages)


if __name__ == '__main__':
    unittest.main()
