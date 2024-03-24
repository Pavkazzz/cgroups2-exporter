import logging
from contextlib import suppress

from .base import CGroupTask, MetricProviderBase, gauge_factory

log = logging.getLogger()


def cpuset_collector(task: CGroupTask):
    for collector in COLLECTORS:
        try:
            collector(task)()
        except Exception:
            log.exception("Failed to collect %r", collector)


class Range:
    __slots__ = "min", "max"

    def __init__(self, val: str):
        with suppress(Exception):
            self.min = self.max = int(val)
            return
        self.min, self.max = map(int, val.split("-"))

    def __len__(self):
        return self.max - self.min + 1


class CPUSetCount(MetricProviderBase):
    STAT_FILE = "cpuset.cpus"
    DOCUMENTATION = "CPU set for the cgroup"

    def __call__(self):
        stat = self.task.abspath / self.STAT_FILE
        if not stat.exists():
            return

        with open(stat, "r") as fp:
            result = [row for row in fp.read().strip().split(",")]

            metric = gauge_factory(
                "count",
                "cpu",
                self.task.group.replace(",", "_"),
                self.DOCUMENTATION,
                labelnames=("base_path", "path"),
            )

            metric.labels(base_path=self.base_path, path=self.path).set(
                sum([len(Range(row)) for row in result]),
            )


COLLECTORS = (CPUSetCount,)
