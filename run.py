import requests, re, telnetlib
import datetime, time, os
from influxdb import InfluxDBClient
from requests.auth import HTTPBasicAuth

HOST = os.environ['ROUTER_HOST']
USERNAME = os.environ['ROUTER_USER']
PASSWORD = os.environ['ROUTER_PASS']
INTERFACE = os.environ['ROUTER_IF']

INFLUXDB_HOST = os.environ['INFLUXDB_HOST']
INFLUXDB_PORT = os.environ['INFLUXDB_PORT']
INFLUXDB_USER = os.environ['INFLUXDB_USER']
INFLUXDB_PASS = os.environ['INFLUXDB_PASS']
INFLUXDB_DB = os.environ['INFLUXDB_DB']
INFLUXDB_NAME = os.environ['INFLUXDB_NAME']

def main():
  while True:
    #print('Running...')
    read_and_submit_data()
    time.sleep(10)

def enable_telnet():
	r = requests.get('http://10.0.0.1/debug_detail.htm', auth=HTTPBasicAuth(USERNAME, PASSWORD))
	data = r.text
	ts = re.search('ts="(\d+)"', data)[1]

	telnet_payload = {'submit_flag': 'debug_info', 'hid_telnet': '1', 'enable_telnet':'on'}
	url = 'http://' + HOST + '/apply.cgi?/debug_detail.htm timestamp=' + ts
	r = requests.post(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), data=telnet_payload)

def read_and_submit_data():
  try:
  	tn = telnetlib.Telnet(HOST)
  except ConnectionRefusedError:
  	enable_telnet()
  	tn = telnetlib.Telnet(HOST)

  tn.read_until(b"login: ")
  tn.write(USERNAME.encode('ascii') + b"\n")
  tn.read_until(b"Password: ")
  tn.write(PASSWORD.encode('ascii') + b"\n")
  tn.read_until(b"RBR40:/# ")
  tn.write(b"ifconfig " + INTERFACE + "\n")
  tn.write(b"exit\n")
  if_data = tn.read_all().decode('ascii')

  rx = re.search('RX bytes:(\d+) ', if_data)[1]
  tx = re.search('TX bytes:(\d+) ', if_data)[1]
  #print(rx, tx)
  #exit()

  client = InfluxDBClient(INFLUXDB_HOST, INFLUXDB_PORT, INFLUXDB_USER, INFLUXDB_PASS, INFLUXDB_DB)
  time = datetime.datetime.utcnow().isoformat()
  influx_json_body = [
    {
      "measurement": "netgear",
      "tags": {
        "host": INFLUXDB_NAME
      },
      "time": time,
      "fields": {
        "rx_bytes": int(rx),
        "tx_bytes": int(tx)
      }
    }
  ]
  client.write_points(influx_json_body)

main()
