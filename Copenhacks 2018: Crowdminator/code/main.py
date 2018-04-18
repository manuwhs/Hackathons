########### Python 2.7 #############
import httplib, urllib, base64, json

import utils

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib import patches
from io import BytesIO
import requests
 
import time 

plt.close("all")
#####
labels_negative = [ 'sadness','disgust','fear','anger']
labels_positive = ["happiness", 'surprise']
labels_neutral = ['neutral']

###########
### Input data 
#####
image_url1 = "http://ak4.picdn.net/shutterstock/videos/2173574/thumb/1.jpg?i10c=img.resize(height:160)"
image_url2 = "https://github.com/kubaex/Pics/blob/master/pic10.jpg?raw=true"
image_url3 = "https://img.huffingtonpost.com/asset/5a32b3501500002a0049bb49.jpg?ops=scalefit_630_noupscale"
images_urls = [image_url1,image_url2,image_url3]
#images_urls = [image_url1]


npics = 5
if(1):
    images_urls = []
    
    for i in range(1,npics):
        images_urls.append("https://github.com/kubaex/faces/blob/master/faces(%i).jpg?raw=true"%i)
    
    n_ima = 0
    
    list_x = []
    list_y = []
    for image_url in images_urls:
        ## Get the emotions of the image
        ## So that we do not violate the number of requests
        time.sleep(10)
        emotions_list,fr_list = utils.get_emotions(image_url)
    
        Npeople = len(emotions_list)
        
        if(Npeople == 0):
            continue
        
        Results_image = dict([["negative",0.0],["positive",0.0], ["neutral",0.0]])
    
    
        list_emotions = []
        for i in range(Npeople):
            emotions = emotions_list[i]
    
            for label in labels_negative:
                Results_image["negative"] += emotions[label]
            for label in labels_positive:
                Results_image["positive"] += emotions[label]
            for label in labels_neutral:
                Results_image["negative"] += emotions[label]
                
        #print emotions
        
    
        Results_image['positive'] = Results_image['positive']/Npeople
        Results_image['neutral'] = Results_image['neutral']/Npeople
        Results_image['negative'] = Results_image['negative']/Npeople
    
        #----------------
        fig = plt.figure()
        ax = plt.subplot2grid((2,3),(1, 2))
        xlabels = ('positive',"neutral","negative")
        y_pos = np.arange(len(xlabels))
        performance = [Results_image['positive'], Results_image['neutral'],Results_image['negative']]
         
        ax.bar(y_pos, performance, align='center', alpha=0.8)
        plt.xticks(y_pos, xlabels)
        plt.ylabel('Distribution')
        plt.title('Impact of the presentation')
        plt.ylim(0,1.3)
        
        ax.xaxis.label.set_size( fontsize = 20)
        ax.yaxis.label.set_size( fontsize = 20)
        ax.title.set_fontsize(fontsize=18)
        
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(14) 
        plt.show()
    
    
        #--------------------------------
        
        list_x.append(n_ima)
        list_y.append(Results_image['positive'])
        
        ax3 = plt.subplot2grid((2,3),(0, 2))
    
        ax3.plot(list_x,list_y)
        
        list_y2 = np.array(list_y)*100
        ax3.fill_between(list_x,list_y2,0, zorder=10)
        
        th = 50
        ax3.fill_between(list_x,list_y2,th,  where= np.array(list_y2) > th, zorder=11,color = "r")
        
        plt.ylabel('Percentage (%)')
        plt.title('Positivity tracking')
        plt.xlabel('time')
        plt.ylim(0,130)
        plt.xlim(0,len(images_urls))
        
        ax3.xaxis.label.set_size( fontsize = 16)
        ax3.yaxis.label.set_size( fontsize = 16)
        ax3.title.set_fontsize(fontsize=18)
        
        
        plt.show()
        # ----------------------
        
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
    
        ax2 = plt.subplot2grid((1,3),(0, 0),colspan=2,rowspan=2)
        ax2.imshow(image, alpha=0.7)
        for j in range(len(fr_list)):
            face = fr_list[j]
            fr = face
            origin = (fr["left"], fr["top"])
            
            green = hex(int(emotions_list[j]["happiness"] * 255)).split("x")[1]
            red = hex(int((1-emotions_list[j]["happiness"]) * 255)).split("x")[1]
            
            if (len(green) == 1):
                green = "0"+ green
            if (len(red) == 1):
                red = "0"+ red        
            p = patches.Rectangle(origin, fr["width"], fr["height"], fill=False, linewidth=6, color="#"+red+green+"00")
            ax2.axes.add_patch(p)
    #        plt.text(origin[0], origin[1], "%s, %.2f"%("Happy", emotions_list[j]["happiness"]), fontsize=20, weight="bold", va="bottom")
        _ = plt.axis("off")
    
        plt.subplots_adjust(hspace=0.35)
        
        file_dir = './images/%i.png'%n_ima
        
        fig.set_size_inches( 6*3, 4*2)
        fig.savefig(file_dir,
                    bbox_inches = "tight",
                    dpi = 100
                    )
    
        plt.close(fig)
        n_ima+= 1;
            
    
images_path = utils.get_allPaths("./images/")
images_path.sort(cmp = utils.comparador_images_names)
utils.create_video(images_path, output_file = "out.avi", fps = 2)
