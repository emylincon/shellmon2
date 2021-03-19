import pickle
import paho.mqtt.client as mqtt
import socket
from threading import Thread
import random as r
import time
from MyDatabase import *

db = Database()

'''
topics to subscribe
system util

topics to publish
migration request

send data to db

open function:
    db insert
    migrate_request
    
data format

system_util = {
                'node_ip': 1.2.3.4,
                't_stamp': 1234,
                'util':{
                        'cpu': 10,
                        'mem': 20,
                        'net': 30,
                        'sto': 40,
                        'bat': 50
                        }
                }

migration_request = {
        't_stamp': '1234',
        'source_ip': '1.2.3.4',
        'dest_ip': '1.2.3.5',
        'cont_id': 'xyz'
        }

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
        self.edge_servers.add(data['node_ip'])  # adds to the set of edge servers
        db_insert(data)

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


def db_insert(data):
    db.add_data(data)
    print(data)


def migration_req():
    try:
        migration_request = {
            't_stamp': time.time(),
            'source_ip': r.choice(list(broker.edge_servers)),
            'dest_ip': r.choice(list(broker.edge_servers)),
            'cont_id': r.randrange(999999999999)
        }
        data = pickle.dumps(migration_request)
        broker.publish(topic='migration', data=data)
        print(f'published \n {migration_request}')
    except IndexError:
        print('Edge servers List Empty')


def run():
    pass


broker = BrokerCom(user='yrtwmwao', pw='FmgTf5G8r-4f', ip='m24.cloudmqtt.com', sub_topic='util')
# {'node_ip': '136.148.147.234', 't_stamp': 1616190724.9944427,
# 'util': {'cpu': 89, 'mem': 68, 'net': 34, 'sto': 61, 'bat': 22}}
