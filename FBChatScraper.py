#!/usr/bin/python3

from collections import defaultdict
from time import time
import argparse
import json

import requests as rq
import gzip

import FBChatScraperConfig as config

url_thread = "https://www.messenger.com/api/graphqlbatch/"

headers = config.headers

class FacebookChatScraper:
  def __init__(self, args):
    self.ses = rq.Session()
    self.thread = args.thread

    self.before = args.before

    self.number = args.number
    self.all = args.all
    
    self.file = args.file
    if self.file:
      self.output_file = open("data/"+self.file, 'w')
      
    self.fetched = 0

    self.user_message_count = args.user_message_count
    
    if self.user_message_count:
      self.user_message_counter = defaultdict(int)

    self.extracted_messages = list()

  def run(self):

    messagesPerChunk = 1000
    iteration = 0

    if not self.before:
      before = None
    else:
      before = self.before

    messageLog = list()

    while (True): #if you have hit the end

      #get the json for this block of messages
      thread_contents = self.download_thread(self.thread, messagesPerChunk, before)
    
      print("got iteration ", iteration, " messages")

      #update before so next message download continue right before this chunk
      before = thread_contents['o0']['data']['message_thread']['messages']['nodes'][0]["timestamp_precise"] #timestamp of earliest messsage

      #get the interesting part, the message log, and append it to list of messages
      for node in thread_contents['o0']['data']['message_thread']['messages']['nodes']:
        self.extract_content_from_message_node(node)

      if (not thread_contents['o0']['data']['message_thread']['messages']["page_info"]["has_previous_page"]): #if you have hit the end
        break

      iteration+=1

    #write messages to file
    self.write_to_file(self.extracted_messages)
    
    self.finish()

  def download_thread(self, thread, messagesPerChunk, before):
    """Download the specified number of messages from the
    provided thread, with an optional offset
    """
    data = self.offset_request_data(self.thread, before, messagesPerChunk)

    res = self.ses.post(url_thread, data=data, headers=headers)
    
    #split so you only get the first dictionary that is returned otherwise json will break when it receives second dictionary
    goodContent = res.text.split('\n')[0]

    thread_contents = json.loads(goodContent)
    return thread_contents

  def offset_request_data(self, thread, before, messagesPerChunk):
    data = config.request_data

    print(before)

    requestDataQueryField = json.loads('{"o0":{"doc_id":"xxxxx","query_params":{"id":"xxxxx","message_limit":400,"load_messages":1,"load_read_receipts":true,"before":null}}}')
    
    # Set doc id (unsure what this is)
    requestDataQueryField['o0']['doc_id']= '1763598403704584'

    #set the id of the conversation
    requestDataQueryField['o0']['query_params']['id'] = thread

    #set number of messages to download in this packet
    requestDataQueryField['o0']['query_params']['message_limit'] = messagesPerChunk

    #enable loading messages
    requestDataQueryField['o0']['query_params']['load_messages'] = 1

    #enable loading read_receipt
    requestDataQueryField['o0']['query_params']['load_read_receipts'] = True

    #Set the before to pull messages from
    requestDataQueryField['o0']['query_params']['before'] = before

    data['queries'] = json.dumps(requestDataQueryField)

    return data

  def extract_content_from_message_node(self, node):
    #Get the content you want from each message
      if(node.get('message') and node.get('message_sender') and node.get('timestamp_precise')): #if node has a message and a sender and a timestamp
        messageDict = dict()

        messageDict['timestamp']  = int(node['timestamp_precise'])
        messageDict['author']     = str(node['message_sender']['id'])
        messageDict['text']       = str(node['message']['text'])

        self.extracted_messages.append(messageDict)

      return

  def write_to_file(self, extracted_messages):

    outList = sorted(extracted_messages, reverse=False, key=lambda x: x['timestamp'])

    for node in outList:
      self.output_file.write(str(node['timestamp'])
                            +str(',')
                            +str(node['author'])
                            +str(',')
                            +str(node['text'])
                            +str('\n'))
    return 

  def handle_messages(self, messages):
    #Perform specied actions on messages

    #TO DO: Implement

    return True

  def finish(self):
    print("Download Completed, closing file...")
    if self.file:
      self.output_file.close()


def main():
  args = parse_args()
  fbcs = FacebookChatScraper(args)
  fbcs.run()


# Validate correct command line arguments
def check_negative(value):
  ivalue = int(value)
  if ivalue < 0:
    raise argparse.ArgumentTypeError('%r is not a positive integer' % value)
  return ivalue

# Parse the command line arguments
def parse_args():
  parser = argparse.ArgumentParser(description='Downloads and parses Facebook conversations')
  number = parser.add_mutually_exclusive_group(required=True)

  parser.add_argument('thread',
            help='the id of the conversation to be downloaded')

  number.add_argument('--number', '-n', type=check_negative,
            metavar='N',
            help='the (approximate) number of messages to perform actions on')

  number.add_argument('--all',
            action='store_true',
            help='perform actions on all messages')

  parser.add_argument('--before', type=check_negative, default=0,
            help='get messages starting before this timestamp')

  parser.add_argument('--file', '-f',
            help='file to save messages to')
            
  parser.add_argument('--user-message-count', '--umc',
            action='store_true',
            help='count the number of messages each user has sent')

  return parser.parse_args()

if __name__ == '__main__':
  main()
