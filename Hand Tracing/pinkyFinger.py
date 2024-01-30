import glob
import cv2
import time
import os
import handtrackingmodule as htm

wCam,hCam=960,540

# cap=cv2.VideoCapture(0)
cap= cv2.imread("Pictures/55.png")

cap.set(3,wCam)
cap.set(4,hCam)

# folderPath="Pictures"
# myList=os.listdir(folderPath)
# print(myList)


pTime=0


detector=htm.handDetector(detectionCon=0.75)
tipIds=[4,8,12,16,20]
while True: 
    success,img=cap.read()
    img,handType=detector.findHands(img)
    lmList=detector.findPosition(img, draw=False)
    
    if len(lmList)!=0:
        fingers=[]
        print(handType)
        
        
        #pinkyfinger
        if lmList[20][2]>=lmList[19][2] and lmList[20][2]<=lmList[17][2]:
            fingers.append(0.5)
        elif lmList[20][2]<lmList[19][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    

        print(fingers)        
        # totalFingers=fingers.count(1)
        # print(totalFingers)
        


    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)