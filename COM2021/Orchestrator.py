import pickle
import random as r
import socket
import time
from BrokerCommunication import MyBroker
from MyDatabase import Database

db = Database()

'''
topics to subscribe
system util

topics to publish
migration request

send data to db

open function:
    db_insert
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


class BrokerCom(MyBroker):
    def __init__(self, user, pw, ip, sub_topic, port=1883):
        super().__init__(user, pw, ip, sub_topic, port)
        self.edge_servers = set()

    def on_message(self, message_client, userdata, msg):
        print(f'Topic received: {msg.topic}')
        data = pickle.loads(msg.payload)
        self.edge_servers.add(data['node_ip'])  # adds to the set of edge servers
        db_insert(data)


def ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def db_insert(data):
    db.add_data(data)
    print(data)


def migration_req():
    '''
    edit this
    :return:
    '''
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


broker = BrokerCom(user='yrtwmwao', pw='FmgTf5G8r-4f', ip='m24.cloudmqtt.com', sub_topic='util', port=16470)
