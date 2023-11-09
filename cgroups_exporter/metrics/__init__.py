import logging
from types import MappingProxyType

from aiomisc import threaded

from .base import CGroupTask
from .cpu import cpu_collector
from .cpuset import cpuset_collector
from .io import io_collector
from .memory import memory_collector
from .pids import pids_collector
from .uptime import uptime_collector

log = logging.getLogger(__name__)

HANDLER_REGISTRY = MappingProxyType(
    {
        "memory": memory_collector,
        "io": io_collector,
        "cpu": cpu_collector,
        "uptime": uptime_collector,
        "cpuset": cpuset_collector,
        "pids": pids_collector,
    },
)


@threaded
def metrics_handler(task: CGroupTask):
    def log_unhandled(task):
        log.debug("Unhandled metric group %r", task.group)

    HANDLER_REGISTRY.get(task.group, log_unhandled)(task)
