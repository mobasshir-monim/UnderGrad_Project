import cv2
import mediapipe as mp
import time
import handtrackingmodule as htm
import poseModule as pm
import pandas as pd
import os

pTime = 0
cTime = 0
# cap = cv2.VideoCapture(0)
directory_path=r"M:\Robotics\underGrad Project\Software\Hand Tracing\Pictures"
for filename in os.listdir(directory_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):
                    # Read image from file
        image = cv2.imread(os.path.join(directory_path, filename))
        # image=cv2.imread("Pictures/1.png")
    detector = htm.handDetector()
    tips=[8,12,16,20]
    tips2=[1,5,13]
    while True:
        # success, img = cap.read()
        img = detector.findHands(image)
        lmList = detector.findPosition(image)
        print(lmList)
        if len(lmList) != 0:
            fingers=[]
                # thumb    
            if lmList[4][1]<lmList[3][1]:
                fingers.append(0)
            else:
                fingers.append(1)
            
            #4 fingers
            for i in range (0,4):
                # print(lmList[tips[i]])
                
                if lmList[tips[i]][2]>=lmList[tips[i]-1][2] and lmList[tips[i]][2]<=lmList[tips[i]-3][2]:
                    fingers.append(0.5)
                elif lmList[tips[i]][2]<lmList[tips[i]-1][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            
            #wrist
            
            
            totalFingers=fingers.count(1)
                
            if lmList[tips[0]][1]>=lmList[tips2[1]][1] and lmList[tips2[0]][1]<=lmList[tips2[2]][1]:
                fingers.append(0.5)
            elif lmList[tips[0]][1]<lmList[tips[2]][1]:
                fingers.append(1)
            else:
                fingers.append(0)       
            
        print(fingers)    
        print(totalFingers)      
        text=[]  
        if totalFingers==1:
            text="one"
        elif totalFingers==2:
            text="two"
        elif totalFingers==3:
            text="three"
        elif totalFingers==4:
            text="four"      
        elif totalFingers==5:
            text="five"
        else:
            text="no finger shown"
        print(text)

        if lmList:
            break       






    # cTime = time.time()
    # fps = 1 / (cTime - pTime)
    # pTime = cTime
    # cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
    #                 (255, 0, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

    # print(fingers[1])
    df = pd.DataFrame({'mot1': fingers[1], 'mot2': fingers[2], 'mot2': fingers[2],'mot3': fingers[3],'mot4': fingers[4],'mot5':fingers[0],'wrist':fingers[5]}, index=[text])
    df.to_csv("datasets.csv",mode="a")    

    print(df) 
        