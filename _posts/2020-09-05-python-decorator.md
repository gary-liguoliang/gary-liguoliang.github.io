---
layout: post
title:  "Python Decorator"
date:  20201126 23:30:00 +0800
categories: default
tags:
 - Python
---

## What is a Python Decorator? 

Less readable code: 

```
def foo(cls):
    pass
foo = synchronized(lock)(foo)
foo = classmethod(foo)
```

A much more readable version: 

```
@classmethod
@synchronized(lock)
def foo(cls):
    pass
```

https://www.python.org/dev/peps/pep-0318/

## What?! Decorator on a decorator

 
``` python
def cover_to_upper_case(f):
    """
    A simple decorator to covert return string upper case.
    """
    def uppercase(*args, **kwargs):
        print("upper stats....")
        r = f(*args, **kwargs)
        return r.upper()
    return uppercase


def add_prefix(f):
    """
    A simple decorator to add a prefix to return value
    """
    def pre(*args, **kwargs):
        r = f(*args, **kwargs)
        return f"[prefix] {r}"
    return pre


def add_prefix_and_covert_to_upper(f):
    """
    A combination of `cover_to_upper_case` and `add_prefix`
    """
    @cover_to_upper_case
    @add_prefix
    def covert(*args, **kwargs):
        r = f(*args, **kwargs)
        return r
    # also work: 
    # covert = add_prefix(covert)
    # covert = cover_to_upper_case(covert)
    return covert


# @add_prefix
# @cover_to_upper_case
@add_prefix_and_covert_to_upper
def hello():
    return "Python"


print(f"output: {hello()}")

```

In the above example: 
`@add_prefix` = `add_prefix(f)`, 
`@add_prefix_and_covert_to_upper` = `covert_to_upper_case(add_prefix(f))` 


in a debugger: `hello` is: 
```
<function cover_to_upper_case.<locals>.uppercase at 0x10e8da200>
```

`hello` can still be a `hello` if ` @wraps(f)` is added in the decorator, e.g.: 
```
def cover_to_upper_case(f):
     @wraps(f)
    def uppercase(*args, **kwargs):
        print("upper stats....")
        r = f(*args, **kwargs)
        return r.upper()
    return uppercase
```

Hello is `<function hello at 0x10a3bd200>` now!

`@wraps` is a decorator to: 
> Update a wrapper function to look like the wrapped function


## What about context manager as Decorator?

`contextlib.ContextDecorator`

> A base class that enables a context manager to also be used as a decorator.
>
> Context managers inheriting from ContextDecorator have to implement __enter__ and __exit__ as normal. __exit__ retains its optional exception handling even when used as a decorator.

How does it work?  

[contextlib.ContextDecorator](https://github.com/python/cpython/blob/a1652da2c89bb21f3fdc71780b63b1de2dff11f0/Lib/contextlib.py#L75): 

```
def __call__(self, func):
    @wraps(func)
    def inner(*args, **kwds):
        with self._recreate_cm():
            return func(*args, **kwds)
    return inner
```

so that a context manager can be used in both way: 
```python
>>> @mycontext()
... def function():
...     print('The bit in the middle')
...
>>> function()
Starting
The bit in the middle
Finishing

>>> with mycontext():
...     print('The bit in the middle')
...
```
