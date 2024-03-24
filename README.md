CGroups exporter
================

Exporter for CGroups metrics, for LXD/Docker/systemd. 

Collects metrics for all cgroups based containers or SystemD services 
on the host machine, without the need to install separate exporters 
inside each container.

Installation
------------

```bash
pip install cgroups2-exporter
```

Example
-------

A simple example collects all available metrics for LXD containers.

```bash
cgroups2-exporter --cgroups-path "/sys/fs/cgroup/*/lxc.payload.*"
```

You can pass several path templates, then metrics will be collected from everyone.

In the example below, metrics will be collected for:
* All LXD containers
* All SystemD services running inside the LXD containers
* All Docker containers inside the LXD containers.
* All user slices (when used entering through the ssh the 
  SystemD creates the slice named by template `user-$UID`)

```bash
cgroups2-exporter --cgroups-path "/sys/fs/cgroup/lxc.payload.*/"
```

Usage
-----

Args that start with `--` (eg. -s) can also be set in a config file 
(`~/.cgroups2-exporter.conf` or `/etc/cgroups2-exporter.conf`). 

Config file syntax allows: `key=value`, `flag=true`, `stuff=[a,b,c]` 
(for details, see syntax [here](https://goo.gl/R74nmi)). 

If an arg is specified in more than one place, then commandline values 
override environment variables which override config file values 
which override defaults.

Environment variable `CGROUPS_EXPORTER_CONFIG` overwrites config file location.

```
usage: cgroups2-exporter [-h] [-s POOL_SIZE] [-u USER] [--log-level {critical,error,warning,info,debug,notset}] [--log-format {stream,color,json,syslog,plain,journald,rich,rich_tb}] [--metrics-address METRICS_ADDRESS]
                        [--metrics-port METRICS_PORT] [--metrics-disable-compression] --cgroups-path CGROUPS_PATH [CGROUPS_PATH ...] [--cgroups-root CGROUPS_ROOT] [--collector-interval COLLECTOR_INTERVAL]
                        [--collector-delay COLLECTOR_DELAY] [--collector-workers COLLECTOR_WORKERS] [--profiler-enable] [--profiler-top-results PROFILER_TOP_RESULTS] [--profiler-interval PROFILER_INTERVAL] [--memory-tracer-enable]
                        [--memory-tracer-top-results MEMORY_TRACER_TOP_RESULTS] [--memory-tracer-interval MEMORY_TRACER_INTERVAL]

croups exporter

options:
  -h, --help            show this help message and exit
  -s POOL_SIZE          Thread pool size (default: 4) [ENV: CGROUPS_EXPORTER_POOL_SIZE]
  -u USER               Change process UID [ENV: CGROUPS_EXPORTER_USER]

  --log-level {critical,error,warning,info,debug,notset}
                        (default: info) [ENV: CGROUPS_EXPORTER_LOG_LEVEL]
  --log-format {stream,color,json,syslog,plain,journald,rich,rich_tb}
                        (default: color) [ENV: CGROUPS_EXPORTER_LOG_FORMAT]

Metrics options:
  --metrics-address METRICS_ADDRESS
                        (default: ::) [ENV: CGROUPS_EXPORTER_METRICS_ADDRESS]
  --metrics-port METRICS_PORT
                        (default: 9753) [ENV: CGROUPS_EXPORTER_METRICS_PORT]
  --metrics-disable-compression
                        [ENV: CGROUPS_EXPORTER_METRICS_DISABLE_COMPRESSION]

CGroups options:
  --cgroups-path CGROUPS_PATH [CGROUPS_PATH ...]
                        [ENV: CGROUPS_EXPORTER_CGROUPS_PATH]
  --cgroups-root CGROUPS_ROOT
                        (default: /sys/fs/cgroup) [ENV: CGROUPS_EXPORTER_CGROUPS_ROOT]

Collector options:
  --collector-interval COLLECTOR_INTERVAL
                        (default: 15) [ENV: CGROUPS_EXPORTER_COLLECTOR_INTERVAL]
  --collector-delay COLLECTOR_DELAY
                        (default: 4) [ENV: CGROUPS_EXPORTER_COLLECTOR_DELAY]
  --collector-workers COLLECTOR_WORKERS
                        (default: 4) [ENV: CGROUPS_EXPORTER_COLLECTOR_WORKERS]

Profiler options:
  --profiler-enable     [ENV: CGROUPS_EXPORTER_PROFILER_ENABLE]
  --profiler-top-results PROFILER_TOP_RESULTS
                        (default: 20) [ENV: CGROUPS_EXPORTER_PROFILER_TOP_RESULTS]
  --profiler-interval PROFILER_INTERVAL
                        (default: 5) [ENV: CGROUPS_EXPORTER_PROFILER_INTERVAL]

Memory Tracer options:
  --memory-tracer-enable
                        [ENV: CGROUPS_EXPORTER_MEMORY_TRACER_ENABLE]
  --memory-tracer-top-results MEMORY_TRACER_TOP_RESULTS
                        (default: 20) [ENV: CGROUPS_EXPORTER_MEMORY_TRACER_TOP_RESULTS]
  --memory-tracer-interval MEMORY_TRACER_INTERVAL
                        (default: 5) [ENV: CGROUPS_EXPORTER_MEMORY_TRACER_INTERVAL]

Default values will based on following configuration files ['cgroups2-exporter.conf', '~/.cgroups2-exporter.conf', '/etc/cgroups-exporter.conf']. The configuration files is INI-formatted files where configuration groups is INI
sections.See more https://pypi.org/project/argclass/#configs
```

Container Usage
---------------

`cgroups2-exporter` is also available as a container image to be used in Docker, Kubernetes or other runtimes. It expects the host `/sys` directory to be mounted in the container (read only).

Docker usage example:

```shell
docker run -p 9753:9753 -v /sys/:/host_sys/ ghcr.io/mosquito/cgroups2-exporter:latest cgroups2-exporter --cgroups-path "/host_sys/fs/cgroup/*/docker/*"
```


Metrics
-------
TDB