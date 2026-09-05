import argparse

from pydantic import BaseModel, Field

from parsekeyval.fileio import process_existing_file_name, read_config_file


class BaseArguments(BaseModel):
    config: str = Field(default=None, description="File containing all arguments")


def add_model(parser, model):
    """
    Add Pydantic model to an ArgumentParser.
    Taken from
    https://stackoverflow.com/questions/72741663/argument-parser-from-a-pydantic-model.
    """
    fields = model.model_fields
    for name, field in fields.items():
        command_string = "--" + name.replace("_", "-")
        # handle flags
        if field.annotation is bool:
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
                type=field.annotation,
                default=argparse.SUPPRESS,
                help=field.description,
            )


def parse_arguments(arguments_class):
    parser = argparse.ArgumentParser()
    add_model(parser, arguments_class)
    kwargs = parser.parse_args()

    # Create an object of user settings
    if hasattr(kwargs, "config"):
        path = process_existing_file_name(kwargs.config, folders=["data"], formats=[".json"])
        config = read_config_file(path)
    else:
        config = dict()

    # KW overwrites file
    config.update(kwargs.__dict__)

    # Validate user settings against the model
    args = arguments_class(**config)
    return args
