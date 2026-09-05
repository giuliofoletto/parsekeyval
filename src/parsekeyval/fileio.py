import json
import tomllib
from pathlib import Path


def process_existing_file_name(file_name, folders=None, formats=None):
    folders = folders or []
    formats = formats or []
    base_candidates = [Path(file_name)]
    for folder in folders:
        base_candidates.append(Path(__file__).parent.parent.absolute() / folder / file_name)
    candidates = []
    for base in base_candidates:
        candidates.append(base)
        for format in formats:
            candidates.append(base.with_suffix(format))
    file_found = False
    for candidate in candidates:
        if candidate.exists():
            path = candidate
            file_found = True
            break
    if not file_found:
        raise FileNotFoundError("File not found")
    else:
        return path


def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def read_toml(file_path):
    with open(file_path, "rb") as f:
        data = tomllib.load(f)
    return data


def read_config_file(file_path):
    file_path = Path(file_path)

    if file_path.suffix.lower() == ".json":
        return read_json(file_path)
    if file_path.suffix.lower() == ".toml":
        return read_toml(file_path)

    raise ValueError(f"Unsupported config file format: {file_path.suffix}")
