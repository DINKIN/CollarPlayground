#!/usr/bin/python
import time, ConfigParser, json
from pprint import pprint

with open('eventmap.json') as data_file:    
	data = json.load(data_file)

for _data in data :
	print(_data['uuid'])
	print(_data['status'])
	_data['status'] = 'playing'
	print(_data['status'])
	for _file in _data['files'] :
		print(_file['fileName'])
