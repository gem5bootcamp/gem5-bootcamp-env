---
title: Modifying various CPU and cache parameters
author: Kaustav Goswami
slides_code:
livestream_code:
example_code: /materials/extra-topics/03-cpu-and-caches
---

# Modifying various CPU and cache parameters

In this module of extra topics, we cover how to quickly modify parameters of
the CPU and the cache. This is based on the `stdlib` runscripts. These scripts
are originally taken from the course ECS201A, taught in the Winter quarter of
2022 at UC Davis.

## Branch Predictor

The code for branch predictors are defined in `src/cpu/pred`. The SimObject
file is `BranchPredictor.py`. To add your new branch predictor, add the
corresponding _.hh_ and _.cc_ files in the same directory. The following code
snippet shows how to use these branch predictors:

```python
from m5.objects.BranchPredictor import *
...
from gem5.components.processors.simple_processor import SimpleProcessor

# Defining a sample Processor
class MyO3Processor(SimpleProcessor):
    ...
    # stdlib cores[N].core has a parameter branchPred
    self.cores[0].core.branchPred = BiModeBP()
```

## Cache Replacement Policy

The code for all the different cache replacement policies in gem5 is defined in
`src/mem/cache/replacement_policies` directory. The SimObject file is called
`ReplacementPolicies.py`, which can be found in the same directory. Similar to
_Branch Predictors_, a new replacement policies can be added by putting the
_.hh_ and _.cc_ files in the same directory. These can be easily swapped in any
stdlib script. The following script shows how to use `TreePLRURP` as the
replacement policy for a system:

```python
from m5.objects import TreePLRURP
...
# the stdlib l1d, l1i or l2 cache has a parameter called replacement_polcy
self.l2cache.replacement_policy = TreePLRURP()
...
```

## Prefecthers

Prefetchers are in the `src/mem/cache/prefetch` directory, with the SimObject
file as `Prefetch.py`. Adding a new prefetcher is similar to the ones above.
The following runscript shows how to use `TaggedPrefetcher` in your system:

```python
from m5.objects import TaggedPrefetcher
...
# Prefetcher can be directly passed while initializing any of the l1icache,
# l1dcache or l2cache from the stdlib
from gem5.components.cachehierarchies.classic.caches.l2cache import L2Cache

class MyL2Cache(L2Cache):
    super().__init__(size = "512KiB", PrefetcherCls = TaggedPrefetcher)
    ...
...
```
