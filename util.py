copiedHeader ="""
<PASTE HEADER FROM CHROME DEV TOOLS HERE>
"""

def chrome_copied_header_to_dict(headerString):
  #separate line items
  keyValuePairs = copiedHeader.split("\n")

  #remove empty items
  keyValueStrings = list(filter(None, keyValuePairs))

  #remove leading colon for psueod-headers: authority, method, path, scheme
  keyValueStrings = [ line[1:] if (line[0] == ":") else line for line in keyValueStrings]

  outDict = dict()
  #create ditionary splitting by first colon instance
  for keyValue in keyValueStrings:
    key = keyValue.split(':', 1)[0]
    value = keyValue.split(':', 1)[1].strip() #get rid of leading or trailing white space from key

    outDict[key] = value

  return outDict

headerDict = chrome_copied_header_to_dict(copiedHeader)
print(headerDict)


def parse_cookie(cookie):
  #put cookies into request session cookie jar
  
  # TO DO: Implement

  return True
