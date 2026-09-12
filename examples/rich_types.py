from enum import Enum
from pathlib import Path
from typing import Literal

from parsekeyval import Argument, Arguments


class OutputFormat(Enum):
    JSON = "json"
    TOML = "toml"


class Options(Arguments):
    names: list[str] = Argument(default_factory=list, description="Names to greet")
    repeat: list[int] = Argument(default_factory=lambda: [1], description="Repeat counts")
    output_format: OutputFormat = Argument(default=OutputFormat.JSON, description="Output format")
    mode: Literal["fast", "safe"] = Argument(default="safe", description="Execution mode")
    output_path: Path | None = Argument(default=None, description="Optional output path")


def main():
    options = Options.parse()
    print(options)

    print("\nParsed values:")
    print(f"names: {options.names}")
    print(f"repeat: {options.repeat}")
    print(f"output_format: {options.output_format}")
    print(f"mode: {options.mode}")
    print(f"output_path: {options.output_path}")


if __name__ == "__main__":
    main()

# Try it with:
# python examples/rich_types.py --names alice bob --repeat 1 2 3 \
#     --output-format toml --mode fast --output-path output.toml
