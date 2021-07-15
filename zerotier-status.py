# -*- coding: utf-8 -*-
import requests
from colorama import init
init(autoreset=True)

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
  
  ipv4=[]
  ipv6=[]
  for ip in data['config']['ipAssignments']:
    if ( ip.find(".",0,len(ip)) != -1 ):
      ipv4.append(ip)
    elif (ip.find(":",0,len(ip)) != -1 ):
      ipv6.append(ip)
  ipv4.extend(ipv6)
  ipAssignments=""
  for x in range(len(ipv4)):
    ipAssignments= ipAssignments +ipv4[x]
    if(x<len(ipv4)-1):
      ipAssignments = ipAssignments +" / "

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

title =         "{:<10.10}".format('nodeId')+"\t"
title = title + '{name:<{len}}'.format(name="name",len=20-len("name".encode('GBK'))+len("name")) + '\t'
title = title + "{:<10.10}".format("online")  +"\t"
title = title + "{:<13.13}".format('clientVersion')  +"\t"
title = title + "{:<20.20}".format('physicalAddress') + "\t"
title = title + "ipAssignments"

print('\033[1;32m'+title+'\033[0m')

for x in range(len(data)):
  outstr = resultFormat(data[x]) 
  print(outstr)
