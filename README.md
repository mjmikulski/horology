# ttt
timing functions, contexts and for-loops

# This is in alpha stage, now just timing an iterable is implemented


## Example: timing a function
```
from ttt import timed

@timed
def foo():
	pass
```


## Example: timing part of code with a context
```
from ttt import timing

with timing() as t:
	do_sth
```


## Example: timing an iterable
```
from ttt import Timed

for x in Timed(L):
	do_sth(x)
```
