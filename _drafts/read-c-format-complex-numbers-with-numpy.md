---
layout: post
title: Loading complex numbers from text files to numpy arrays
author: jayd
tags:
 - complex numbers
 - numpy
---

In my workflow, I typically use C++ for production code and Python for data
post-processing and data analysis. A major annoyance is that NumPy's
`genfromtxt` does not recognize the C++ complex number format.

Of course, one could write their own I/O for their C++ production codes, but
most libraries have built-in I/O functions and it's just a pain. It's much
easier to get Python to read the C++ format!

### The Issue

C++ represents a given complex number $$z=a+ib$$ as `(a,b)`. When using
`genfromtxt` to read a file containing an array of complex numbers, the obvious
```python
import numpy as np
x = np.genfromtxt("file", dtype=complex)
```
yields `NaN`s for the real part and `0`s for the imaginary part. To get Python
to understand the format, an easy solution is to first parse the elements of the
array as strings, then use a lambda function to effectively cast the string
as a complex number. Let's show the code and work from there.


### The Code

```python
def LoadComplexData(file,**genfromtext_args):
    """
    Load complex data in the C++ format in numpy.
    """
    array_as_strings = np.genfromtext(file,dtype=str,**genfromtext_args)
    complex_parser = np.vectorize(lambda x: complex(*eval(x)))
    return complex_parser(array_as_strings)
```

First, we load the array of complex numbers as an array of strings in Python.
Then, we use `np.vectorize` to define a callable that takes each of the
array and applies the `complex(*eval(x))` to it. `eval()` takes a string
and evaluates to a tuple. The `*` unpacks the tuple such that we are calling
`complex(a,b)`, which returns a complex number in Python format.
