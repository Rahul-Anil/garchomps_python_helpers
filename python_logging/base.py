import log_template

logger = log_template.init_logger(
    "logging-config.yaml", log_template.DevStatus.DEVELOPMENT
)
