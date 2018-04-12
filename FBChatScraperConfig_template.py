# This can probably be reduced
request_data = {
  "batch_name": "MessengerGraphQLThreadFetcher",
  "__user": "<YOUR USER_ID>",
  "__a": "<YOUR __a>",
  "__dyn": "<YOUR __dyn>",
  "__req": "<YOUR __req>",
  '__be'      : '<YOUR __be>',
  '__pc'      : '<YOUR __pc>',
  "fb_dtsg": "<YOUR fb_dtsg>",
  "ttstamp": "<YOUR ttstamp>",
  "__rev": "<YOUR __rev>",
  "jazoest": "<YOUR jazoest>",
  "queries": '<YOUR queries>'
  }

headers = {
  "authority": "www.messenger.com",
  "method": "POST",
  "path": "/api/graphqlbatch/",
  "scheme": "https",
  "accept": "*/*",
  "accept-encoding": "gzip, deflate",
  "accept-language": "en-US,en;q=0.9",
  "cache-control": "no-cache",
  "content-length": "754",
  "content-type" : "application/x-www-form-urlencoded",
  "cookie": "<YOUR cookie>",
  "origin": "https://www.messenger.com",
  "pragma": "no-cache",
  "referer": "<YOUR _referer (can probably be anything like www.messenger.com/)>",
  "user-agent": "<YOUR user-agent>"
}

# You'll have to generate a list of friend IDs on your own
# TO DO: Extract ID and associate to names in the script
# not currently used, was used in previous script that no longer works
friends = {
    "<ID0>" : "NAME0",
    "<ID1>" : "NAME1",
    "<ID2>" : "NAME2",
    "<ID3>" : "NAME3",
    "<IDetc>" : "NAMEetc",
}

# not currently used, was used in previous script that no longer works
chats = {
    "chatName0" : "chatID0"
    "chatName1" : "chatID1"
    "chatNameetc" : "chatIDetc"
}