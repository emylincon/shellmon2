import paho.mqtt.client as mqtt
import os
import socket
from threading import Thread
import ast

username = 'shellmon'
password = 'shellmon'
broker_port_no = 1883
topic = 'shellmon'
thread_list = []   # all threads
shell_record = {}
topic_list = []


def subscribe_to(data):
    d_list = ast.literal_eval(data)
    mo = set(d_list) - set(topic_list)
    return len(mo), mo


class Shell:
    _client = mqtt.Client()

    def __init__(self, _topic_):
        self._topic_ = _topic_

    def on_connect_(self, connect_client, userdata, flags, rc):
        print("Connected with Code :" + str(rc))
        # Subscribe Topic from here
        connect_client.subscribe(self._topic_)

    def on_message_(self, message_client, userdata, msg):
        # print the message received from the subscribed topic
        print('{}: '.format(self._topic_), str(msg.payload, 'utf-8'))
        shell_record[self._topic_].append(str(msg.payload, 'utf-8'))

    def shell_loop(self):
        self._client.loop_forever()

    def shell_connect(self):
        self._client.on_connect = self.on_connect_
        self._client.on_message = self.on_message_

        self._client.username_pw_set(username, password)
        self._client.connect(broker_ip, broker_port_no, 60)

        cl = Thread(target=self.shell_loop)
        thread_list.append(cl)
        cl.start()


def daemon_func(args):
    Shell(args).shell_connect()


def thread_def(arg):
    thread_list.append(Thread(target=daemon_func, args=(arg,)))
    thread_list[-1].start()


def start_up():
    global broker_ip

    os.system('clear')
    print('-----------------------------------')
    print('Welcome to MQTT Subscriber client')
    print('-----------------------------------')

    broker_ip = input('Enter Broker IP: ')

    print('-----------------------------------')


# Callback Function on Connection with MQTT Server
def on_connect(connect_client, userdata, flags, rc):
    print("Connected with Code :" +str(rc))
    # Subscribe Topic from here
    connect_client.subscribe(topic)


# Callback Function on Receiving the Subscribed Topic/Message
def on_message(message_client, userdata, msg):
    # print the message received from the subscribed topic
    print('Publisher: ', str(msg.payload, 'utf-8'))
    t_topic = str(msg.payload, 'utf-8').split()
    if t_topic[0] == 'bk':
        sub = subscribe_to(' '.join(t_topic[1:]))
        if sub[0] > 0:
            for topics in sub[1]:
                thread_def(topics)


def client_loop():
    client.loop_forever()


def mqtt_connect():
    global client

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set(username, password)
    client.connect(broker_ip, broker_port_no, 60)

    cl = Thread(target=client_loop)
    thread_list.append(cl)
    cl.start()


def main():
    start_up()
    mqtt_connect()

