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

The Zernike polynomials are a very popular basis to describe aberrations in the
wavefront of optical beams. They are used in ophthalmology {% cite Thibos2000
--file zernike %}, microscopy, and laser metrology, among others {% cite
Wyant1992 --file zernike %}. Because they are orthogonal on the unit disk, they are most
suitable to describe deviations from a flat phase front in a single transverse
plane of the beam.

They are given by

$$
\begin{align}
    Z_{n}^{m}(\rho,\phi) &=  R_{n}^{m}(\rho)\cos(m\phi)      & (m\geq0) \\
    Z_{n}^{m}(\rho,\phi) &=  R_{n}^{|m|}(\rho)\sin(|m|\phi)  & (m<0)
\end{align}
$$

where we can verify that they are indeed orthogonal on the unit disk:

$$
\int_0^1\int_0^{2\pi} Z_{n}^{m}Z_{n'}^{m'}\rho d\rho d\phi
    = \frac{(1+\delta_{m,0})\pi}{2n+2}\delta_{n,n'}\delta_{m,m'}.
$$

For a given value of $$n\in\{\{0\}\cup\mathbb{N}\}=\mathbb{N}_0$$, the possible
$$m$$ values are in the range $$m\in\{-n,n\}$$ and increase in increments of 2.
To simplify the enumeration of Zernike polynomials, various linear index schemes
have been devised. In short, each possible pair of $$(n,m)$$ is assigned to a
monotonically increasing index that we will denote $$j$$. In this post, we'll go
over some index schemes and write Python scripts that will allow us to map form
the linear index $$j$$ to the quantum pair $$(n,m)$$.

{:toc}

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

Since each row contains one element more than the previous row, the number of
elements contained in the first $$k$$ rows is given by the $$k$$th triangular
number $$T_k$$, defined by

$$
    T_k = \sum_{i=1}^{n} i = \frac{k(k+1)}{2}.
$$

For index systems that are monotonic in $$n$$, i.e. most of them,  we can
directly relate the quantum number $$n$$ to the index of the smallest triangular
number larger than $$j$$. Fortunately, the index can easily be determined via
the formula {% cite DAurizio2015 --file zernike %}

$$
k = \left\lceil \frac{1+\sqrt{1+8n}}{2} \right\rceil - 1.
$$

The remainder $$r=j-T_k+n$$ can then be used to determine what column corresponds
to that particular $$j$$ value. 


### Noll Indices

The rules to assign the Noll index is to have it monotonic in $$n$$ and then
assign in order of increasing $$|m|$$, where odd indices correspond to negative
values of $$m$$ and even indices to positive values of $$m$$. The correspondence
between the Noll indices and the quantum pairs is the subject of OEIS sequence
A176988 {% cite A176988 --file zernike %}.

Since the Noll indices start at 1, the first quantum number can be written
as one less than the triangular number index, $$n=k-1$$.

The $$m$$ value can be computed from the remainder $$r=j-T_k+n$$. The latter can
serve as an index into the list `m = [k  for k in range(-n,n+2,2)]`, as it
guaranteed to lie in the range $$[0,n-1]$$. Because of the rules governing the
assignment of signs, using the remainder directly as an index into this list is
rather tedious. A simpler way is to create a list that generates all the
possible values of $$|m|$$ and sort them in ascending order. For $$n=3$$, that
list would be `[1,1,3,3]`. $$r$$ can be used as an index in this list to
determine the value of $$|m|$$. The sign is then decided by the parity of $$j$$
directly, as stated by the Noll rules.

Here's the Python code that implements this (a C++ implementation is available
as part of my
[Zernike](https://github.com/joeydumont/zernike/blob/9eff81ebec7f0ef579ff01bfaabe23ff7ce8291c/src/zernike_indices.cpp#L41)
library)

```python
import numpy as np
def NollToQuantum(j):
    triangular_numbers_idx = np.array(np.ceil((1+np.sqrt(1+8*j))/2),dtype=int)-1
    triangular_numbers     = np.array(indices*(indices+1)/2).astype(int)
    n = indices - 1

    r     = j - triangular_numbers
    rpn   = r+n

    # -- Have to work value-per-value here.
    for i in range(n.size):
        m_vec = np.array([j for j in range(-n[i],n[i]+2,2)])
        m_vec = np.sort(np.abs(m_vec))
        m[i]  = (-1)**(j[i]%2)*m_vec[rpn[i]]

    return n, m
```
$$m$$ could be computed directly via the one-liner
```python
m = (-1)**j * ((n % 2) + 2 * np.array((r + ((n+1)%2))/2).astype(int))
```
but in practice I found the code above to be faster, even though
it generated a larger bytecode than the one-liner version.

Let's work through an example value.
For instance, suppose that we have $$j=8$$, then the formula above $$k=4$$ and thus $$n=3$$.
The remainder is $$r=8-10+3=1$$. From our list above, we have that $$|m|=1$$.
Since $$j$$ is even, $$m$$ is positive, and we have $$m=1$$.
And indeed, $$(j=8)\mapsto(3,1)$$.


### Phasics Indices

The Phasics index system is monotonic in $$n$$, as Noll's is, and also monotonic
in $$|m|$$. However, this system elects to always assign positive values of
$$m$$ to lower linear indices, regardless of parity, as stated in the SID4 6.4
User Handbook, Chapter 6.

From these characteristics, we see that Noll and Phasics only differ
on rows where $T_n$ is even. We can thus use the same basic function above,
but add the single-line
```python
m[i] *= (-1)**(triangular_numbers[i]%2+1)
```
at the end of the loop.


### Sources

{% bibliography --file zernike --cited_in_order %}


### Appendix: Table of index values generated by the algorithm

<style>
table {
    border-collapse: collapse;
    width: 100%;
}

th, td {
    text-align: left;
    padding: 8px;
}

tr:nth-child(even) {background-color: #f2f2f2;}

</style>

| $$j$$ &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| Noll | Phasics |
|-------------------------|
| $$1$$ | $$(0,0)$$ | $$(0,0)$$ |
| $$2$$ | $$(1,1)$$ | $$(1,1)$$ |
| $$3$$ | $$(1,-1)$$ | $$(1,-1)$$ |
| $$4$$ | $$(2,0)$$ | $$(2,0)$$ |
| $$5$$ | $$(2,-2)$$ | $$(2,2)$$ |
| $$6$$ | $$(2,2)$$ | $$(2,-2)$$ |
| $$7$$ | $$(3,-1)$$ | $$(3,1)$$ |
| $$8$$ | $$(3,1)$$ | $$(3,-1)$$ |
| $$9$$ | $$(3,-3)$$ | $$(3,3)$$ |
| $$10$$ | $$(3,3)$$ | $$(3,-3)$$ |
| $$11$$ | $$(4,0)$$ | $$(4,0)$$ |
| $$12$$ | $$(4,2)$$ | $$(4,2)$$ |
| $$13$$ | $$(4,-2)$$ | $$(4,-2)$$ |
| $$14$$ | $$(4,4)$$ | $$(4,4)$$ |
| $$15$$ | $$(4,-4)$$ | $$(4,-4)$$ |
| $$16$$ | $$(5,1)$$ | $$(5,1)$$ |
| $$17$$ | $$(5,-1)$$ | $$(5,-1)$$ |
| $$18$$ | $$(5,3)$$ | $$(5,3)$$ |
| $$19$$ | $$(5,-3)$$ | $$(5,-3)$$ |
| $$20$$ | $$(5,5)$$ | $$(5,5)$$ |
| $$21$$ | $$(5,-5)$$ | $$(5,-5)$$ |
| $$22$$ | $$(6,0)$$ | $$(6,0)$$ |
| $$23$$ | $$(6,-2)$$ | $$(6,2)$$ |
| $$24$$ | $$(6,2)$$ | $$(6,-2)$$ |
| $$25$$ | $$(6,-4)$$ | $$(6,4)$$ |
| $$26$$ | $$(6,4)$$ | $$(6,-4)$$ |
| $$27$$ | $$(6,-6)$$ | $$(6,6)$$ |
| $$28$$ | $$(6,6)$$ | $$(6,-6)$$ |
| $$29$$ | $$(7,-1)$$ | $$(7,1)$$ |
| $$30$$ | $$(7,1)$$ | $$(7,-1)$$ |
| $$31$$ | $$(7,-3)$$ | $$(7,3)$$ |
| $$32$$ | $$(7,3)$$ | $$(7,-3)$$ |
| $$33$$ | $$(7,-5)$$ | $$(7,5)$$ |
| $$34$$ | $$(7,5)$$ | $$(7,-5)$$ |
| $$35$$ | $$(7,-7)$$ | $$(7,7)$$ |
| $$36$$ | $$(7,7)$$ | $$(7,-7)$$ |
| $$37$$ | $$(8,0)$$ | $$(8,0)$$ |
| $$38$$ | $$(8,2)$$ | $$(8,2)$$ |
| $$39$$ | $$(8,-2)$$ | $$(8,-2)$$ |
| $$40$$ | $$(8,4)$$ | $$(8,4)$$ |
| $$41$$ | $$(8,-4)$$ | $$(8,-4)$$ |
| $$42$$ | $$(8,6)$$ | $$(8,6)$$ |
| $$43$$ | $$(8,-6)$$ | $$(8,-6)$$ |
| $$44$$ | $$(8,8)$$ | $$(8,8)$$ |
| $$45$$ | $$(8,-8)$$ | $$(8,-8)$$ |
| $$46$$ | $$(9,1)$$ | $$(9,1)$$ |
| $$47$$ | $$(9,-1)$$ | $$(9,-1)$$ |
| $$48$$ | $$(9,3)$$ | $$(9,3)$$ |
| $$49$$ | $$(9,-3)$$ | $$(9,-3)$$ |
| $$50$$ | $$(9,5)$$ | $$(9,5)$$ |
