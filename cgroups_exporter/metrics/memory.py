import logging

from .base import CGroupTask, IntProviderBase, PressureBase, StatBase

log = logging.getLogger()


def memory_collector(task: CGroupTask):
    for collector in COLLECTORS:
        try:
            collector(task)()
        except Exception:
            log.exception("Failed to collect %r", collector)


class MemoryCurrentProvider(IntProviderBase):
    FILENAME = "memory.current"
    NAME = "current"
    METRIC = None
    DOCUMENTATION = "The total amount of memory currently"


class MemorySwapCurrentProvider(IntProviderBase):
    FILENAME = "memory.swap.current"
    NAME = "swap_current"
    METRIC = None
    DOCUMENTATION = "The total amount of swap currently"


class MemorySwapEventsProvider(StatBase):
    STAT_FILE = "memory.swap.events"
    DOCUMENTATION = "Memory swap events"


class MemoryEventsProvider(StatBase):
    STAT_FILE = "memory.events"
    DOCUMENTATION = "Memory events"


class MemoryStatProvider(StatBase):
    STAT_FILE = "memory.stat"
    DOCUMENTATION = "Memory statistic"


class MemoryPressure(PressureBase):
    PRESSURE_FILE = "memory.pressure"
    DOCUMENTATION = "Memory resource pressure"


COLLECTORS = (
    MemoryCurrentProvider,
    MemorySwapCurrentProvider,
    MemorySwapEventsProvider,
    MemoryEventsProvider,
    MemoryStatProvider,
    MemoryPressure,
)
