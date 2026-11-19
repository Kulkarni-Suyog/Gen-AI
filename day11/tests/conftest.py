"""Shared test setup for the GSTSaral Day 11 checks."""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DAY9_DIR = PROJECT_ROOT / "day9"

if str(DAY9_DIR) not in sys.path:
    sys.path.insert(0, str(DAY9_DIR))
