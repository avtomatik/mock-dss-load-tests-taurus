import asyncio
from functools import wraps
from typing import Any, Awaitable, Callable


def debug_print_out(
    coro: Callable[..., Awaitable[Any]]
) -> Callable[..., Awaitable[Any]]:
    """
    Decorator to print entry, exit, and optionally pause
    for debugging async coroutines.

    :param coro: The asynchronous coroutine function to be wrapped by the decorator.
    :type coro: Callable[..., Awaitable[Any]]
    :return: A wrapped coroutine function that includes debug prints.
    :rtype: Callable[..., Awaitable[Any]]
    """

    @wraps(coro)
    async def wrapper(*args, **kwargs):
        print(f"[DEBUG] Entering {coro.__name__}")
        await asyncio.sleep(1)
        result = await coro(*args, **kwargs)
        print(f"[DEBUG] Exiting {coro.__name__}")
        await asyncio.sleep(1)
        return result

    return wrapper
