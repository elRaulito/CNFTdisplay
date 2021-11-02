import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
import time
import requests
import json
import random
limit=50 #how many nfts to load?
#what is the address?
owner="addr1q9yuy9tdge82h2lssu6kmykx5x4t8aqazscwahetl0kt64jz5jepupj25990gfpg59kg9q0su9uxyxr8n5ra03d479hskp3723"


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
<div id="over">NAME</div>
</div>
</body>
</html>

"""


counter=0
def get_Refresh(address):

    url = "https://cardano-mainnet.blockfrost.io/api/v0/addresses/"+address
    payload={}
    headers = {
      'project_id': 'mainnet1o2gGtf57cLUAOXkj1S90LUPNJJRNiNX'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    response=json.loads(response.text)
    stake_address=response['stake_address']#this line is new
    data = {}
    counter=0
    url='https://cardano-mainnet.blockfrost.io/api/v0/accounts/'+stake_address+'/addresses/assets'#new line
    response = requests.request("GET", url, headers=headers, data=payload)#new line
    response=json.loads(response.text)#new line
    try:
        for nft in response:#line changed
            if "lovelace" not in nft['unit'] and "adc5716393953403109c335e68c0384238fd19653e960e03afa1fb1f" in nft['unit']:
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


array=get_Refresh(owner)


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
page=html.replace("NFT",src)
page=page.replace("NAME",name)
web.setHtml(page)
web.show()
timer = QtCore.QTimer(interval=1*1000)
timer.timeout.connect(job)
timer.start()
sys.exit(app.exec_())
