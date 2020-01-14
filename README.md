# `Horology`

[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/mjmikulski/horology.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/mjmikulski/horology/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/mjmikulski/horology.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/mjmikulski/horology/alerts/)
[![Downloads](https://pepy.tech/badge/horology/month)](https://pepy.tech/project/horology/month)
[![PyPI version](https://badge.fury.io/py/horology.svg)](https://badge.fury.io/py/horology)

[![CircleCI](https://circleci.com/gh/mjmikulski/horology/tree/master.svg?style=svg)](https://circleci.com/gh/mjmikulski/horology/tree/master)

Conveniently measures the time of your loops, contexts and functions.

![](hourglass.jpg "Photo by Mike from Pexels")



## Instalation
Simply:
```
pip install horology
```



## Usage
The following 3 tools will let you measure practically any part of your Python code.

### Timing an iterable (list, tuple, generator, etc)
#### Quick example
```python
from horology import Timed
animals = ['cat', 'dog', 'crocodile']

for x in Timed(animals):
    feed(x)
```
Result:
```
iteration    1: 12.00 s
iteration    2: 8.00 s
iteration    3: 100.00 s

total 3 iterations in 120.00 s
min/median/max: 8.00/12.00/100.00 s
average (std): 40.00 (52.00) s

```

#### More cool stuff:
You can specify where (if at all) you want each iteration and summary to be printed, eg.:
```python
for x in Timed(animals, unit='ms', 
               iteration_print_fn=logger.debug, 
               summary_print_fn=logger.info):
    feed(x)
```


### Timing a function with a `@timed` decorator
#### Quick example
```python
from horology import timed

@timed
def foo():
    pass
```
Result:
```
>>> foo()
foo: 7.12 ms
```

#### More cool stuff:
Personalize time unit and name
```python
@timed(unit='s', name='Processing took ')
def bar():
    pass
```
Result:
```
>>> bar()
Processing took 0.18 s
```


### Timing part of code with a `Timing` context
#### Quick example
Just wrap your code using a `with` statement
```python
from horology import Timing

with Timing(name='Important calculations: '):
    pass
```
Result:
```
Important calculations: 12.43 s
```

#### More cool stuff:
You can suppress default printing and directly use measured time (also within context)
```python
with Timing(print_fn=None) as t:
    pass
    
make_use_of(t.interval)
```


## Time units
Time units are by default automatically adjusted, for example you will see
`foo: 7.12 ms` rather than `foo: 0.007 s`. If you don't like it, 
you can override this by setting the `unit` argument with one of these names: 
`['ns', 'us', 'ms', 's', 'min', 'h', 'd']`.


## Contributions 
Contributions are welcomed, see [contribution guide](.github/contributing.md).



## Internals:
Horology internally measures time with `perf_counter` which provides the *highest available resolution,*
 see [docs](https://docs.python.org/3/library/time.html#time.perf_counter).
