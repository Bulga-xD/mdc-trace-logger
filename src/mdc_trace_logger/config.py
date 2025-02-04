import logging
import yaml
import os
from typing import Dict, Any
from mdc_trace_logger.utils import is_true

def load_config() -> Dict[str, Any]:
    """Loads logging configuration based on environment."""
    env = os.getenv("MDC_ENVIRONMENT", "default")
    config_filename = f"{env}.logger.config.yaml"
    config_path = os.getenv("MDC_LOGGER_CONFIG", config_filename)

    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return yaml.safe_load(f)

    return {
        "logger_name": os.getenv("MDC_LOGGER_NAME", "mdc_logger"),
        "log_level": os.getenv("MDC_LOG_LEVEL", "INFO"),
        "log_to_console": is_true(os.getenv("MDC_LOG_TO_CONSOLE", "true")),
        "log_to_file": is_true(os.getenv("MDC_LOG_TO_FILE", "false")),
        "log_file": os.getenv("MDC_LOG_FILE", "logs/app.log"),
        "use_ecs_format": is_true(os.getenv("MDC_USE_ECS", "true")),
        "log_level_upper": is_true(os.getenv("MDC_LOG_LEVEL_UPPER", "true")),
    }

CONFIG = load_config()

def get_logger(name: str = None) -> logging.Logger:
    """Returns a configured logger instance."""
    from mdc_logger.handlers import MDCFilter, CustomECSFormatter

    logger = logging.getLogger(name or CONFIG["logger_name"])
    logger.setLevel(CONFIG["log_level"])
    logger.propagate = False

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    formatter = CustomECSFormatter() if CONFIG["use_ecs_format"] else logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    if CONFIG["log_to_console"]:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if CONFIG["log_to_file"]:
        file_handler = logging.FileHandler(CONFIG["log_file"])
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.addFilter(MDCFilter())

    return logger
