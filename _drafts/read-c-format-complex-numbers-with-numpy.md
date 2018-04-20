---
layout: post
title: Loading complex numbers from text files to numpy arrays
author: jayd
tags:
 - complex numbers
 - numpy
---


http://numpy-discussion.10968.n7.nabble.com/genfromtxt-converter-question-td8121.html

```python
def LoadComplexData(file,**genfromtext_args):
    """
    Load complex data in the C format in numpy.
    """
    complex_parser = np.vectorize(lambda x: complex(*eval(x)))
    return complex_parser(np.genfromtxt(file, dtype=str,**genfromtext_args))
```