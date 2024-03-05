import cv2
import mediapipe as mp
import numpy as np
import os
import pandas as pd
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

# window_name = "window"
# For static images:
# # IMAGE_FILES = [r"M:\Robotics\underGrad Project\Software\Hand Tracing\Picture"]
# BG_COLOR = (192, 192, 192) # gray
# with mp_holistic.Holistic(
#     static_image_mode=True,
#     model_complexity=2,
#     enable_segmentation=True,
#     refine_face_landmarks=True) as holistic:
#     directory_path=r"M:\Robotics\underGrad Project\Software\Hand Tracing\Picture"
#     for filename in os.listdir(directory_path):
#         if filename.endswith('.jpg') or filename.endswith('.png'):
#                         # Read image from file
#             image = cv2.imread(os.path.join(directory_path, filename))
#     image_height, image_width, _ = image.shape
#     # Convert the BGR image to RGB before processing.
#     results = holistic.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

#     # if results.pose_landmarks:
#     # print(
#     #     f'Nose coordinates: ('
#     #     f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].x * image_width}, '
#     #     f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y * image_height})'
#     # )

#     # annotated_image = image.copy()
#     # Draw segmentation on the image.
#     # To improve segmentation around boundaries, consider applying a joint
#     # bilateral filter to "results.segmentation_mask" with "image".
#     condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
#     bg_image = np.zeros(image.shape, dtype=np.uint8)
#     bg_image[:] = BG_COLOR
#     annotated_image = np.where(condition, annotated_image, bg_image)
# #     # Draw pose, left and right hands, and face landmarks on the image.
# #     mp_drawing.draw_landmarks(
# #         annotated_image,
# #         results.face_landmarks,
# #         mp_holistic.FACEMESH_TESSELATION,
# #         landmark_drawing_spec=None,
# #         connection_drawing_spec=mp_drawing_styles
# #         .get_default_face_mesh_tesselation_style())
# #     mp_drawing.draw_landmarks(
# #         annotated_image,
# #         results.pose_landmarks,
# #         mp_holistic.POSE_CONNECTIONS,
# #         landmark_drawing_spec=mp_drawing_styles.
# #         get_default_pose_landmarks_style())
# #     cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
# #     # Plot pose world landmarks.
# #     mp_drawing.plot_landmarks(
# #         results.pose_world_landmarks, mp_holistic.POSE_CONNECTIONS)

# For webcam input:

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)
# cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = holistic.process(image)

    # Draw landmark annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.face_landmarks,
        mp_holistic.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles
        .get_default_face_mesh_contours_style())
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_holistic.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles
        .get_default_pose_landmarks_style())
    #right hand
    mp_drawing.draw_landmarks(
        image,
        results.right_hand_landmarks,
        mp_holistic.HAND_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles
        .get_default_hand_landmarks_style())
    #left hand
    mp_drawing.draw_landmarks(
        image,
        results.left_hand_landmarks,
        mp_holistic.HAND_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles
        .get_default_hand_landmarks_style())
    
    #find position
    llmList = []
    if results.left_hand_landmarks:
        myHand = results.left_hand_landmarks
        for id, lm in enumerate(myHand.landmark):
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            # print(id, cx, cy)
            llmList.append([id, cx, cy])
            # print("left hand: ",llmList)
    rlmList = []
    if results.right_hand_landmarks:
        myHand = results.right_hand_landmarks
        for id, lm in enumerate(myHand.landmark):
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            # print(id, cx, cy)
            rlmList.append([id, cx, cy])
            # print("Right hand: ",rlmList) 
    tips=[8,12,16,20]
    tips2=[1,5,13]        
    if len(rlmList) != 0:
            fingers=[]
                # thumb    
            if rlmList[4][1]<rlmList[3][1]:
                fingers.append(0)
            else:
                fingers.append(1)
            
            #4 fingers
            for i in range (0,4):
                # print(rlmList[tips[i]])
                
                if rlmList[tips[i]][2]>=rlmList[tips[i]-1][2] and rlmList[tips[i]][2]<=rlmList[tips[i]-3][2]:
                    fingers.append(0.5)
                elif rlmList[tips[i]][2]<rlmList[tips[i]-1][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            
            #wrist
            
            
            totalFingers=fingers.count(1)
                
            if rlmList[tips[0]][1]>=rlmList[tips2[1]][1] and rlmList[tips2[0]][1]<=rlmList[tips2[2]][1]:
                fingers.append(0.5)
            elif rlmList[tips[0]][1]<rlmList[tips[2]][1]:
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
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Holistic', cv2.flip(image, 1))
    cv2.waitKey(1)
# df= pd.DataFrame({'mot1': fingers[1], 'mot2': fingers[2], 'mot2': fingers[2],'mot3': fingers[3],'mot4': fingers[4],'mot5':fingers[0],'wrist':fingers[5]}, index=[text])
# df.to_csv("datasets2.csv",mode="a") 