import random
import time
from typing import Callable, Iterable, Type, TypeVar

T = TypeVar("T")


def retry_call(
    fn: Callable[[], T],
    retries: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 10.0,
    jitter: float = 0.2,
    retry_exceptions: Iterable[Type[BaseException]] = (Exception,),
) -> T:
    attempt = 0
    while True:
        try:
            return fn()
        except retry_exceptions as exc:
            attempt += 1
            if attempt > retries:
                raise exc
            delay = min(max_delay, base_delay * (2 ** (attempt - 1)))
            jitter_amount = delay * jitter
            sleep_for = delay + random.uniform(-jitter_amount, jitter_amount)
            time.sleep(max(0.0, sleep_for))
