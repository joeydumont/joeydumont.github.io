---
layout: post
title: Calling C libraries with C++ member functions
author: jayd
tags:
 - C
 - C++
 - member function pointers
---

I mostly code in C++, but often use C scientific libraries such as GSL, Cuba and
FFTW to compute something or other. Every time I do it, I feel like I have to
relearn how it works. I figured I'd write it down to save some time.

Example to work through: class that computes the value of pi with Cuba.
 - Explain how data is passed in C libraries (void pointer);
 - Unless it's static, the state needs to be passed to the member function
   pointer.
 - Explicit use of `this` in call to Cuba routines (could be better with
   serialziation, maybe?)

