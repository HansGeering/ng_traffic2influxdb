FROM python:3-slim
ADD run.py /
ADD requirements.txt /

ENV HOST=10.0.0.1 USERNAME=admin PASSWORD=password INTERFACE=ppp0 \
    INFLUXDB_HOST=localhost INFLUXDB_PORT=8086 INFLUXDB_USER=admin \
    INFLUXDB_PASS=password INFLUXDB_DB=telegraf INFLUXDB_MY_NAME=orbi

RUN pip install -r /requirements.txt
CMD ["python", "/run.py"]

