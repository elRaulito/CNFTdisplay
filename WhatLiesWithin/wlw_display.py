import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
import time
import requests
import json
import random
import base64
def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))

def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')
limit=5 #how many nfts to load?
#what is the address?
owner="addr1qywywxe3ag9sf3jjhk8hdv3e46jl2ufehhz69v52k8nfza0a8f4leccdwaz2c40fe7g5dk9z5p8v07evuthxnp3xqefs2pw5yg"


html="""
<html><head>
  <style>
    body  {overflow:hidden;
    background:black;}
    #over { font-size:5em; position:absolute; top:20px; left:30%; z-index:2 }
    </style>
</head>
<body>
  <div style="text-align:center">
<iframe id="nft-file-0" marginwidth="0" marginheight="0" allow="geolocation;magnetometer;gyroscope;accelerometer" sandbox="allow-scripts" src="NFT" style="width: 100%; height: 100%; border: 0px; padding: 0px; margin: 0px; overflow: hidden;"></iframe>
<div id="over" style="color:white"><p>NAME<p></div>
</div>
</body>
</html>

"""


def get_Awoken(address):

    url = "https://cardano-mainnet.blockfrost.io/api/v0/addresses/"+address
    payload={}
    headers = {
      'project_id': 'mainnet1o2gGtf57cLUAOXkj1S90LUPNJJRNiNX'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    response=json.loads(response.text)
    stake_address=response['stake_address']#this line is new
    data = {}
    page=1
    counter=0
    total=[]
    while len(response)>0:
        url='https://cardano-mainnet.blockfrost.io/api/v0/accounts/'+stake_address+'/addresses/assets?page='+str(page)#new line
        response = requests.request("GET", url, headers=headers, data=payload)#new line
        response=json.loads(response.text)#new line
        total+=response
        page+=1
        #print(response)
        print(total)
    try:
        for nft in total:#line changed
            print(nft)
            if "lovelace" not in nft['unit'] and "e8209a96a456202276f66224241a703676122d606d208fe464f2e09f" in nft['unit']:
                counter=counter+1
                if counter>limit:
                    continue
                url = "https://cardano-mainnet.blockfrost.io/api/v0/assets/"+nft['unit']
                print(url)
                payload={}
                headers = {
                  'project_id': '5JnwhqGoyF2CyTjns9IRXFrqysfJeQZl'
                }

                metadata = json.loads(requests.request("GET", url, headers=headers, data=payload).text)
                data[nft['unit']]={}
                data[nft['unit']]['asset']=nft['unit']
                try:
                    data[nft['unit']]['name']=metadata['onchain_metadata']['name']

                except:
                    data[nft['unit']]['name']=metadata['onchain_metadata']['title']
                try:
                    data[nft['unit']]['html']=''.join(metadata['onchain_metadata']['files'][0]['src'])
                except:
                    print("image not found")
    except Exception as ex:
        print(ex)
        print("error")
        data['result']='ma un indirizzo con nft veri no eh?'
    return data


array={}


array=get_Awoken(owner)


def job():
    nft=random.choice(list(array.values()))
    src=nft['html']
    name=nft['name']
    print(name)
    page=html.replace("NFT",src)
    page=page.replace("NAME",name)
    web.setHtml(page)
    web.show()


app = QApplication(sys.argv)
web = QWebEngineView()
web.showFullScreen()
nft=random.choice(list(array.values()))
src=nft['html']
name=nft['name']
print(name)
page=html.replace("NFT",src)
page=page.replace("NAME",name)
web.setHtml(page)
print(page)
web.show()
timer = QtCore.QTimer(interval=40*1000)
timer.timeout.connect(job)
timer.start()
sys.exit(app.exec_())
