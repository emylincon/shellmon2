import pickle
import socket
import random as r
import time
from BrokerCommunication import MyBroker

'''
topics subscribe
migration request

topics to publish
system util

migrate if source Ip matches

function to handle migration
    handle_migration
'''


class BrokerCom(MyBroker):
    def __init__(self, user, pw, ip, sub_topic, port=1883):
        super().__init__(user, pw, ip, sub_topic, port)
        self.mec_ip = ip_address()

    def on_message(self, message_client, userdata, msg):
        print(f'Topic received: {msg.topic}')
        data = pickle.loads(msg.payload)
        if data['source_ip'] == self.mec_ip:
            handle_migration(data=data)


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


broker = BrokerCom(user='yrtwmwao', pw='FmgTf5G8r-4f', ip='m24.cloudmqtt.com', sub_topic='migration', port=16470)

run()
