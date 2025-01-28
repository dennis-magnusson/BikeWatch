import logging
import time
from functools import wraps

import requests


def rate_limited_request(rate_limit_seconds):
    """
    A decorator to limit the rate of requests.

    Args:
        rate_limit_seconds (float): The minimum time (in seconds) between requests.
    """
    last_request_time = [0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            elapsed_time = current_time - last_request_time[0]

            if elapsed_time < rate_limit_seconds:
                time_to_sleep = rate_limit_seconds - elapsed_time
                logging.debug(
                    f"Rate limit reached. Sleeping for {time_to_sleep:.2f} seconds."
                )
                time.sleep(time_to_sleep)

            last_request_time[0] = time.time()
            return func(*args, **kwargs)

        return wrapper

    return decorator


@rate_limited_request(rate_limit_seconds=5)
def get_request(url, **kwargs):
    """Perform a GET request with rate limiting."""
    return requests.get(url, **kwargs)
