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

        
################ CREATE OUR LIST WITH FACES ####################
faceIDslist = "teammembers_8"
creating_db = 0
if(creating_db):
    list_names_db = ["Manu","Ema","Kuba"]
    list_face_ids_db = []
    list_images_url_db = ["https://github.com/kubaex/faces/blob/master/Manuel4.jpg?raw=true",
                          "https://github.com/kubaex/faces/blob/master/Ema1.jpg?raw=true",
                          "https://github.com/kubaex/faces/blob/master/Jakub1.jpg?raw=true"] 
    Npeople_db = len(list_names_db)
    utils.create_faceIdsList(faceIDslist)
    
    ### Add faces to the list ####
    for person_i in range(Npeople_db):
        image_url = list_images_url_db[person_i]
        faceids_list,fr_list = utils.get_faceids(image_url)
        
        faceId = faceids_list[0]
        
        name = list_names_db[person_i]
        list_face_ids_db.append(faceId)
        
        Npeople_in_picture = len(faceids_list)  ### ONLY 1
        for i in range(Npeople_in_picture):  ## We only expect one person from these pictures
            rectangle = "%i,%i,%i,%i"%(fr_list[i]["left"],fr_list[i]["top"],fr_list[i]["width"],fr_list[i]["height"])
            utils.add_face_to_faceIdsList(faceIDslist, image_url, rectangle = rectangle,userData = name)
            
    #    faceId_to_name_dict = dict();
    #    for person_i in range(Npeople_db):
    #        faceId_to_name_dict[list_face_ids_db[person_i]] = list_names_db[person_i]

### Get the faces in the DDBB
results_db = utils.get_facesId_in_faceIdsList(faceIDslist)
pf = results_db['persistedFaces']
Npeople_db = len(pf)
 
faceId_to_name_dict = dict();
name_to_faceId_dict = dict();
for person_i in range(Npeople_db):
    faceId_to_name_dict[pf[person_i]['persistedFaceId']] = pf[person_i]['userData']
    name_to_faceId_dict[pf[person_i]['userData']] = pf[person_i]['persistedFaceId']

if(0):
    ## Find similars:
    image_url = "https://github.com/kubaex/faces/blob/master/Manuel3.jpg?raw=true";
    faceids_list,fr_list = utils.get_faceids(image_url)
    Npeople = len(faceids_list)
    for i in range(Npeople):
        faceId = faceids_list[i]
        result_similarity = utils.find_similars(faceIDslist, faceId)
        
        print "For Face Id: %s"%faceId
        for similar in result_similarity:
            print faceId_to_name_dict[similar["persistedFaceId"]], similar["confidence"]


############## Do magic ##########3
npics = 3
if(1):
    images_urls = []
    for i in range(1,npics+1):
        images_urls.append("https://github.com/kubaex/faces/blob/master/Novo%i.jpg?raw=true"%i)
    
    n_ima = 0

    images_urls = ["https://github.com/manuwhs/Labyrinth/blob/master/internet_images/jury4.png?raw=true"]
    
    list_x = []
    list_y = []
    for image_url in images_urls:
        ## Get the emotions of the image
        ## So that we do not violate the number of requests
#        time.sleep(20)
        faceids_list,fr_list = utils.get_faceids(image_url)
        Npeople = len(faceids_list)
        if(Npeople == 0):
            continue
        
        ## Probability that the person is Manu
        person_detect = "Manu"
        person_detect_faceID = name_to_faceId_dict[person_detect]
        prob_list = []
        
        ## Match the faces in the image with the DDBB. 
        for i in range(Npeople):
            faceId = faceids_list[i]
            result_similarity = utils.find_similars(faceIDslist, faceId)
            
            print "For Face Id: %s"%faceId
            for similar in result_similarity:
#                print faceId_to_name_dict[similar["persistedFaceId"]], similar["confidence"]
                if (faceId_to_name_dict[similar["persistedFaceId"]] == person_detect):
                    prob_list.append(similar["confidence"])
                    
        # ----------------------
        fig = plt.figure()
#        ax = plt.subplot2grid((2,3),(1, 2))
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
    
        ax2 = plt.subplot2grid((1,1),(0, 0),colspan=1,rowspan=1)
        ax2.imshow(image, alpha=0.9)
        
        for j in range(len(fr_list)):
            face = fr_list[j]
            fr = face
            origin = (fr["left"], fr["top"])
            
            green = hex(int(prob_list[j] * 255)).split("x")[1]
            red = hex(int((1-prob_list[j]) * 255)).split("x")[1]
            
            if (len(green) == 1):
                green = "0"+ green
            if (len(red) == 1):
                red = "0"+ red        
            p = patches.Rectangle(origin, fr["width"], fr["height"], fill=False, linewidth=6, color="#"+red+green+"00")
            ax2.axes.add_patch(p)
            plt.text(origin[0], origin[1], "%s, %.2f"%(person_detect, prob_list[j]), fontsize=20, weight="bold", va="bottom")
        _ = plt.axis("off")
    
#        plt.subplots_adjust(hspace=0.35)
        
        file_dir = './images/%i.png'%n_ima
        
        fig.set_size_inches( 6*2, 4*2)
        fig.savefig(file_dir,
#                    bbox_inches = "tight",
                    dpi = 200
                    )
    
        plt.close(fig)
        n_ima+= 1;
            

create_video = 0
if(create_video):
    images_path = utils.get_allPaths("./images/")
    images_path.sort(cmp = utils.comparador_images_names)
    utils.create_video(images_path, output_file = "out.avi", fps = 2)
    
    
    


################ CREATE RANDOM LIST WITH FACES ####################
if(0):
    faceIDslist = "caca"
    utils.create_faceIdsList(faceIDslist)
    ### Add faces to the list ####
    image_url = "https://github.com/kubaex/faces/blob/master/Novo%i.jpg?raw=true"%1;
    faceids_list,fr_list = utils.get_faceids(image_url)
    Npeople = len(faceids_list)
    
    for i in range(Npeople):
        rectangle = "%i,%i,%i,%i"%(fr_list[i]["left"],fr_list[i]["top"],fr_list[i]["width"],fr_list[i]["height"])
        utils.add_face_to_faceIdsList(faceIDslist, image_url, rectangle = rectangle,userData = "Person %i"%(i+1))


    ## Find similars:
    image_url = "https://github.com/kubaex/faces/blob/master/Novo%i.jpg?raw=true"%5;
    faceids_list,fr_list = utils.get_faceids(image_url)
    
    for i in range(Npeople):
        faceId = faceids_list[i]
        print faceId
        result_similarity = utils.find_similars(faceIDslist, faceId)
        print result_similarity
