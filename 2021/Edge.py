import pickle
import paho.mqtt.client as mqtt
import socket
import sqlite3
from threading import Thread
import random as r
import time

'''
topics subscribe
migration request

topics to publish
system util

migrate if soure Ip matches

function to handle request
'''


class BrokerCom:
    def __init__(self, user, pw, ip, sub_topic):
        self.user = user
        self.pw = pw
        self.ip = ip
        self.port = 16470  # 1883
        self.topic = sub_topic
        self.client = mqtt.Client()
        self.mec_ip = ip_address()
        self.edge_servers = set()
        self.client.username_pw_set(self.user, self.pw)
        self.client.connect(self.ip, self.port, 60)
        self.run = True
        self.start()

    def start(self):
        t1 = Thread(target=self.broker_loop, daemon=True)
        t1.start()

    def on_connect(self, connect_client, userdata, flags, rc):
        print("Connected with Code :" + str(rc))
        # Subscribe Topic from here
        connect_client.subscribe(self.topic)

    def on_message(self, message_client, userdata, msg):
        print(f'Topic received: {msg.topic}')
        data = pickle.loads(msg.payload)
        if data['source_ip'] == self.mec_ip:
            handle_migration(data=data)

    def publish(self, topic, data):
        self.client.publish(topic, data)

    def broker_loop(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.loop_start()
        while True:
            if not self.run:
                self.client.loop_stop()
                self.client.disconnect()
                break

    def __del__(self):
        print('Broker Communication Object Deleted!')


def ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def handle_migration(data):
    print(f'handling \n{data}')


def run():
    while True:
        system_util = {
            'node_ip': ip_address(),
            't_stamp': time.time(),
            'util': {
                'cpu': r.randrange(30, 90),
                'mem': r.randrange(20, 90),
                'net': r.randrange(10, 90),
                'sto': r.randrange(30, 90),
                'bat': r.randrange(20, 90),
            }
        }
        data = pickle.dumps(system_util)
        broker.publish(topic='util', data=data)
        time.sleep(60)


broker = BrokerCom(user='yrtwmwao', pw='FmgTf5G8r-4f', ip='m24.cloudmqtt.com', sub_topic='migration')

run()
