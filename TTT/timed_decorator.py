from functools import wraps
from time import perf_counter as counter, sleep

from TTT.tformatter import format


def timed(f=None, *, unit='s', print_fn=print, name=None):
    def decorator(_f):
        @wraps(_f)
        def wrapped(*args, **kwargs):
            start = counter()
            return_value = _f(*args, **kwargs)
            delta = counter() - start

            if print_fn is not None:
                nonlocal name
                if name is None:
                    name = _f.__name__ + ': '
                d, u = format(delta, unit=unit)
                print_str = f'{name}{d} {u}'
                print_fn(print_str)

            return return_value

        return wrapped

    if f is None:
        return decorator
    else:
        return decorator(f)


# Simple example

@timed
def foo():
    sleep(0.1)

foo()


# Still quite simple example

@timed(name='bar elapsed: ', unit='ms')
def bar():
    """Very important function"""
    sleep(0.2)

bar()

# bar is transparently wrapped
print(bar.__doc__)
print(bar.__name__)
