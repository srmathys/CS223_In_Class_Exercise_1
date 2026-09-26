# MODULE NAME:  util_funs.py

# IMPORTS
from functools import wraps
import time
import timeit

from numba.cuda.cudadecl import func


""" This section contains two different versions/ways to measure the
    execution time of functions or code snippits.    
    
    1. CUSTOM DECODER
    The most flexible and industry-standard way to time a Python function 
    is by using a decorator with time.perf_counter(). This method provides 
    the highest precision for measuring execution time and allows you to 
    reuse the timing logic across multiple functions without modifying their 
    core code. This approach measures the CPU usage time of the function. 
    See https://www.youtube.com/watch?v=FblABqaKz_U), or 
     (https://www.youtube.com/shorts/TfccynZoF-c), or
    (https://stackoverflow.com/questions/14452145/how-to-measure-time-taken-between-lines-of-code-in-python)
    
    2. BUILT-IN timeit MODULE 
    If you need to benchmark a small code block or a quick function snippet 
    repeatedly to account for system fluctuations, the built-in timeit module 
    is ideal. This measures the wallclock execution time of a function, which 
    may not be exactly the same as the CPU execution time.
    See (https://docs.python.org/3/library/timeit.html), or 
        (https://pymotw.com/3/timeit/)
"""

# CUSTOM DECODER: timer_decorator
# def timer_decorator(func):
#     """A decorator that prints the execution time of a function."""
#
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         # Start the high-precision performance counter
#         if not hasattr(wrapper, 'depth'):
#             wrapper.depth = 0
#         if wrapper.depth == 0:
#             start_time = time.perf_counter()
#         try:
#             # Execute the actual function
#             return func(*args, **kwargs)
#         finally:
#             wrapper.depth -=1
#             if wrapper.depth == 0:
#         # Calculate elapsed time
#                 end_time = time.perf_counter()
#                 execution_time = end_time - start_time
#                 print(f"Function '{func.__name__}' executed in {execution_time:.6f} seconds.")
#
#                 if func.__name__ not in execution_log:
#                     execution_log[func.__name__] = []
#                 execution_log[func.__name__].append(execution_time)
#
#     return wrapper


class timer_decorator:
    def __init__(self, func):
        self.func = func
        self._active = False
        wraps(func)(self)  # Preserves function metadata

    def __call__(self, *args, **kwargs):
        # If already inside a recursive chain, just execute the function
        if self._active:
            return self.func(*args, **kwargs)

        # Outer call: start timing
        self._active = True
        start_time = time.perf_counter()
        try:
            return self.func(*args, **kwargs)
        finally:
            # End timing and reset state
            end_time = time.perf_counter()
            self._active = False
            execution_time = end_time - start_time
            print(f"{self.func.__name__} total execution time: {execution_time:.6f} seconds")
            return execution_time #understand dangerous, but unsure how to otherwise pull it
###
# Make sure this module is imported
if __name__ == '__main__':
    print("The module named util_funs.py is intended to be imported and not executed.")
