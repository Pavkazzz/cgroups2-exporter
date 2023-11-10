import logging
import os

from aiomisc import entrypoint
from aiomisc.service import MemoryTracer, Profiler
from aiomisc.service.sdwatchdog import SDWatchdogService
from aiomisc_log import basic_config
from cgroups2_exporter.args import Parser
from cgroups2_exporter.services.collector import Collector
from cgroups2_exporter.services.metrics import MetricsAPI


def main():
    parser: Parser = Parser(
        auto_env_var_prefix="CGROUPS2_EXPORTER_",
        description="croups2 exporter",
        config_files=[
            os.getenv("CGROUPS2_EXPORTER_CONFIG", "cgroups2-exporter.conf"),
            "~/.cgroups2-exporter.conf",
            "/etc/cgroups2-exporter.conf",
        ],
    )

    arguments = parser.parse_args()

    log_config = dict(
        log_level=arguments.log.level,
        log_format=arguments.log.format,
    )

    basic_config(**log_config)

    services = [
        MetricsAPI(
            address=arguments.metrics.address,
            port=arguments.metrics.port,
            compression=not arguments.metrics.disable_compression,
        ),
        Collector(
            interval=arguments.collector.interval,
            delay=arguments.collector.delay,
            cgroup_paths=arguments.cgroups.path,
            cgroup_root=arguments.cgroups.root,
            max_workers=arguments.collector.workers,
        ),
        SDWatchdogService(),
    ]

    if arguments.profiler.enable:
        services.append(
            Profiler(
                interval=arguments.profiler.interval,
                top_results=arguments.profiler.top_results,
            ),
        )

    if arguments.memory_tracer.enable:
        services.append(
            MemoryTracer(
                interval=arguments.memory_tracer.interval,
                top_results=arguments.memory_tracer.top_results,
            ),
        )

    entrypoint_kw = dict(pool_size=arguments.pool_size)

    with entrypoint(*services, **log_config, **entrypoint_kw) as loop:
        logging.info("CGroups exporter has been started")
        if arguments.user is not None:
            logging.info("Changing user to %r", arguments.user.pw_name)
            os.setgid(arguments.user.pw_gid)
            os.setuid(arguments.user.pw_uid)
        loop.run_forever()


if __name__ == "__main__":
    main()
