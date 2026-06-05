import json  # for reading JSON files
from pathlib import Path  # path utilities
from typing import Any  # generic typing


DATA_DIR = Path(__file__).resolve().parents[1] / "data"  # project-level data folder


def load_json(name: str, default: Any) -> Any:  # load a JSON file by name with a fallback
    path = DATA_DIR / name
    if not path.exists():
        return default  # return default if file missing
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)  # parse and return JSON
