import logging
import time
from pathlib import Path

from .base import CGroupTask, MetricProviderBase, gauge_factory

log = logging.getLogger()


def uptime_collector(task: CGroupTask):
    for collector in COLLECTORS:
        try:
            collector(task)()
        except Exception:
            log.exception("Failed to collect %r", collector)


class Uptime(MetricProviderBase):
    DOCUMENTATION = "init.scope uptime"

    def __call__(self):
        fpath = self.task.abspath / "init.scope" / "cgroup.procs"

        if not fpath.exists():
            return

        with open(fpath, "r") as fp:
            pid = fp.readline().strip()
            if not pid:
                return

        stat = (Path("/proc/") / pid).stat()

        metric = gauge_factory(
            "uptime",
            None,
            self.task.group.replace(",", "_"),
            self.DOCUMENTATION,
            labelnames=("base_path", "path"),
        )
        metric.labels(base_path=self.base_path, path=self.path).set(
            time.time() - stat.st_ctime,
        )


COLLECTORS = (
    Uptime,
)
