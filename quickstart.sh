#start mosquitto deamon 
# mosquitto -d

cd /home/pi/py-beacon
#start beacon collactor and emitter
sudo python ./collector.py &
sudo python ./emitter.py &

#gotto working directory
cd /home/pi/example
sudo python counter.py &
python py-beacon-mqtt-subscriber.py &
