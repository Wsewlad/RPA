
def exception_decorator(step_name=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                source = getattr(func, '__qualname__', None)
                if source is None:
                    source = f"{func.__module__}.{func.__name__}"
                step = step_name or source
                errorMsg = f'[{step}] {str(e)}'
                raise Exception(errorMsg)
        return wrapper
    return decorator


def step_logger_decorator(step_name=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            source = getattr(func, '__qualname__', None)
            if source is None:
                source = f"{func.__module__}.{func.__name__}"
            step = step_name or source
            print(f"Start: [{step}]")
            result = func(*args, **kwargs)
            print(f"End: [{step}]")
            return result
        return wrapper
    return decorator
