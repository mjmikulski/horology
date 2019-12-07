# Horology
conveniently measures time of your for-loops, contexts and functions.

Following 3 tools let you measure practically any part of your Python code.

## Usage



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
Just wrap your code using `with` statement
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
you can overwrite this by setting `unit` argument with one of those: 
`['ns', 'us', 'ms', 's', 'min', 'h', 'd']`.





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