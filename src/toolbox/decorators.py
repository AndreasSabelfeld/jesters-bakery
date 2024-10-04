
def run_once(f):
    """
    Decorator that ensures a function runs only once.

    :params f: The function to be wrapped.
    :return: The wrapped function.
    """
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)

    wrapper.has_run = False
    return wrapper
