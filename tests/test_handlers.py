import logging

from src.mdc_trace_logger.context import MDC
from src.mdc_trace_logger.handlers import CustomECSFormatter


def test_ecs_formatter_with_log_level_upper():
    """Ensure ECS formatter respects log_level_upper config."""
    formatter = CustomECSFormatter()
    record = logging.LogRecord("test_logger", logging.WARNING, "", 0, "Test warning", None, None)

    MDC.ensure_mdc()
    MDC.set_global_context({"trace_id": "trace-5678"})

    ecs_log = formatter.format_to_ecs(record)

    assert "log" in ecs_log
    assert "level" in ecs_log["log"]
    assert ecs_log["log"]["level"] == "WARNING"


def test_ecs_formatter_without_mdc():
    """Ensure ECS formatter works when no MDC data is set."""
    formatter = CustomECSFormatter()
    record = logging.LogRecord("test_logger", logging.DEBUG, "", 0, "Debug message", None, None)

    ecs_log = formatter.format_to_ecs(record)

    assert "message" in ecs_log
    assert ecs_log["message"] == "Debug message"
