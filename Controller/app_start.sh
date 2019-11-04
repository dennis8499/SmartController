#!/bin/sh
#echo "GreenGrass Start"
#cd /greengrass/ggc/core/
#sudo ./greengrassd start
echo "Start Program after 20s"
sleep 20
sudo cp ~/asoundrc ~/.asoundrc
amixer set 'MI Portable Bluetooth - A2DP' -- 85%
sudo cp ~/asoundrc ~/.asoundrc
cd /home/pi/project
python main.py

