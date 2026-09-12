from enum import Enum
from pathlib import Path
from typing import Literal

from parsekeyval import BaseArguments, Field, parse_arguments


class OutputFormat(Enum):
    JSON = "json"
    TOML = "toml"


class Arguments(BaseArguments):
    names: list[str] = Field(default_factory=list, description="Names to greet")
    repeat: list[int] = Field(default_factory=lambda: [1], description="Repeat counts")
    output_format: OutputFormat = Field(default=OutputFormat.JSON, description="Output format")
    mode: Literal["fast", "safe"] = Field(default="safe", description="Execution mode")
    output_path: Path | None = Field(default=None, description="Optional output path")


def main():
    args = parse_arguments(Arguments)
    print(args)

    print("\nParsed values:")
    print(f"names: {args.names}")
    print(f"repeat: {args.repeat}")
    print(f"output_format: {args.output_format}")
    print(f"mode: {args.mode}")
    print(f"output_path: {args.output_path}")


if __name__ == "__main__":
    main()

# Try it with:
# python examples/rich_types.py --names alice bob --repeat 1 2 3 \
#     --output-format toml --mode fast --output-path output.toml
