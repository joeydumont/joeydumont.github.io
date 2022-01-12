---
layout: post
title: "Building a multilib MIPS toolchain: my journey through gcc's build system"
author: jayd
tags:
 - gcc
 - multilib
 - multi ABI
 - mips64-elf
 - mips64
 - mips
 - toolchains
---

This article assumes that you know to compile a cross-compiler from scratch. If
not, I recommend this [succinct guide][1], or this [longer guide][2] if you want
to have some context.

On x86_64 architectures, building gcc such that it can generate both 32- and
64-bit code is easy: just use the `--enable-multilib` flag at configuration
time, and everything will follow smoothly (see Arch Linux's PKGBUILD for
[gcc][3], the packaging is a bit more complicated, but the build itself is
simple).

It is not as easy when targeting the MIPS architecture, specifically
`mips64-elf`. By default, the 32-bit ABIs are not part of the multilib setup.
gcc exposes the multilib setup that was used to compile a toolchain via the
`-print-multi-lib` option. On your own x86_64 system, you should see something
similar to this (assuming you have `gcc-multilib` on your system)

```bash
valandil ~ $ gcc -print-multi-lib
.;
32;@m32
```
where the second line shows the use of `-m32` in the build options for the gcc
toolchain itself, and the libraries are stored in the `32/` directory. This
toolchain is thus comprised of two sets of GCC libraries, one compiled with
default options, and one with `-m32`.

If you had installed a mips64-elf toolchain with `--enable-multilib`, by default
you would get the following output

```bash
valandil ~ $ mips64-elf-gcc -print-multi-lib
.;
soft-float;@msoft-float
el;@EL
soft-float/el;@msoft-float@EL
```

In order to enable other ABIs, specify other build options for the GCC libraries
in general, you need to know about *[Target makefile
fragments](https://gcc.gnu.org/onlinedocs//gcc-3.4.5/gccint/Target-Fragment.html)*.

In short, target Makefile fragments are the `gcc/config/<target>/t*` files in
gcc's source tree. When you specify a target at the `configure` step, it looks
for those in order to generate the Makefile that will actually build the gcc
libraries [^1]. For a `mips64-elf` target, the file that is of interest to us is
the `gcc/config/mips/t-elf` file. By default, it sets three Makefile variables

```make
MULTILIB_OPTIONS = msoft-float EL/EB
MULTILIB_DIRNAMES = soft-float el eb
MULTILIB_MATCHES = EL=mel EB=meb msingle-float=m4650
```

which instructs the gcc build system to generate libraries for combinations of
these three build flags. Flags that are separated by a space are combined, while
incompatible flag are separated with a slash. It is this fragment that generated
the `mips64-elf-gcc -print-multi-lib` output that we saw above.

So, if you want to generate libraries for other ABIs, you simply edit (or create
a new one!) that file to what you need. In my case, I wanted to have libraries
compiled with `-mabi=32`, at it is the ABI used by most N64 games. So, I edited
my `t-elf` fragment to be

```make
MULTILIB_OPTIONS = mabi=32 msoft-float EL/EB
MULTILIB_DIRNAMES = 32 soft-float el eb
MULTILIB_MATCHES = EL=mel EB=meb msingle-float=m4650
```

If you were to compile this toolchain, you would get the following
`-print-multib-lib` output:

```bash
.;
32;@mabi=32
soft-float;@msoft-float
el;@EL
soft-float/el;@msoft-float@EL
32/soft-float;@mabi=32@msoft-float
32/el;@mabi=32@EL
32/soft-float/el;@mabi=32@msoft-float@EL
```

`MULTILIB_DIRNAMES` controls the name of the folder in which the libraries
reside. Note that this corresponds to the information before the semi-colon in
the `-print-multilib-output`, while the string after describes the build
options, prepended with `@`. and `MULTILIB_MATCHES` provides the synonyms of
some build options.

There are other options than those discussed here. Feel free to read the
[Makefile
Fragment](https://gcc.gnu.org/onlinedocs//gcc-3.4.5/gccint/Fragments.html#Fragments)
of the gcc docs to have the whole story, or look at an example of custom target
in [glank][4]'s [n64 repo][5], under config (as of July 9th, this is only in the
n64-ultra branch).

[^1]: At least, that is how I think it works.
[1]: http://www.ifp.illinois.edu/~nakazato/tips/xgcc.html#binutil
[2]: https://preshing.com/20141119/how-to-build-a-gcc-cross-compiler
[3]: https://git.archlinux.org/svntogit/packages.git/tree/trunk/PKGBUILD?h=packages/gcc
[4]: https://github.com/glankk
[5]: https://github.com/glankk/n64/
