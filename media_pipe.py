import cv2
import numpy as np
import mediapipe as mp
#import matplotlib.pyplot as plt

print('Launching main')
mp_drawing = mp.solutions.drawing_utils

mp_pose = mp.solutions.pose

def gstreamer_pipeline (capture_width=3820, capture_height=2464, display_width=816, 
     display_height=616, framerate=21, flip_method=0) :   
     return ('nvarguscamerasrc ! ' 
    'video/x-raw(memory:NVMM), '
    'width=(int)%d, height=(int)%d, '
    'format=(string)NV12, framerate=(fraction)%d/1 ! '
    'nvvidconv flip-method=%d ! '
    'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
    'videoconvert ! '
    'video/x-raw, format=(string)BGR ! appsink'  % (capture_width,capture_height,framerate,flip_method,display_width,display_height))


# For webcam input:
i = 0
cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
ys_l_shoulder = []
ys_r_shoulder = []
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
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
    results = pose.process(image)

    # Draw the pose annotation on the image.
    #image.flags.writeable = True
    #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    #mp_drawing.draw_landmarks(
    #    image,
    #    results.pose_landmarks,
    #    mp_pose.POSE_CONNECTIONS)
        
    # Flip the image horizontally for a selfie-view display.
    #cv2.imshow('MediaPipe Pose', image) #cv2.flip(image, 1))
    
    
    if results.pose_landmarks != None :
        print('frame \n')
        
        landmarks = [(data_point.x, data_point.y, data_point.z) for data_point in results.pose_landmarks.landmark]
        #y is important for distance
        #position x, y and z: Real-world 3D coordinates in meters with the origin at the center between hips.
        ys_l_shoulder.append(landmarks[12][1])
        ys_r_shoulder.append(landmarks[11][1])
        ly = landmarks[12][1]
        ry = landmarks[11][1]
        print('y = ', np.mean(ly, ry))


   
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
