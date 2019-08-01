#!/usr/bin/env bash

clear
echo "============ Setting up Your Shellmon platform ================="
sleep 2
apt update && apt upgrade -y
apt install mosquitto mosquitto-clients -y
/etc/init.d/mosquitto start
apt install python3 -y
apt install python3-pip -y
python3