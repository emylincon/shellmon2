import paho.mqtt.client as mqtt
import os
import socket
from threading import Thread
import random as r
import time

username = 'shellmon'
password = 'shellmon'
broker_port_no = 1883
topic = 'shellmon'

sub_list = []  # all topics
thread_list = []  # all threads


def ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def start_up():
    global broker_ip

    os.system('clear')
    print('-----------------------------------')
    print('Welcome to MQTT Broker')
    print('-----------------------------------')

    broker_ip = ip_address()
    print('Broker ip: {}'.format(broker_ip))

    print('-----------------------------------')


class Shell:
    _client = mqtt.Client()

    def __init__(self, _topic_):
        self._topic_ = _topic_

    def on_connect_(self, connect_client, userdata, flags, rc):
        print("Subscribed to {} :".format(self._topic_) + str(rc))
        # Subscribe Topic from here
        connect_client.subscribe(self._topic_)

    def on_message_(self, message_client, userdata, msg):
        # print the message received from the subscribed topic
        pass

    def shell_loop(self):
        self._client.loop_forever()

    def shell_connect(self):
        self._client.on_connect = self.on_connect_
        self._client.on_message = self.on_message_

        self._client.username_pw_set(username, password)
        self._client.connect(broker_ip, broker_port_no, 60)

        thread_list.append(Thread(target=self.shell_loop))
        thread_list[-1].start()


def daemon_func(args):
    Shell(args).shell_connect()


def thread_def(arg):
    thread_list.append(Thread(target=daemon_func, args=(arg,)))
    thread_list[-1].start()


# Callback Function on Connection with MQTT Server
def on_connect(connect_client, userdata, flags, rc):
    print("subscribed to {} :".format(topic) + str(rc))
    # Subscribe Topic from here
    connect_client.subscribe(topic)


# Callback Function on Receiving the Subscribed Topic/Message
def on_message(message_client, userdata, msg):
    # print the message received from the subscribed topic
    print('Publisher: ', str(msg.payload, 'utf-8'))
    _topic = str(msg.payload, 'utf-8')
    if _topic.split()[0] != 'bk':
        sub_list.append(_topic)
        thread_def(_topic)
        message = "bk {}".format(sub_list)
        time.sleep(r.randrange(3))
        client.publish(topic, message)


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
    try:
        mqtt_connect()

    except KeyboardInterrupt:
        print('Programme Terminated')
        for i in thread_list:
            i.stop()


main()
