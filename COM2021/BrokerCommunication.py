from threading import Thread
import paho.mqtt.client as mqtt


class MyBroker:
    def __init__(self, user, pw, ip, sub_topic, port=1883):
        self.user = user
        self.pw = pw
        self.ip = ip
        self.port = port
        self.topic = sub_topic
        self.client = mqtt.Client()
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
