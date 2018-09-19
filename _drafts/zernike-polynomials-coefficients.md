---
layout: post
title: Converting between different Zernike polynomial index systems
author: jayd
tags:
 - Zernike polynomials
 - indexing conventions
 - Noll
 - Phasics
---

The Zernike polynomials are a very popular basis to describe aberrations to the
wavefront of optical beams. They are used in ophthalmology, microscopy, and
laser metrology, among others. Because they are orthogonal on the unit disk,
they are most suitable to describe deviations from a flat phase front in a
single transverse plane of the beam's path.

They are given by

$$
\begin{align}
    Z_{n}^{m}(\rho,\phi) &=  R_{n}^{m}(\rho)\cos(m\phi)      & (m\geq0) \\
    Z_{n}^{m}(\rho,\phi) &= -R_{n}^{|m|}(\rho)\sin(|m|\phi)  & (m<0)
\end{align}
$$

where we can verify that they are indeed orthogonal on the unit disk:

$$
\int_0^1\int_0^{2\pi} Z_{n}^{m}Z_{n'}^{m'}\rho d\rho d\phi
    = \frac{(1+\delta_{m,0})\pi}{2n+2}\delta_{n,n'}\delta_{m,m'}.
$$

For a given value of $$n$$, the possible $$m$$ values are in the range
$$m\in\{-n,n\}$$ and increase in increments of 2. To simplify the description of
Zernike polynomials, various linear index schemes have been devised. In short,
each possible pair of $$(n,m)$$ is assigned to a monotonically increasing index
that we will denote $$j$$. In this post, we'll go over some index schemes and
write Python scripts that will allow us to map form the linear index $$j$$ to
the quantum pairs $$(n,m)$$.

### The Triangular Structure of the Quantum Pairs

By simply enumerating the quantum pairs and arranging them on a grid where
rows indicate the value of $$n$$ and columns the value of $$m$$, their triangular
structure becomes readily apparent.

$$
\begin{matrix}
             &            &            &  (0,0)   &           &           &            \\
             &            &   (1,-1)   &          &   (1,1)   &           &            \\
             &   (2,-2)   &            &  (2,0)   &           &   (2,2)   &            \\
   (3,-3)    &            &   (3,-1)   &          &   (3,1)   &           & (3,3)
\end{matrix}
$$

Since each row contains an element more than the previous row, the number of
elements contained in the first $$n$$ rows is given by the $$n$$th triangular
number $$T_n$$, defined by

$$
    T_n = \sum_{i=1}^{n} i = \frac{n(n+1)}{2}.
$$


{::comment}
|            |            |            | $$(0,0)$$ |           |           |            |
|            |            | $$(1,-1)$$ |           | $$(1,1)$$ |           |            |
|            | $$(2,-2)$$ |            | $$(2,0)$$ |           | $$(2,2)$$ |            |
| $$(3,-3)$$ |            | $$(3,-1)$$ |           | $$(3,1)$$ |           | $$(3,3)$$  |
{:/comment}

### Noll Indices

The rules to assign the Noll index is to have it monotonic in $$n$$ and then
assign in order of increasing $$|m|$$, where odd indices correspond to negative
values of $$m$$ and even indices to positive values of $$m$$.

To determine the value of $$n$$ from the linear index $$j$$, we need to
identity the smallest triangular number larger than $j$. Its index will
directly correspond to $$n$$. Fortunately, this can be easily determined
by the [formula](https://math.stackexchange.com/questions/1417579/largest-triangular-number-less-than-a-given-natural-number)

$$
k = \left\lceil \frac{1+\sqrt{1+8n}}{2} \right\rceil - 1.
$$


### Phasics Indices

The Phasics index system is monotonic in $$n$$, as Noll's is, and also monotonic
in $$|m|$$. However, this system elects to always assign positive values of
$$m$$ to lower linear indices, regardless of parity.

From these characteristics, we see that Noll and Phasics only differ
on rows where $T_n$ is even. 
### Sources

Largest triangular number: 

Noll indices: https://oeis.org/A176988

Phasics indices (idiots): Phasics manual.

Fringe/ZEMAX indices: https://www.sciencedirect.com/science/article/pii/S1567173915000942?via%3Dihub#bib7

Zernike polynomials in optics: http://wyant.optics.arizona.edu/zernikes/Zernikes.pdf