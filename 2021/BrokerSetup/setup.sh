#!/usr/bin/env bash

apt update && apt upgrade -y
apt install nano iproute2 net-tools mosquitto mosquitto-clients -y
touch /etc/mosquitto/passwd ; mosquitto_passwd -b /etc/mosquitto/passwd admin password
echo -e 'allow_anonymous false \npassword_file /etc/mosquitto/passwd' > /etc/mosquitto/conf.d/default.conf

