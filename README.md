# Parsekeyval

Parsekeyval is yet another argument parser for command line utilities.
I wrote it because it fits my workflow very well, and I wanted to reuse it in multiple projects.

Arguments are defined via a Pydantic model, and are passed using a simple key-value syntax, like this:

```bash
my_program --arg1 value1 --arg2 value2
```

Parsekeyval automatically includes the possibility to pass a configuration file as input, containing all other arguments.
Currently the supported formats are JSON and TOML.

```bash
my_program --arg1 value1 --config path/to/config.json
```

## Usage

As you can see in [examples/example.py](examples/example.py), you can define your arguments by subclassing the `BaseArguments` class and defining your arguments as Pydantic fields.

```python
from parsekeyval import BaseArguments, Field, parse_arguments


class Arguments(BaseArguments):
    word: str = Field(default="hello", description="Word to print")
    number: int = Field(default=1, description="Number of times to print the word")
    uppercase: bool = Field(default=False, description="Whether to print the word in uppercase")


def main():
    args = parse_arguments(Arguments)
    ...
```

## Priority of arguments

If arguments are passed both via CLI and via a configuration file, the CLI arguments will take precedence over the configuration file.
If they are not passed either via CLI or configuration file, the default values defined in the code will be used.

| Passed via CLI | Present in passed config | Result                  |
|----------------|--------------------------|-------------------------|
| Yes            | Yes                      | As in CLI               |
| No             | Yes                      | As in config            |
| No             | No                       | Default defined in code |

For example, if you run the following command:

```bash
python examples/example.py --word "hi" --config examples/config.toml
```

the argument `word` will be set to `"hi"` (from CLI), while the argument `number` will be set to `2` (from config file), and the argument `uppercase` will be set to `False` (default value in the definition of the argument).
