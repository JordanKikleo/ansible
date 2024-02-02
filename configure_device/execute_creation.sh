#!/bin/bash

PORT=$1
device_name=$2
restaurant_name=$3
device_port=$4
device_type=$5
echo "PORT: ${PORT}"

FILE_NAME="variables.py"

restaurant_name=${restaurant_name^^}

echo "Le nom du device est : $device_name"
echo "Le nom du restaurant est : $restaurant_name"
echo "Le port est : $device_port"
echo "Le type est : $device_type"

touch $FILE_NAME
echo "device_name = '$device_name'" > $FILE_NAME
echo "restaurant_name = '$restaurant_name'" >> $FILE_NAME
echo "device_port = '$device_port'" >> $FILE_NAME
echo "device_type = '$device_type'" >> $FILE_NAME

python3 configure_thingsboard_and_mongo.py
scp modify_config.py ec2-user@$PORT:/tmp/
ssh $PORT "python3 /tmp/modify_config.py $device_name $restaurant_name $device_port $device_type"

python3 create_device_config.py
scp deviceConfig.json ec2-user@$PORT:/home/ec2-user/deviceConfig.json
echo "deviceConfig.json file created, now rebooting"
ssh $PORT "sudo -s reboot now"

rm $FILE_NAME
rm deviceConfig.json

echo "DONE" 