---
marp: true
paginate: true
theme: gem5
title: gem5's Standard Library
---

<!-- _class: title -->

## gem5's Standard Library

---

## What is the standard library for?

- When done without the library you must define *every part* of your simulation
- This allows for maximum flexibility, but it can mean creating 100s of lines of python to create the most basic simulation

---

## Where to find stuff: Importing in a script

```python
from gem5.components import *
```
