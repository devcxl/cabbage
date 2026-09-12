#!/usr/bin/env python3
"""Regenerate this repository's CLI snapshot without changing project workflows."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cabbage_cli.scaffold import sync_vendored_cli

if __name__ == '__main__':
    sync_vendored_cli(ROOT)
    print('Updated .cabbage/tooling/cabbage_cli from cabbage_cli/')
