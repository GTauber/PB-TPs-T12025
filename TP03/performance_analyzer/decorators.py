from functools import wraps
from typing import Iterable


def measure_performance(operation_name: str = None):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if hasattr(self, 'analyzer'):
                start_time = self.analyzer.start_operation(operation_name or func.__name__)

                elements = 1
                if args:
                    first_arg = args[0]
                    if isinstance(first_arg, (list, tuple, set, dict)):
                        elements = len(first_arg)
                    elif isinstance(first_arg, Iterable) and not isinstance(first_arg, str):
                        elements = sum(1 for _ in first_arg)

                result = func(self, *args, **kwargs)
                self.analyzer.end_operation(
                    operation_name or func.__name__,
                    start_time,
                    elements
                )
                return result
            return func(self, *args, **kwargs)

        return wrapper

    return decorator