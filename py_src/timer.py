import functools
import time

def runTime(num_of_repeats: int = 1):
    def wrapper(func):
        @functools.wraps(func)
        def execute_with_time(*args, **kwargs):
            func_result = None
            start_time = time.perf_counter()
            for iteration in range(num_of_repeats):
                func_result = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_execution_time_in_milliseconds = (end_time - start_time) * 1000
            print(f"Avg time of execution {func.__name__} calculated on {num_of_repeats} iterations: {total_execution_time_in_milliseconds / num_of_repeats} millisec")
            return func_result
        return execute_with_time
    return wrapper