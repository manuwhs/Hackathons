########### Python 2.7 #############
import httplib, urllib, base64, json
import imageio
import cv2

def get_emotions(image_url = ""):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '7cef923318814299bf3efb87d7ba809a',
    }
    
    params = urllib.urlencode({
        # Request parameters
        'returnFaceId': 'false',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,emotion'
    })
    
    
    body = json.dumps({
            "url": image_url
            })
    
    try:
        # /w/face/v1.0
        # westus.api.cognitive.microsoft.com
        # westcentralus.api.cognitive.microsoft.com
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        # "face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=false&returnFaceAttributes=age"
        # "/face/v1.0/detect?%s" % params
        
        print "Obtaining response..."
        conn.request("POST","/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        
        data = response.read()
    #    print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    
    #####
    ## Plot distribution of all the people
    ####
    
    print "Data loaded"
    list_emotions = []
    fr_list = []
    Npeople = len(json.loads(data))
    
    for i in range(Npeople):
        data_json = json.loads(data)[i]
        emotions = data_json["faceAttributes"]["emotion"]
        list_emotions.append(data_json["faceAttributes"]["emotion"])
        
        fr = data_json["faceRectangle"]
        fr_list.append(fr)
        
    return list_emotions,fr_list

def get_faceids(image_url = ""):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '7cef923318814299bf3efb87d7ba809a',
    }
    
    params = urllib.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender'
    })
    
    
    body = json.dumps({
            "url": image_url
            })
    
    try:
        # /w/face/v1.0
        # westus.api.cognitive.microsoft.com
        # westcentralus.api.cognitive.microsoft.com
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        # "face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=false&returnFaceAttributes=age"
        # "/face/v1.0/detect?%s" % params
        
        print "Obtaining response..."
        conn.request("POST","/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        
        data = response.read()
    #    print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    
    #####
    ## Plot distribution of all the people
    ####
    
    print "Data loaded"
    list_ids = []
    fr_list = []
    Npeople = len(json.loads(data))
    
    
    for i in range(Npeople):
        data_json = json.loads(data)[i]
        face_id = data_json["faceId"]
        list_ids.append(face_id)
        
        fr = data_json["faceRectangle"]
        fr_list.append(fr)
        
    return list_ids,fr_list


import os
def get_allPaths(rootFolder, fullpath = "yes"):
    ## This function finds all the files in a folder
    ## and its subfolders

    allPaths = []

    for dirName, subdirList, fileList in os.walk(rootFolder):  # FOR EVERY DOCUMENT
#       print "dirName"
       for fname in fileList:
            # Read the file
            path = dirName + '/' + fname;
            if (fullpath == "yes"):
                allPaths.append(os.path.abspath(path))
            else:
                allPaths.append(path)
    
    return allPaths

def comparador_images_names(x1,x2):
    number1 = int(x1.split("/")[-1].split(".")[0])
    number2 = int(x2.split("/")[-1].split(".")[0])
    

    if (number1 > number2):
        return 1
    else:
        return -1
    
def create_video(images_path, output_file = "out.avi", fps = 5):
    # Determine the width and height from the first image
    frame = cv2.imread(images_path[0])
    print frame
#    print frame
    cv2.imshow('video',frame)
    height, width, channels = frame.shape
    
    # Define the codec and create VideoWriter object
#    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
    #out = cv2.VideoWriter(output, fourcc, 20.0, (width, height))
    #out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640,480))
    out = cv2.VideoWriter(output_file,
                          cv2.VideoWriter_fourcc('M','J','P','G'), fps, (width,height))
    for im_path in images_path:
        frame = cv2.imread(im_path)
    #    print frame.shape
        out.write(frame) # Write out frame to video
    
        cv2.imshow('video',frame)
        if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
            break
    
    # Release everything if job is finished
    out.release()
    cv2.destroyAllWindows()
