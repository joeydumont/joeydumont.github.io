---
layout: post
title: Mixing C and Assembly
author: jayd
tags:
  - gcc
  - assembly
  - c structs in assembly
  - gas
  - linking
---

Describe mixing C and asm in general terms:
  - inline asm (regular vs extended) and its limitations
  - using gas as the assembler
  - making sure that the linker does not throw away the sections (useful in embedded systems and, hum, the N64)
  - mention using platform specific linkers (harder to interface with gcc, but simpler to use)
