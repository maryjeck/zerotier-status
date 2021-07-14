# -*- coding: utf-8 -*-
import requests
from colorama import init
init(autoreset=True)

#first ,you must got your zerotier_ID and API_Tokens ,the curl is https://my.zerotier.com/account
zerotier_ID=""
API_Tokens=""

def resultFormat(data):
  nodeId = "{:<10.10}".format(data['nodeId'])+"\t"
  name   = format(data['name']) 
  if data['online'] == True :
    online = "{:<10.10}".format("online")  +"\t"
  else:
    online = "{:<10.10}".format("offline")  +"\t"
  clientVersion = "{:<13.13}".format(data['clientVersion'])  +"\t"
  ipAssignments=""
  imark=1
  for ip in data['config']['ipAssignments']:
    ipAssignments = ipAssignments + ip
    if imark < len(data['config']['ipAssignments']) :
      ipAssignments = ipAssignments +" / "
    imark = imark+1 
  ipAssignments = ipAssignments + "\t"
  if data['physicalAddress']== None :
    physicalAddress = "{:<20.20}".format("")
  elif len(data['physicalAddress']) > 15:
    physicalAddress = "{:<15.15}".format(data['physicalAddress'])
    physicalAddress = physicalAddress + "....."
  else:
    physicalAddress = "{:<20.20}".format(data['physicalAddress'])
  physicalAddress = physicalAddress +"\t"
  return nodeId + '{name:<{len}}'.format(name=name,len=20-len(name.encode('GBK'))+len(name)) + "\t"+ online + clientVersion + physicalAddress  + ipAssignments


headers={"Authorization": "bearer "+API_Tokens}
curls="https://my.zerotier.com/api/network/"+zerotier_ID+"/member"

r = requests.get(curls, headers=headers)
if r.status_code != 200 :
  print("zerotierID或API_Tokens设置，请重新设置！！")
data=r.json()
imark =1
outstr=""
for x in data:
  outstr =outstr+ resultFormat(x) 
  if imark < len(data):
    outstr = outstr+"\r\n"
  imark=imark+1

title =         "{:<10.10}".format('nodeId')+"\t"
title = title + '{name:<{len}}'.format(name="name",len=20-len("name".encode('GBK'))+len("name")) + '\t'
title = title + "{:<10.10}".format("online")  +"\t"
title = title + "{:<13.13}".format('clientVersion')  +"\t"
title = title + "{:<20.20}".format('physicalAddress') + "\t"
title = title + "ipAssignments"

print('\033[1;32m'+title+'\033[0m')
print(outstr)
