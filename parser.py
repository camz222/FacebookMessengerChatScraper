##Facebook Chat Log JSON -> Human

import os
import sys
import json
from config import friends

if len(sys.argv) <= 1:
	print("Usage: \t python parser.py [path_to_folder]")
	print("Example: \t python parser.py ./Messages/HouseChat")
	sys.exit()

path = sys.argv[1]


with open(path+'messageLog.txt', 'w') as outputLog:
	for f in os.listdir(path):
		if '.json' not in f: #if not a .json file
			continue

		print("Parsing ", f)
		
		with open(path+f, 'r') as file:
			dump = json.load(file)

		messageLog = dump["payload"]["actions"]

		for message in messageLog:
			author_ID = message["author"].split('fbid:')[1] #get everything after fbid

			if author_ID not in friends.keys(): #if we dont have this persons fbid matching a name in config file, skip over them
				continue 

			author_name = friends[author_ID]

			message_body = message["body"]

			chatMessage = str(author_name) + ': ' + str(message_body) + str('\n')

			outputLog.write(chatMessage)