import json

import pytest

from parsekeyval import BaseArguments, Field, parse_arguments


class ExampleArguments(BaseArguments):
    word: str = Field(default="hello", description="Word to print")
    number: int = Field(default=1, description="Number of times to print the word")
    uppercase: bool = Field(default=False, description="Whether to print the word in uppercase")


def test_parse_defaults():
    args = parse_arguments(ExampleArguments, [])

    assert args.word == "hello"
    assert args.number == 1
    assert args.uppercase is False


def test_parse_cli_arguments():
    args = parse_arguments(ExampleArguments, ["--word", "hi", "--number", "2", "--uppercase"])

    assert args.word == "hi"
    assert args.number == 2
    assert args.uppercase is True


def test_parse_json_config_file(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"word": "from-config", "number": 3}), encoding="utf-8")

    args = parse_arguments(ExampleArguments, ["--config", str(config_path)])

    assert args.word == "from-config"
    assert args.number == 3
    assert args.uppercase is False


def test_cli_arguments_override_config_file(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"word": "from-config", "number": 3}), encoding="utf-8")

    args = parse_arguments(ExampleArguments, ["--config", str(config_path), "--word", "from-cli"])

    assert args.word == "from-cli"
    assert args.number == 3


def test_missing_config_file_raises():
    with pytest.raises(FileNotFoundError):
        parse_arguments(ExampleArguments, ["--config", "missing.json"])
