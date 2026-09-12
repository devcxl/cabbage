"""Frozen old-project workflow for compatibility regressions."""
from pathlib import Path
import shutil

from cabbage_cli.scaffold import init_project


def init_legacy_project(root):
    init_project(root)
    shutil.copyfile(
        Path(__file__).parent / 'fixtures/legacy-feature.yaml',
        root / '.cabbage/workflows/feature.yaml',
    )
