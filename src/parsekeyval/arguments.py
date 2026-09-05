import argparse
from types import UnionType
from typing import Union, get_args, get_origin

from pydantic import BaseModel, Field

from parsekeyval.fileio import process_existing_file_name, read_config_file


class BaseArguments(BaseModel):
    config: str | None = Field(default=None, description="File containing all arguments")


def _argparse_type(annotation):
    origin = get_origin(annotation)
    if origin in (Union, UnionType):
        non_none_args = [arg for arg in get_args(annotation) if arg is not type(None)]
        if len(non_none_args) == 1:
            return non_none_args[0]
    return annotation


def add_model(parser, model):
    """
    Add Pydantic model to an ArgumentParser.
    Taken from
    https://stackoverflow.com/questions/72741663/argument-parser-from-a-pydantic-model.
    """
    fields = model.model_fields
    for name, field in fields.items():
        command_string = "--" + name.replace("_", "-")
        field_type = _argparse_type(field.annotation)
        # handle flags
        if field_type is bool:
            if field.default:
                action = "store_false"
            else:
                action = "store_true"
            parser.add_argument(
                command_string,
                dest=name,
                default=argparse.SUPPRESS,
                action=action,
                help=field.description,
            )
        else:
            parser.add_argument(
                command_string,
                dest=name,
                type=field_type,
                default=argparse.SUPPRESS,
                help=field.description,
            )


def parse_arguments(arguments_class, argv=None):
    parser = argparse.ArgumentParser()
    add_model(parser, arguments_class)
    kwargs = parser.parse_args(argv)

    # Create an object of user settings
    if hasattr(kwargs, "config"):
        path = process_existing_file_name(kwargs.config, formats=[".json", ".toml"])
        config = read_config_file(path)
    else:
        config = dict()

    # KW overwrites file
    config.update(kwargs.__dict__)

    # Validate user settings against the model
    args = arguments_class(**config)
    return args
