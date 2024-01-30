import cv2
import mediapipe as mp
import time
import handtrackingmodule as htm
import os
import numpy as np
from os import listdir
from os.path import isfile, join
#paht to the folder
pTime = 0
cTime = 0
images=[]   
target_size = (224, 224) 
# cap = cv2.VideoCapture(0)


mypath='Pictures'
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
images = np.empty(len(onlyfiles), dtype=object)
for n in range(0, len(onlyfiles)):
  images[n] = cv2.imread( join(mypath,onlyfiles[n]) )

        
  
detector = htm.handDetector()
tips=[8,12,16,20]
while True:
    # success, img = cap.read()
    images = detector.findHands(images)
    lmList = detector.findPosition(images)
    if len(lmList) != 0:
        fingers=[]
        
         # thumb    
        if lmList[4][1]<lmList[3][1]:
            fingers.append(0)
        else:
            fingers.append(1)
        
        #4 fingers
        for i in range (0,4):
            print(lmList[tips[i]])
            
            if lmList[tips[i]][2]>=lmList[tips[i]-1][2] and lmList[tips[i]][2]<=lmList[tips[i]-3][2]:
                fingers.append(0.5)
            elif lmList[tips[i]][2]<lmList[tips[i]-1][2]:
                fingers.append(1)
            else:
                fingers.append(0)
                
           

    
    print(fingers)    
            
            
            
    if lmList:
        break        
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(images, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
    cv2.imshow("Image", images)
    cv2.waitKey(1)