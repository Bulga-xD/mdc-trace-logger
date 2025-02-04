import threading
from collections import defaultdict
from typing import Callable, Dict, List, Any

class MDC:
    """A thread-local implementation of the Mapped Diagnostic Context (MDC)."""
    _mdc = threading.local()
    _hooks: List[Callable[[Dict[str, Any]], None]] = []

    @classmethod
    def _init_context(cls) -> None:
        if not hasattr(cls._mdc, "contexts"):
            cls._mdc.contexts = defaultdict(dict)

    def __init__(self, **kwargs: Any) -> None:
        MDC._init_context()
        self.thread_id = threading.get_ident()
        MDC._mdc.contexts[self.thread_id].update(kwargs)
        MDC.set_global_context(MDC._mdc.contexts[self.thread_id])
        MDC._execute_hooks()

    def __enter__(self) -> "MDC":
        MDC.set_global_context(self._mdc.contexts[self.thread_id])
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        pass

    @classmethod
    def ensure_mdc(cls) -> None:
        if not cls.get():
            cls.set_global_context({})

    @classmethod
    def get(cls) -> Dict[str, Any]:
        cls._init_context()
        thread_id = threading.get_ident()
        return cls._mdc.contexts.get(thread_id, {}).copy()

    @classmethod
    def set_global_context(cls, data: Dict[str, Any]) -> None:
        cls._init_context()
        thread_id = threading.get_ident()
        cls._mdc.contexts[thread_id].update(data)
        MDC._execute_hooks()

    @classmethod
    def register_hook(cls, func: Callable[[Dict[str, Any]], None]) -> None:
        cls._hooks.append(func)

    @classmethod
    def _execute_hooks(cls) -> None:
        for hook in cls._hooks:
            hook(cls.get())
