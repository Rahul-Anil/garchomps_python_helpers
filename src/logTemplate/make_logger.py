# -*- coding: utf-8 -*-
"""Package to create a logger

Will create a python logger using the default logging API from a yaml config 
file

"""

import os
import logging
import logging.handlers
import logging.config
from pathlib import Path

import yaml

# TODO: add tests for the logger
# TODO: add tox for the project


def init_logger(logging_config_path: str, logger_name: str) -> logging.Logger:
    """Initialize logger from yaml config file

    Args:
        logging_config_path (str): Path to logging config file
        logger_name: Name of the logger to use from the config file

    Returns:
        Python Logger obj

    Raises:
        FileNotFoundError: logging config file not found
        ValueError: logger name not present on config
    """
    if not os.path.isfile(logging_config_path):
        raise FileNotFoundError(
            f"Logging config file `{logging_config_path}` not found"
        )

    # Read the logging config file
    with open(logging_config_path, "rt", encoding="utf-8") as f:
        logging_config = yaml.safe_load(f.read())
    f.close()

    log_output_path = logging_config["handlers"]["file"]["filename"]
    log_output_parent_dir = Path(log_output_path).parent.absolute()
    os.makedirs(os.path.dirname(log_output_parent_dir), exist_ok=True)

    if logger_name not in logging_config["loggers"]:
        raise ValueError(
            f"Logger `{logger_name}` not present in logging config"
        )

    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(logger_name)
    logger.info(
        "Logging successfully setup using %s config", logging_config_path
    )
    return logger
