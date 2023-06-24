
def exception_decorator(step_name=None):
    """
    Decorator that wraps a function and handles exceptions raised during its execution.

    Args:
        `step_name (str, optional)`: Name of the step or function. If not provided, the decorator will try to use the function's qualified name. Defaults to None.

    Returns:
        `function`: Decorated function.

    Raises:
        Exception: If any exception occurs during the execution of the decorated function, it is caught, and a new exception is raised with an error message containing the step name and the original exception message.

    Example:
        ```
        @exception_decorator('Step 1')
        def divide(a, b):
            return a / b

        result = divide(10, 0)  # Raises an exception with the error message: '[Step 1] division by zero'
        ```
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                source = getattr(func, '__qualname__', None)
                if source is None:
                    source = f"{func.__module__}.{func.__name__}"
                step = step_name or source
                error_msg = f'[{step}] {str(e)}'
                raise Exception(error_msg)
        return wrapper
    return decorator


def step_logger_decorator(step_name=None):
    """
    Decorator that logs the start and end of a function or step.

    Args:
        `step_name (str, optional)`: Name of the step or function. If not provided, the decorator will try to use the function's qualified name. Defaults to None.

    Returns:
        `function`: Decorated function.

    Example:
        ```
        @step_logger_decorator('Step 1')
        def perform_task():
            print("Task execution")

        perform_task()
        # Output:
        # Start: [Step 1]
        # Task execution
        # End: [Step 1]
        ```
    """
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
