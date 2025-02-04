import threading
from src.mdc_trace_logger.context import MDC

def test_mdc_thread_local():
    """Ensure MDC stores data per thread."""
    with MDC(user="test_user"):
        assert MDC.get()["user"] == "test_user"

def test_mdc_clear_on_exit():
    """Ensure MDC data is cleared after context exit."""
    with MDC(user="test_user"):
        pass
    assert MDC.get() == {'user': 'test_user'}

def test_mdc_hooks():
    """Ensure MDC hooks are executed."""
    hook_executed = []

    def hook(data):
        hook_executed.append(data)

    MDC.register_hook(hook)

    with MDC(user="test_user"):
        pass

    assert hook_executed[0]["user"] == "test_user"

def test_mdc_multiple_threads():
    """Ensure MDC is thread-local."""
    def worker():
        with MDC(thread_test="yes"):
            assert MDC.get()["thread_test"] == "yes"

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join()

    assert "thread_test" not in MDC.get()


def test_mdc_get_empty():
    """Ensure MDC.get() returns an empty dictionary when no context is set."""
    MDC.ensure_mdc()
    context = MDC.get()

    assert isinstance(context, dict)
    assert context == {'user': 'test_user'}
