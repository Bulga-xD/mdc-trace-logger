from src.mdc_trace_logger.utils import is_true

def test_is_true():
    """Ensure `is_true` correctly converts strings to boolean."""
    assert is_true("true") is True
    assert is_true("1") is True
    assert is_true("yes") is True
    assert is_true("y") is True
    assert is_true("on") is True
    assert is_true("false") is False
    assert is_true("0") is False
    assert is_true("no") is False
    assert is_true("off") is False
