from enum import Enum
import os
import logging
import logging.handlers

import yaml


class DevStatus(Enum):
    """Enum representing stages of development"""

    DEVELOPMENT = 0
    TESTING = 1
    PRODUCTION = 2


def _init_default_logger(logger_name: str) -> logging.Logger:
    """Initialize a logger with a default set of configurations

    Args:
        logger_name (str): Name of the logger to be created

    Return:
        Python Logger obj
    """
    logger = logging.getLogger(logger_name)
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_format)
    stream_handler.setLevel(logging.WARNING)
    logger.addHandler(stream_handler)
    os.makedirs("logs", exist_ok=True)
    file_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join("logs", f"{logger_name}.logs"),
        maxBytes=1024 * 10,
        backupCount=20,
        encoding="utf8",
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    return logger


def init_logger(
    logging_config_path: str, dev_status: DevStatus
) -> logging.Logger:
    """Initialize logger from yaml config file

    Args:
        logging_config_path (str): Path to logging config file
        dev_status (DevStatus): Represent current development Status of the Package

    Returns:
        Python Logger obj

    Raises:
        ValueError: logger name not present on config
    """
    package_name = os.path.basename(os.path.dirname(__file__))
    logger_name = f"{package_name}_{dev_status.name}"

    try:
        with open(logging_config_path, "rt") as f:
            logging_config = yaml.safe_load(f.read())
    except FileNotFoundError as error:
        logger = _init_default_logger(logger_name)
        logger.warning(
            "File %s could not be found (reason: %r), switching to default logger",
            logging_config_path,
            error,
        )
        logger.info("Default logger has been invoked")
        return logger

    log_file_output_path = logging_config["handlers"]["file"]["filename"]
    os.makedirs(os.path.dirname(log_file_output_path), exist_ok=True)

    try:
        if logger_name not in logging_config["loggers"]:
            raise ValueError(
                f"Logger name {logger_name} not present in logging config"
            )
    except ValueError as error:
        logger = _init_default_logger(logger_name)
        logger.warning(error)
        logger.info("Default logger has been invoked")
        return logger

    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(logger_name)
    logger.info(
        "Logging successfully setup using %s config", logging_config_path
    )
    return logger
