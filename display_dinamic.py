import sys
import time
import math
if sys.version_info[0] == 2:  # the tkinter library changed it's name from Python 2 to 3.
    import Tkinter
    tkinter = Tkinter #I decided to use a library reference to avoid potential naming conflicts with people's programs.
else:
    import tkinter
from PIL import Image, ImageTk, ImageDraw

from tkinter import *
from PIL import Image, ImageTk, ImageDraw
import requests
import json
import random

#EDIT
limit=50 #how many nfts to load?
#what is the address?
owner="addr1q9dzwgq9t8pvlc7n76r7d46rrshe5s4v0gd7lmzenfxg49lrsguyk4655g488x3hzdyvwlz9zygp8aee6t2hzgc2p9rqry4rcg"




counter=0
def get_Images(address):

    url = "https://cardano-mainnet.blockfrost.io/api/v0/addresses/"+address
    payload={}
    headers = {
      'project_id': 'mainnet1o2gGtf57cLUAOXkj1S90LUPNJJRNiNX'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    response=json.loads(response.text)
    data = {}
    counter=0
    try:
        for nft in response['amount']:
            if "lovelace" not in nft['unit']:
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
                    print(metadata['onchain_metadata']['image'])
                    print("*******")
                    data[nft['unit']]['image']="https://ipfs.blockfrost.dev/ipfs/"+metadata['onchain_metadata']['image'].replace("ipfs://","").replace("ipfs/","")

                except:
                    print("image not found")
    except Exception as ex:
        print(ex)
        print("error")
        data['result']='ma un indirizzo con nft veri no eh?'


    return data


array={}


class myGUI(object):
    def __init__(self):
        self.root = Tk()

        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.canvas = Canvas(width=w, height=h, bg='black')
        self.canvas.pack()
        self.root.overrideredirect(1)
        self.root.geometry("%dx%d+0+0" % (w, h))
        secondi=time.localtime().tm_sec

        try:
            print(random.choice(list(array.items())))
            url=random.choice(list(array.items()))[1]['image']
            image=Image.open(requests.get(url, stream=True, timeout=5).raw)
            w2,h2=image.size
            print(w2,h2)
            x=w/w2
            y=h/h2
            print(x,y)
            if x>y:
                image=image.resize((int(y*w2),h),Image.ANTIALIAS)
            else:
                image=image.resize((w,int(x*h2)),Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(image)
            self.img = self.canvas.create_image(w/2,h/2, image=self.photo)
            self.root.after(1000, self.change_photo)
            self.root.mainloop()
        except Exception as ex:
            print(ex)
            print("no image")
            self.root.after(1, self.change_photo)
            self.root.mainloop()


    def change_photo(self):
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        secondi=time.localtime().tm_sec
        try:
            print(random.choice(list(array.items())))
            choice=random.choice(list(array.items()))[1]
            url=choice['image']
            image=Image.open(requests.get(url, stream=True, timeout=5).raw)
            w2,h2=image.size
            print(w2,h2)
            x=w/w2
            y=h/h2
            print(x,y)
            if x>y:
                image=image.resize((int(y*w2),h),Image.ANTIALIAS)
            else:
                image=image.resize((w,int(x*h2)),Image.ANTIALIAS)
            #draw = ImageDraw.Draw(image)
            #draw.text((w/2, h/10),choice['name'])
            self.photo = ImageTk.PhotoImage(image)
            self.canvas.itemconfig(self.img, image=self.photo)
            self.root.after(1000, self.change_photo)
        except Exception as ex:
            print(ex)
            print("no image")
            self.root.after(1, self.change_photo)


if __name__ == "__main__":
    array=get_Images(owner)
    print(array)
    print(len(array))
    gui = myGUI()
