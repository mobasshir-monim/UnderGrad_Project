import cv2
import time
import os
import handtrackingmodule as htm

wCam,hCam=960,540

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

folderPath="Pictures"
myList=os.listdir(folderPath)
print(myList)
overlayList=[]
for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

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
        
        #thumb
        if lmList[tipIds[0]][1]<lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # other 4 fingers

        for id in range(1,5):
            if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

       # print(fingers)        
        totalFingers=fingers.count(1)
        print(totalFingers)
        h,w,c=overlayList[totalFingers-1].shape
        img[0:h, 0:w]=overlayList[totalFingers-1]


    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)