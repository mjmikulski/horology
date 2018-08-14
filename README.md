# TTT
timing functions, contexts and for-loops

## This project is in concept stage, timing context is not yet implemented.


## Example: timing a function
```
from TTT import timed

@timed
def foo():
	pass
```


## Example: timing part of code with a context
```
from TTT import timing

with timing() as t:
	do_sth
```


## Example: timing an iterable
```
from TTT import Timed

for x in Timed(L):
	do_sth(x)
```
