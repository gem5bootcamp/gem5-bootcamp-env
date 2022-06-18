from gem5.components.cachehierarchies.classic.abstract_classic_cache_hierarchy \
    import AbstractClassicCacheHierarchy
from gem5.components.boards.abstract_board import AbstractBoard

from m5.objects import Port

class UniqueCacheHierarchy(AbstractClassicCacheHierarchy):


    def __init__(self) -> None:
        AbstractClassicCacheHierarchy.__init__(self=self)

    def get_mem_side_port(self) -> Port:
        pass

    def get_cpu_side_port(self) -> Port:
        pass

    def incorporate_cache(self, board: AbstractBoard) -> None:
        pass
