import logging
from abc import ABC
from glob import glob
from pathlib import Path
from types import MappingProxyType
from typing import Tuple

from aiomisc import threaded

from .base import CGroupTask, MetricProviderBase, PressureBase, gauge_factory

log = logging.getLogger()


def block_device_ids() -> Tuple[str, Path]:
    path: Path
    sys_dev_path = Path("/dev")
    base = Path("/sys/block")
    for path in map(Path, glob(str(base / "**/"))):
        dev_path = path / "dev"
        dm_path = path / "dm" / "name"

        if not dev_path.exists():
            continue

        with open(dev_path) as fp:
            dev_id = fp.read().strip()

        device_path = path.relative_to(base)
        if dm_path.exists():
            with open(dm_path) as fp:
                device_path = sys_dev_path / "mapper" / fp.read().strip()

        yield dev_id, device_path


DEVICE_IDS = {}


@threaded
def uptade_device_ids():
    global DEVICE_IDS
    DEVICE_IDS = MappingProxyType(dict(block_device_ids()))


def io_collector(task: CGroupTask):
    for collector in COLLECTORS:
        try:
            collector(task)()
        except Exception:
            log.exception("Failed to collect %r", collector)


class BlockIOBase(MetricProviderBase, ABC):
    FILENAME: str
    NAME: str
    DOCUMENTATION: str

    def __call__(self, *args, **kwargs):
        path = self.task.abspath / self.FILENAME

        if not path.exists():
            return

        with open(path, "r") as fp:
            for line in fp:
                devices = [key for key in line.split() if ":" in key]
                try:
                    rbytes, wbytes, rios, wios, dbytes, dios = line.split()[len(devices):]
                except ValueError:
                    log.warning("failed to parse %r", path)
                    return

                device = ",".join([str(DEVICE_IDS[device_id]) for device_id in devices])
                for metric in [rbytes, wbytes, rios, wios, dbytes, dios]:
                    metric_name, value = metric.split("=")

                    metric = gauge_factory(
                        self.NAME,
                        metric_name,
                        self.task.group,
                        self.DOCUMENTATION + " ({!r} field from {!r} file)".format(
                            metric_name, self.FILENAME,
                        ),
                        labelnames=("base_path", "path", "device"),
                    )

                    metric.labels(
                        base_path=self.base_path, path=self.path, device=device,
                    ).set(value)


class IOStat(BlockIOBase):
    FILENAME = "io.stat"
    NAME = "io"
    DOCUMENTATION = "IO Statistic"


class IOPressure(PressureBase):
    PRESSURE_FILE = "io.pressure"
    DOCUMENTATION = "IO resource pressure"


COLLECTORS = (
    IOStat,
    IOPressure,

)
