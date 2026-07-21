import functools
import multiprocessing as mp
import multiprocessing.connection

import os
from typing import Any, Callable, Optional, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def _run_in_process(func: F, conn: mp.connection.Connection, args: tuple[Any, ...], kwargs: dict[str, Any]) -> None:
    try:
        result = func(*args, **kwargs)
    except BaseException as exc:
        try:
            conn.send(("EXCEPTION", exc))
        except Exception:
            conn.send(("EXCEPTION", RuntimeError("Failed to serialize exception from timed-out process")))
    else:
        conn.send(("RESULT", result))
    finally:
        conn.close()


def timeout_with_default(seconds: float, default: Optional[Any] = None, raise_on_timeout: bool = False) -> Callable[[F], F]:
    """Decorator that returns from a function after a given timeout.

    If the wrapped function does not complete within ``seconds``, the decorated
    call terminates the worker process and returns ``default``. If
    ``raise_on_timeout`` is True, a :class:`TimeoutError` is raised.

    Note:
        This implementation runs the wrapped function in a separate process
        and terminates it when the timeout is reached. That means the function
        must be picklable and its arguments must be serializable by multiprocessing.
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_method = "fork" if os.name != "nt" else "spawn"
            ctx = mp.get_context(start_method)
            parent_conn, child_conn = ctx.Pipe(duplex=False)
            process = ctx.Process(
                target=_run_in_process,
                args=(func, child_conn, args, kwargs),
                daemon=True,
            )
            process.start()
            child_conn.close()

            try:
                if parent_conn.poll(timeout=seconds):
                    kind, payload = parent_conn.recv()
                    process.join()
                    if kind == "RESULT":
                        return payload
                    raise payload
                if raise_on_timeout:
                    raise TimeoutError("Function timed out")
                return default
            finally:
                if process.is_alive():
                    process.terminate()
                    process.join(timeout=1)
                    if process.is_alive():
                        process.kill()

        return wrapper  # type: ignore[return-value]

    return decorator
