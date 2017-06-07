#!/usr/bin/env python3
import speedtest
import json
from influxdb import InfluxDBClient

HOST = '127.0.0.1'
PORT = 8086
USER = 'python'
PASSWORD = ''


def runTest():
    servers = []
    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.download()
    s.upload()
    return s.results.dict()


def sendData(data):
    client = InfluxDBClient(HOST, PORT, USER, PASSWORD, 'freifunk')
    # Optional
    # client.create_database('freifunk')
    client.write_points(data, 'ns')
    return "ok"  # "Result: {0}".format(result)


def main():
    result = runTest()
    data = {}
    data['measurement'] = "speed"
    data['tags'] = {}
    data['tags']['country'] = result['country']
    data['tags']['host'] = result['host']
    data['time'] = result['timestamp']
    data['fields'] = {}
    data['fields']['download'] = result['download']
    data['fields']['upload'] = result['upload']
    sendData(data)
    # print(json.dumps(result))


if __name__ == '__main__':
    main()
