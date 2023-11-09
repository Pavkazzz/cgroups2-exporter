FROM python:3.10.12-slim-bullseye

COPY dist/*.whl /tmp/
RUN pip install /tmp/*.whl

CMD ["/usr/local/bin/cgroups2-exporter"]

EXPOSE 9753
