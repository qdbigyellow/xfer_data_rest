from flask import Flask
import json
import urllib.request as request
from influxdb import InfluxDBClient
from config import Configurations

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello Hewen!"

@app.route("/getdata")
def fetch_data_to_influx(data):
    for data in read_data():
        client = InfluxDBClient(host=Configurations.DB.INFLUXHOST, port=Configurations.DB.INFLUXPORT, database=Configurations.DB.DBNAME)
        client.write_points(data)
    
def read_data():
    for l in Configurations.Server.dest:
        result = json.load(request.urlopen(l))
        print(result)
        yield result


if __name__  == '__main__':
    app.run()