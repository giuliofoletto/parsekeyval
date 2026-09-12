import json
from enum import Enum
from pathlib import Path
from typing import Literal

import pytest

from parsekeyval import BaseArguments, Field, parse_arguments
from parsekeyval.fileio import read_config_file


class ExampleArguments(BaseArguments):
    word: str = Field(default="hello", description="Word to print")
    number: int = Field(default=1, description="Number of times to print the word")
    uppercase: bool = Field(default=False, description="Whether to print the word in uppercase")


class OutputFormat(Enum):
    JSON = "json"
    TOML = "toml"


class RichArguments(BaseArguments):
    names: list[str] = Field(default_factory=list, description="Names to process")
    counts: list[int] = Field(default_factory=list, description="Counts to process")
    output_format: OutputFormat = Field(default=OutputFormat.JSON, description="Output format")
    mode: Literal["fast", "safe"] = Field(default="safe", description="Execution mode")
    output_path: Path | None = Field(default=None, description="Output path")


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


def test_parse_toml_config_file(tmp_path):
    config_path = tmp_path / "config.toml"
    config_path.write_text('word = "from-toml"\nnumber = 4\n', encoding="utf-8")

    args = parse_arguments(ExampleArguments, ["--config", str(config_path)])

    assert args.word == "from-toml"
    assert args.number == 4
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


def test_read_config_file_rejects_unsupported_suffix(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text("word: from-yaml\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported config file format"):
        read_config_file(config_path)


def test_parse_list_arguments():
    args = parse_arguments(
        RichArguments,
        ["--names", "alice", "bob", "--counts", "1", "2", "3"],
    )

    assert args.names == ["alice", "bob"]
    assert args.counts == [1, 2, 3]


def test_parse_enum_literal_and_path_arguments(tmp_path):
    output_path = tmp_path / "out.json"

    args = parse_arguments(
        RichArguments,
        [
            "--output-format",
            "toml",
            "--mode",
            "fast",
            "--output-path",
            str(output_path),
        ],
    )

    assert args.output_format is OutputFormat.TOML
    assert args.mode == "fast"
    assert args.output_path == output_path


def test_parse_invalid_literal_argument_exits():
    with pytest.raises(SystemExit):
        parse_arguments(RichArguments, ["--mode", "unsupported"])
