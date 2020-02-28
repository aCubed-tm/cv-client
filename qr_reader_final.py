# import the necessary packages
from pyzbar import pyzbar
import cv2
import glob
import os
from os import path

import requests
import time


 
#---------------------------------------------------------------------Functies---------------------------------------------------------------------------------
def get_recent_file(path):
    #neem heet laatste bestand in map.
    files = glob.glob(path)
    recent_file = max(files, key=os.path.getctime)
    # print (recent_file)
    return recent_file
    
    
def get_oldest_file(path):
    #neem heet laatste bestand in map.
    files = glob.glob(path)
    recent_file = min(files, key=os.path.getctime)
    # print (recent_file)
    return recent_file

def barcodescanner(image, barcodes, camera):
    returnData = []
    
    # loop over the detected barcodes in the image
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw the
        # bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        print(camera + ":")
        
        print("h= " + str(h))
        print("x= " + str(x))
        print("y= " + str(y))
        print("w= " + str(w))

        # the barcode data is a bytes object so if we want to draw it on
        # our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
    
        try:
            #kijk of je een qr code hebt gevonden in de code.  
            barcodeData

            #bereken het midden van de qrcode en plaats deze in een dictionary. Key = qrcode data.
            pointx = (x + (w/2))
            pointy = (y + (h/2))

            print ("centerX= " + str(pointx))
            print ("centerY= " + str(pointx))

            # draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
 
            # print the barcode type and data to the terminal
            print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData) + '\n')

            #een dictionary om meerdere data te returnen en om gemakkelijk op te sturen met de
            #post request.
            # returnData = dict()
            # returnData['code'] = barcodeData
            # returnData['x'] = pointsx
            # returnData['y'] = pointsy

            
            returnData.append({"code":barcodeData,"x":pointx,"y":pointy, 'time':int(time.time()), 'camera':camera})
            

        except NameError:
            print("No QRcode found!\n")

    return returnData
    
def deleting_files(path_number):
    hetpad = path_number

    # print("deleting 5 oldest files on path " + hetpad)
    
    files = os.listdir(hetpad)

    delete_file = 0
    counter = 0 
    oldest_file_1 = get_oldest_file(hetpad  + '*')
    # print(hetpad)
    
    

    # print(str(len(files)))

    if(len(files) > 5):
        # print("in eerste if")
        while(counter < 2):
            # print("in while")
            if(path.exists(oldest_file_1)):
                os.system("sudo rm " + oldest_file_1)
                print(oldest_file_1 + " has been deleted!")
            # else:           
                # print(oldest_file_1 + " does not exist")
            counter = counter + 1  
            # print("counter= " + str(counter))
            # else:
                # os.error
        counter = 0    


#---------------------------------------------------------------Main programma-----------------------------------------------------------
# camera1 = 1 camera2 = 2 camera3 = 3

while(True):

    path_1 = '/home/pi/FTP/FTP/FTP_C1/C1_00626E6DF685/snap/'
    path_2 = '/home/pi/FTP/FTP/FTP_C2/C1_00626E6DF597/snap/'
    path_3 = '/home/pi/FTP/FTP/FTP_C3/C1_00626E6DF454/snap/'

    recent_file_1 = get_recent_file(path_1 + '*')
    recent_file_2 = get_recent_file(path_2 + '*')
    recent_file_3 = get_recent_file(path_3 + '*')
    print('\n') 

    # load the input image
    im_1 = cv2.imread(recent_file_1)
    im_2 = cv2.imread(recent_file_2)
    im_3= cv2.imread(recent_file_3)

    image_1 = cv2.resize(im_1, (1280, 720))
    image_2 = cv2.resize(im_2, (1280, 720))
    image_3 = cv2.resize(im_3, (1280, 720))
 
    # find the barcodes in the image and decode each of the barcodes
    barcodes_1 = pyzbar.decode(image_1)
    barcodes_2 = pyzbar.decode(image_2)
    barcodes_3 = pyzbar.decode(image_3)

    #functie voor het uitlezen van de qr code data.       
    data_C1 = barcodescanner(image_1, barcodes_1, "camera1")

    data_C2 = barcodescanner(image_2, barcodes_2, "camera2")

    data_C3 = barcodescanner(image_3, barcodes_3, "camera3")

    url = 'http://68.183.152.18:1337/v1/tracking/capture'
    test_url = 'https://enxfqeb2eyb2a.x.pipedream.net'
    
    print("send data")
    
    if(len(data_C1) == 0):
        print("no data in camera1")
    else:
            req_C1 = requests.post(test_url, json=data_C1)
        
        
    if(len(data_C2) == 0):
        print("no data in camera2")
    else:
        req_C2 = requests.post(test_url, json=data_C2)
        
        
    if(len(data_C3) == 0):
        print("no data in camera3")
    else:
        req_C3 = requests.post(test_url, json=data_C3)

    
    print("data is send")


    deleting_files(path_1)
    deleting_files(path_2)
    deleting_files(path_3)



    
  # #show the output image
  # cv2.imshow("Image", image)
  # cv2.waitKey(0)

 # delete all files from path varibale




