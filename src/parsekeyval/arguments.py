import argparse
from enum import Enum
from pathlib import Path
from types import UnionType
from typing import Literal, Union, get_args, get_origin

from pydantic import BaseModel, Field

from parsekeyval.fileio import process_existing_file_name, read_config_file


class BaseArguments(BaseModel):
    config: str | None = Field(default=None, description="File containing all arguments")


def _unwrap_optional(annotation):
    origin = get_origin(annotation)
    if origin in (Union, UnionType):
        non_none_args = [arg for arg in get_args(annotation) if arg is not type(None)]
        if len(non_none_args) == 1:
            return non_none_args[0]
    return annotation


def _literal_kwargs(annotation):
    choices = [choice for choice in get_args(annotation) if choice is not None]
    kwargs = {"choices": choices}
    if choices:
        kwargs["type"] = type(choices[0])
    return kwargs


def _enum_kwargs(annotation):
    values = [member.value for member in annotation]
    kwargs = {"choices": values}
    if values:
        kwargs["type"] = type(values[0])
    return kwargs


def _argparse_kwargs(annotation):
    annotation = _unwrap_optional(annotation)
    origin = get_origin(annotation)

    if origin is Literal:
        return _literal_kwargs(annotation)

    if isinstance(annotation, type) and issubclass(annotation, Enum):
        return _enum_kwargs(annotation)

    if origin in (list, set, tuple):
        item_args = get_args(annotation)
        item_annotation = item_args[0] if item_args else str
        item_kwargs = _argparse_kwargs(item_annotation)
        item_kwargs["nargs"] = "+"
        return item_kwargs

    if annotation is Path:
        return {"type": Path}

    if isinstance(annotation, type):
        return {"type": annotation}

    return {}


def add_model(parser, model):
    """
    Add Pydantic model to an ArgumentParser.
    Taken from
    https://stackoverflow.com/questions/72741663/argument-parser-from-a-pydantic-model.
    """
    fields = model.model_fields
    for name, field in fields.items():
        command_string = "--" + name.replace("_", "-")
        field_type = _unwrap_optional(field.annotation)
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
                default=argparse.SUPPRESS,
                help=field.description,
                **_argparse_kwargs(field.annotation),
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
