"""Shared test helpers: frozen legacy workflow setup and artifact completion."""
import re
from pathlib import Path
import shutil

from cabbage_cli.scaffold import init_project


def init_legacy_project(root):
    init_project(root)
    shutil.copyfile(
        Path(__file__).parent / 'fixtures/legacy-feature.yaml',
        root / '.cabbage/workflows/feature.yaml',
    )


def fill_template(path):
    """Replace CABBAGE prompts with neutral content so a stage can be verified."""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"<!--\s*CABBAGE:.*?-->", "Completed content.", text, flags=re.S)
    path.write_text(text, encoding="utf-8")
