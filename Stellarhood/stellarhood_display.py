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
limit=50 #how many nfts to load?
#what is the address?
owner="addr1q9gv35dx8vd740u88qjuvv46tz62te8cw0w6qxwxldmsg2uqkztps9jkxsls37sa764g7xmd7a3cvuyp4d9d25razucs2glmys"


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
</div>
</body>
</html>

"""



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
            if "91acca0a2614212d68a5ae7313c85962849994aab54e340d3a68aabb" in nft['unit'] :
                if counter>limit:
                    continue
                print("here")
                counter=counter+1
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
                    base64_message = ''.join(metadata['onchain_metadata']['files'][0]['src']).replace("data:text/html;base64,","")
                    print(base64_message)
                    base64_bytes = base64_message.encode('utf-8')
                    message_bytes = base64.b64decode(base64_bytes)
                    message = message_bytes.decode('utf-8')
                    message=message.replace("FS=M=oS=0;","FS=M=oS=0;FS=1;").replace("</script></body>","ka(cF,iw,ih);</script></body>")
                    message_bytes = message.encode('utf-8')
                    base64_bytes = base64.b64encode(message_bytes)
                    base64_message = base64_bytes.decode('utf-8')
                    data[nft['unit']]['html']="data:text/html;base64,"+base64_message
                except Exception as ex:
                    print("image not found ", ex)
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
    page=html.replace("NFT",src)
    web.setHtml(page)
    web.show()


app = QApplication(sys.argv)
web = QWebEngineView()
web.showFullScreen()
nft=random.choice(list(array.values()))
src=nft['html']
page=html.replace("NFT",src)
web.setHtml(page)
print(page)
web.show()
timer = QtCore.QTimer(interval=10*1000)
timer.timeout.connect(job)
timer.start()
sys.exit(app.exec_())
