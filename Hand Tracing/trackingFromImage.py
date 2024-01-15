import cv2
import mediapipe as mp
import time
import handtrackingmodule as htm

pTime = 0
cTime = 0
# cap = cv2.VideoCapture(0)
img= cv2.imread("Pictures/55.png")
detector = htm.handDetector()
tips=[4,8,12,16,20]
while True:
    # success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        for i in range (0,4):
            print(lmList[tips[i]])
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)