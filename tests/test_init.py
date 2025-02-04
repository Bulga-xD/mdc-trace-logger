from src.mdc_trace_logger import get_logger, MDC

def test_init_imports():
    """Ensure `get_logger` and `MDC` are correctly imported."""
    assert get_logger is not None
    assert MDC is not None
