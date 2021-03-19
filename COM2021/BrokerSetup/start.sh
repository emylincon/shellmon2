/etc/init.d/mosquitto start
my_ip=$(ip route get 8.8.8.8 | awk -F"src " 'NR==1{split($2,a," ");print a[1]}')
data="#MQTT Server Details\n\n#Username\nadmin\n#Password\npassword\n#IP Address\n${my_ip}"
echo $data > show
nano show
