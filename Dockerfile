FROM python:3-slim
ADD run.py /
ADD requirements.txt /

ENV ROUTER_HOST=10.0.0.1 ROUTER_USER=admin ROUTER_PASS=password ROUTER_IF=ppp0 \
    INFLUXDB_HOST=localhost INFLUXDB_PORT=8086 INFLUXDB_USER=admin \
    INFLUXDB_PASS=password INFLUXDB_DB=telegraf INFLUXDB_NAME=orbi

RUN pip install -r /requirements.txt
CMD ["python", "-u", "/run.py"]

