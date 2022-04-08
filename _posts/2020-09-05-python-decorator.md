---
layout: post
title:  "Python Decorator"
date:  20201126 23:30:00 +0800
categories: default
tags:
 - Python
---

## Python Decorators

In my first few weeks with Python, I was shocked that I cloud pass a function around as a parameter, for example:

```python
def foo():
    pass
synchronized_foo = synchronized(lock)(foo)
synchronized_foo()
```

and there's a better version with decorator:

```python
@synchronized(lock)
def foo():
    pass
```

Since I come from Java world, I immediately linked this with AOP in Java.  but decorator seems so light and easy to use.
as described in [PEP 318 – Decorators for Functions and Methods](https://www.python.org/dev/peps/pep-0318/)


## What?! Decorator on a decorator

```python
def covert_to_upper_case(f):
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
    A combination of `covert_to_upper_case` and `add_prefix`
    """
    @covert_to_upper_case
    @add_prefix
    def covert(*args, **kwargs):
        r = f(*args, **kwargs)
        return r
    # also work:
    # covert = add_prefix(covert)
    # covert = covert_to_upper_case(covert)
    return covert


# @add_prefix
# @covert_to_upper_case
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
<function covert_to_upper_case.<locals>.uppercase at 0x10e8da200>
```

`hello` can still be a `hello` if ` @wraps(f)` is added in the decorator, e.g.:
```python
def covert_to_upper_case(f):
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
> Context managers inheriting from ContextDecorator have to implement __enter__ and __exit__ as normal __exit__ retains its optional exception handling even when used as a decorator.

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

```
@mycontext()
def function():
    print('The bit in the middle')

# or:
with mycontext():
    print('The bit in the middle')
```


## What about adding more arguments?

example:

```python
def async_task(name: str):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            submit_task(target=f, args=args, kwargs=kwargs, name=name)
            print(f"{name} task submitted")
        return wrapper
    return decorator


@async_task("my_task")
def my_task():
    pass
```

## Summary

 - a decorator in Python is a function that takes a function as a parameter
 - add `@wraps()` to keep the function signature unchanged
