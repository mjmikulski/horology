# TTT
Measure time of your for-loops...

...and contexts and functions

Following 3 tools let you measure  practically any part of your Python code.

## Usage



### Timing an iterable (list, generator, etc)
#### Quick example
```python
from horology import Timed
L = ['cat', 'dog', 'crocodile']

for x in Timed(L):
    feed(x)
```
Result:
```
iteration    1: 12 s
iteration    2: 8 s
iteration    3: 289 s

min/median/max/average: 8/12/289/103
```

#### More cool stuff:
You can specify where (if at all) you want each iteration and summary to be printed, eg.:
```python
for x in Timed(L, unit='ms', 
               iteration_print_fn=logger.debug, 
               summary_print_fn=loger.info):
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
foo: 142 ms
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












### Timing part of code with a `timing` context
#### Quick example
Just wrap your code using `with` statement
```python
from horology import timing

with timing(name='Important calculations: '):
    pass
```
Result:
```
Important calculations: 12.132 s
```

#### More cool stuff:
You can suppress default printing and directly use measured time (also within context)
```python
with timing(print_fn=None) as t:
    pass
    
make_use_of(t.interval)
```








## Contributions 
1. Contributions are welcomed
2. Make sure that all tests pass (both unittests and doctests), you can run them all with:
```bash
nosetests -vv --with-doctest --doctest-options=+ELLIPSIS
```
3. If any questions, feel free to contact me.




## Internals:
TTT internally measures time with `perf_counter` which provides *highest available resolution,*
 see [docs](https://docs.python.org/3/library/time.html#time.perf_counter).