import logging
from logging.handlers import RotatingFileHandler
import logging.config
import yaml
from pathlib import Path
import os

# TODO: use precommit hooks to convert double quotes to single quotes


def _init_logger(logging_config_path: str) -> any:
    logger_name = os.path.splitext(os.path.basename(__file__))[0]
    if not Path(logging_config_path).is_file():

        def _create_base_logger():
            logger = logging.getLogger(logger_name)  # create logger
            log_format = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            logger.setLevel(logging.WARNING)
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(log_format)
            stream_handler.setLevel(logging.WARNING)
            logger.addHandler(stream_handler)
            os.makedirs("logs", exist_ok=True)
            file_handler = RotatingFileHandler(
                filename=f"logs/{logger_name}.log",
                maxBytes=1024 * 10,
                backupCount=20,
                encoding="utf8",
                mode="a",
            )
            file_handler.setFormatter(log_format)
            file_handler.setLevel(logging.INFO)
            logger.addHandler(file_handler)
            return logger

        logger = _create_base_logger()
        logger.warning('Log config file could not be found')
        logger.info('Default logger has been invoked')
        return logger
    else:
        with open(logging_config_path, "rt") as f:
            logging_config = yaml.safe_load(f.read())
        log_file_output_path = logging_config['handlers']['file']['filename']
        os.makedirs(os.path.dirname(log_file_output_path), exists_ok=True)
        if logger_name not in logging_config['loggers']:
            logger = _create_base_logger()
            logger.WARNING(
                f'Log config file does not contain logger name: {logger_name} \
                    switching to using default logger'
            )
            logger.info('Default logger has been invoked')
            return logger

        logging.config.dictConfig(logging_config)
        logger = logging.getLogger(logger_name)
        logger.info(
            "Logging has been correctly setup using log config from yaml")
        return logger


if __name__ == "__main__":
    logger = _init_logger("logging-config.yaml")
    print("DONE")
