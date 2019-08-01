import paho.mqtt.client as mqtt
import os
import socket
from threading import Thread

username = 'shellmon'
password = 'shellmon'
broker_port_no = 1883
topic = 'shellmon'

sub_list = []   # all topics
thread_list = []   # all threads
client_data = {}    # all data from client
sub_pointer = 0     # keep track of subscriptions
sl = 0   # lenght of sub_List

def start_up():
    global broker_ip

    os.system('clear')
    print('-----------------------------------')
    print('Welcome to MQTT Subscriber client')
    print('-----------------------------------')

    broker_ip = ip_address()

    print('-----------------------------------')


def ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


# Callback Function on Connection with MQTT Server
def on_connect(connect_client, userdata, flags, rc):
    print("Connected with Code :" +str(rc))
    # Subscribe Topic from here
    connect_client.subscribe(topic)


# Callback Function on Receiving the Subscribed Topic/Message
def on_message(message_client, userdata, msg):
    # print the message received from the subscribed topic
    print('Publisher: ', str(msg.payload, 'utf-8'))
    _topic = str(msg.payload, 'utf-8')
    sub_list.append(_topic)
    client_data[_topic] = []


def on_connect2(connect_client, userdata, flags, rc):
    global sub_pointer

    print("Connected with Code :" +str(rc))
    # Subscribe Topic from here
    connect_client.subscribe(sub_list[sub_pointer])
    sub_pointer += 1


# Callback Function on Receiving the Subscribed Topic/Message
def on_message2(message_client, userdata, msg):
    # print the message received from the subscribed topic
    print('Publisher: ', str(msg.payload, 'utf-8'))
    data_ = str(msg.payload, 'utf-8').split()
    client_data[data_[0]].append(' '.join(data_[1:]))  # client sends his topic and data


def client_loop():
    client.loop_forever()


def client_loop2():
    client2.loop_forever()


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


def client_connect():
    global client2

    client2 = mqtt.Client()
    client2.on_connect = on_connect2
    client2.on_message = on_message2

    client2.username_pw_set(username, password)
    client2.connect(broker_ip, broker_port_no, 60)

    cl = Thread(target=client_loop2)
    thread_list.append(cl)
    cl.start()


def check_sub():
    while True:
        try:
            if len(sub_list) != sl:
                d = Thread(target=client_connect)
                thread_list.append(d)
                d.start()
        except KeyboardInterrupt:
            print("Check Sub stopped")
            break


def main():
    try:
        mqtt_connect()

    except KeyboardInterrupt:
        print('Programme Terminated')
        for i in thread_list:
            i.stop()


main()