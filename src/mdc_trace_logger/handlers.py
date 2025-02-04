import logging
import ecs_logging
from typing import Any
from mdc_trace_logger.context import MDC

class MDCFilter(logging.Filter):
    """A logging filter that injects MDC data into log records."""
    def filter(self, record: logging.LogRecord) -> bool:
        MDC.ensure_mdc()
        mdc_data = MDC.get()
        for key, value in mdc_data.items():
            setattr(record, key, value)
        return True

class CustomECSFormatter(ecs_logging.StdlibFormatter):
    """A custom ECS logging formatter that includes MDC data in the log output."""
    def format_to_ecs(self, record: logging.LogRecord) -> dict[str, Any]:
        from mdc_logger.config import CONFIG

        result = super().format_to_ecs(record)
        MDC.ensure_mdc()
        result.update(MDC.get())

        if CONFIG.get("log_level_upper", True):
            result["log"]["level"] = record.levelname.upper() if record.levelname else None

        return result
