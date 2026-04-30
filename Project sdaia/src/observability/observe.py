import time
from functools import wraps

def observe(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.time()

        result = fn(*args, **kwargs)

        end = time.time()

        print(f"[TRACE] {fn.__name__} took {end - start:.2f}s")

        return result

    return wrapper