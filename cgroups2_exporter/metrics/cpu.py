import logging

from .base import CGroupTask, IntProviderBase, PressureBase, StatBase

log = logging.getLogger()


def cpu_collector(task: CGroupTask):
    for collector in COLLECTORS:
        try:
            collector(task)()
        except Exception:
            log.exception("Failed to collect %r", collector)


class CPUStat(StatBase):
    STAT_FILE = "cpu.stat"
    DOCUMENTATION = "CPU statistic"


class CPUWeight(IntProviderBase):
    FILENAME = "cpu.weight"
    NAME = "weight"
    METRIC = None
    DOCUMENTATION = "Allowed CPU weight"


class CPUPressure(PressureBase):
    PRESSURE_FILE = "cpu.pressure"
    DOCUMENTATION = "CPU resource pressure"


COLLECTORS = (
    CPUStat,
    CPUWeight,
    CPUPressure,
)
