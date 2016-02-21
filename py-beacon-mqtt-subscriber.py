import time
import ConfigParser
import json
import paho.mqtt.client as mqtt
import os
import subprocess
import re
from subprocess import Popen
from pprint import pprint
import collections
import itertools
import operator
# load data


eventmap = []
key_status='status'
key_uuid='uuid'
key_files='files'
key_fileName='fileName'
# status never,playing,completed,status
never='never'
playing='playing'
completed='completed'
skipped='skipped'
MAX_LENGTH = 5
circularBuffer = collections.deque(maxlen=MAX_LENGTH)
appendCount=0
with open('eventmap.json') as data_file:
	eventmap = json.load(data_file)


def findProcess(processName):
	ps = subprocess.Popen("ps | grep " + processName,
						  shell=True, stdout=subprocess.PIPE)
	output = ps.stdout.read()
	# print output
	ps.stdout.close()
	ps.wait()
	return output


def isProcessRunning(processName):
	output = findProcess(processName)
	# print "isProcessRunning : " +output
	if output.find(processName) != -1:
		return True
	else:
		return False

deviceID = ""
currentStatus = ""
# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, rc):
	# print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("/lab3/ble/nearest/")

# The callback for when a PUBLISH message is received from the server.


def getEventMapFileName(eventmap, input_uuid):
	print 'getEventMapFileName '+input_uuid
	fileName = "no file"
	for _data in eventmap:
		if(_data[key_uuid] == input_uuid) == True:
			if(_data[key_status]==never)==True:
				fileName = _data[key_files][0][key_fileName]
			elif(_data[key_status]==completed)==True:
				fileName = _data[key_files][1][key_fileName]
			elif(_data[key_status]==skipped)==True:
				fileName = _data[key_files][2][key_fileName]
			else:
				fileName = _data[key_files][0][key_fileName]
			
			print "playing file " + fileName
	return fileName


def playFile(filePath):
	print filePath
	if(os.path.isfile(filePath))==True:
		cmd = 'mpg321 ' + filePath + ' &'
		print cmd
		os.system(cmd)
	else :
		print "error open file :"+filePath



def getEventmapStatus(input_uuid):
	global eventmap
	for _data in eventmap:
		if (_data[key_uuid] == input_uuid) == True:
			return _data['status']
	return ""


def updateEventmapStatus(input_uuid, status):
	global eventmap
	output_uuid = None
	# print eventmap
	for _data in eventmap:
		if (_data[key_uuid] == input_uuid) == True:
			_data['status'] = status
			print eventmap
			return _data['status']

def most_common(lst):
	print lst
	return max(set(lst), key=lst.count)

def appendBuffer(input_uuid):
	global appendCount
	# print len(circularBuffer)
	output_uuid = None
	if(appendCount < MAX_LENGTH ):
		circularBuffer.append(input_uuid)
		appendCount+=1
		print circularBuffer
	else:
		appendCount=0
		# output_uuid = circularBuffer
		output_uuid = most_common(circularBuffer)
		circularBuffer.clear()
	return output_uuid

def on_message(client, userdata, msg):
	# print(msg.topic+" "+str(msg.payload))
	obj = json.loads(msg.payload)
	global deviceID
	# print ('deviceID: ' + deviceID)
	# print ('obj[id]: ' + obj['id'])
	# print (deviceID == obj['id'])
	global eventmap
	global currentStatus
	# compair the current uuid
	# if uuid does not match skip the process
	obj_uuid = obj['id']
	value=float(obj['val'])
	print appendBuffer(obj_uuid)

	# if(value>-75) == True:
	# 	print 'value ' + str(value )
	# 	if (deviceID == obj_uuid) == False:
	# 		if isProcessRunning('mpg321') == False:
	# 			print "play track directly"
	# 			deviceID = obj_uuid
				
	# 			print 'event map status ' + getEventmapStatus(deviceID)
	# 			currentStatus = getEventmapStatus(deviceID)
	# 			if( currentStatus == 'never') == True:
	# 				print 'never play'
	# 				currentStatus = updateEventmapStatus(deviceID, 'playing')
	# 			elif(currentStatus == 'playing') == True:
	# 				print 'playing'
	# 				currentStatus = updateEventmapStatus(deviceID, 'completed')
	# 			elif(currentStatus== 'completed') == True:
	# 				print 'paly completed note'
	# 			elif(currentStatus == 'skipped') == True:
	# 				print 'play skipped note'
					
	# 			fileName = getEventMapFileName(eventmap, deviceID)
	# 			playFile(fileName)
	# 			print 'event map status ' + getEventmapStatus(deviceID)
	# 		else:
	# 			print "skip current track"
	# 			currentStatus = updateEventmapStatus(deviceID, 'skipped')
	# 			os.system('pkill mpg321')
	# 			deviceID = obj_uuid
	# 			if( currentStatus == 'never') == True:
	# 				print 'never play'
	# 				currentStatus = updateEventmapStatus(deviceID, 'playing')
	# 			fileName = getEventMapFileName(eventmap, obj_uuid)
	# 			playFile(fileName)
	# 	else:
	# 		if isProcessRunning('mpg321') == False:
	# 			currentStatus = updateEventmapStatus(deviceID, 'completed')
		

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

# Non Blocking call interface
# It starts a thread and is a more preferred method for use
client.loop_start()
