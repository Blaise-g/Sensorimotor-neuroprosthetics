import os
import PySimpleGUI as sg
from PIL import Image
import cv2
import io
import numpy as np
import mediapipe as mp
import matplotlib.pyplot as plt
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# For static images:
IMAGE_FILES = []
BG_COLOR = (192, 192, 192)

def draw(robot, direction) :
    if 'front_t' in direction :
        pt1 = (262, 0)
        pt2 = (162, 100)
        pt3 = (362, 100)
        cv2.circle(robot, pt1, 2, (0,0,255), -1)
        cv2.circle(robot, pt2, 2, (0,0,255), -1)
        cv2.circle(robot, pt3, 2, (0,0,255), -1)
        triangle_cnt = np.array( [pt1, pt2, pt3] )
        cv2.drawContours(robot, [triangle_cnt], 0, (0,255,0), -1)
    if 'back_t' in direction :
        pt1 = (262, 638)
        pt2 = (162, 538)
        pt3 = (362, 538)
        cv2.circle(robot, pt1, 2, (0,0,255), -1)
        cv2.circle(robot, pt2, 2, (0,0,255), -1)
        cv2.circle(robot, pt3, 2, (0,0,255), -1)
        triangle_cnt = np.array( [pt1, pt2, pt3] )
        cv2.drawContours(robot, [triangle_cnt], 0, (0,255,0), -1)
    if 'left_t' in direction :
        pt1 = (514, 319)
        pt2 = (414, 219)
        pt3 = (414, 419)
        cv2.circle(robot, pt1, 2, (0,0,255), -1)
        cv2.circle(robot, pt2, 2, (0,0,255), -1)
        cv2.circle(robot, pt3, 2, (0,0,255), -1)
        triangle_cnt = np.array( [pt1, pt2, pt3] )
        cv2.drawContours(robot, [triangle_cnt], 0, (0,255,0), -1)
    if 'right_t' in direction :
        pt1 = (0, 319)
        pt2 = (100, 219)
        pt3 = (100, 419)
        cv2.circle(robot, pt1, 2, (0,0,255), -1)
        cv2.circle(robot, pt2, 2, (0,0,255), -1)
        cv2.circle(robot, pt3, 2, (0,0,255), -1)
        triangle_cnt = np.array( [pt1, pt2, pt3] )
        cv2.drawContours(robot, [triangle_cnt], 0, (0,255,0), -1)
    return robot

def run(image, pose, i, robot):
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image2 = image.copy()
    black = np.where((image[:,:,0]>=0) & (image[:,:,1]>=0) & (image[:,:,2]>=0))
    image2[black]=(0,0,0)

    if results.pose_landmarks!=None :
        direction = []
        #print(results.pose_landmarkss)
        landmarks = [(data_point.x, data_point.y, data_point.z) for data_point in results.pose_landmarks.landmark]
        #print(landmarks[11][1],landmarks[12][1])
        sum_x = landmarks[11][0]+landmarks[12][0]
        mean_y = np.mean(landmarks[11][1]+landmarks[12][1])
        if mean_y > 0.45 :
            direction.append("front_t")
            #print("FRONT")
        elif mean_y < 0.1 :
             direction.append("back_t")
             #print("BACK")
        if sum_x > 1.25 :
            direction.append("left_t")
            #print("LEFT")
        elif sum_x < 0.1 :
            direction.append("right_t")
            #print("RIGHT")
        #y is important for distance
        #position x, y and z: Real-world 3D coordinates in meters with the origin at the center between hips.
        #ys_l_shoulder.append(landmarks[12][1])
        #ys_r_shoulder.append(landmarks[11][1])
        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry(440, 0, 800, 808)
        #if landmarks[12][0] < landmarks[11][0] :
            #print("turn")
        plt.scatter(i, np.mean([landmarks[11][1],landmarks[12][1]]), c='red')
        #else : plt.scatter(i, np.mean([landmarks[11][1],landmarks[12][1]]), c='red')
        plt.xlabel('Timepoint')
        plt.ylabel('Relative distance from camera')
        #plt.scatter(i, landmarks[11][1], c='blue')
        plt.pause(0.00000000000000005)
        #plot = np.mean([landmarks[11][1],landmarks[12][1]])
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    mp_drawing.draw_landmarks(
        image2,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the image horizontally for a selfie-view display.
    #plt.plot(ys_l_shoulder)
    #plt.plot(ys_r_shoulder)
    #plt.savefig('/home/james/neuro/Data/plot.mp4')
    return image, image2, direction

def main():
    keepgoing = True
    while keepgoing:
        robot_filename = "/home/james/Downloads/Webp.net-resizeimage.png"
        file_list_column = [
            [
                sg.Text("Video Folder"),
                sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
                sg.FolderBrowse(),
            ],
            [
                sg.Listbox(
                    values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
                )
            ],
        ]

        video_viewer_column = [
            [sg.Text("Choose a video from list on left:")],
            [sg.Text(size=(40, 1), key="-TOUT-")],
            [sg.Image(size=(300,300), filename = robot_filename)]
        ]
        layout = [
            [
                sg.Column(file_list_column),
                sg.VSeperator(),
                sg.Column(video_viewer_column),
            ]
        ]
        window1 = sg.Window("Video Analyzer", layout)
        while True:
            event, values = window1.read()
            if event == sg.WIN_CLOSED:
                keepgoing = False
                break
            elif event == "Exit" :
                keepgoing = False
                break
            elif event == "-FOLDER-":
                folder = values["-FOLDER-"]
                try:
                    # Get list of files in folder
                    file_list = os.listdir(folder)
                except:
                    file_list = []

                fnames = [
                    f
                    for f in file_list
                    if os.path.isfile(os.path.join(folder, f))
                    and f.lower().endswith((".mp4"))
                ]
                window1["-FILE LIST-"].update(fnames)
            # Here only show files -> we want it to analyze

            elif event == "-FILE LIST-":  # A file was chosen from the listbox
                try:
                    filename = os.path.join(
                        values["-FOLDER-"], values["-FILE LIST-"][0]
                    )
                    layout = [[sg.Text('Do you want to run: '+filename, size=(124, 1), justification='center', font=("Helvetica", 24), relief=sg.RELIEF_RIDGE, key='-OUTPUT-')],
                        [sg.Button('Yes', size=(124, 1)), sg.Button('No', size=(124, 1))],
                        [sg.Image(size=(1800,200), filename = "/home/james/Downloads/Erlebniss_HindernisfreieWege_GrosseSuoneVex (1) (1).png")]]
                    window2 = sg.Window('Confirm', layout, layout,size=(1782, 300), location=(0,1000))
                    event, values = window2.read()
                    if event == sg.WIN_CLOSED :
                        window2.close()
                        break
                    elif event == 'No' :
                        window2.close()
                    elif event == 'Yes':
                        i=0
                        cap = cv2.VideoCapture(filename)
                        # vlc : 640 × 360, 5,00 frames per second -> CONVERTIR
                        #cap.set(cv2.CAP_PROP_FPS, 5)
                        with mp_pose.Pose(
                            min_detection_confidence=0.5,
                            min_tracking_confidence=0.5) as pose:
                            while cap.isOpened():
                                robot = cv2.imread(robot_filename)
                                robot = cv2.resize(robot, [620, 762])
                                success, image = cap.read()
                                if not success:
                                  print("Ignoring empty camera frame.")
                                  # If loading a video, use 'break' instead of 'continue'.
                                  cap.release()
                                  break
                                else :
                                    img, img2, direction = run(image, pose, i, robot)
                                    i+=1
                                    winname = "MediaPipe Pose"
                                    cv2.namedWindow(winname)
                                    cv2.moveWindow(winname, 0,0)
                                    cv2.resizeWindow(winname, 720,1280)
                                    cv2.imshow(winname, cv2.flip(img, 1))
                                    winname2 = "Pose only"
                                    cv2.namedWindow(winname2)
                                    #cv2.moveWindow(winname2, 1040, 0)
                                    cv2.moveWindow(winname2, 0, 400)
                                    cv2.resizeWindow(winname2, 360,640)
                                    cv2.imshow(winname2, cv2.flip(img2, 1))
                                    winname3 = "Robot"
                                    cv2.namedWindow(winname3)
                                    cv2.moveWindow(winname3, 1240, 0)
                                    if direction :
                                        robot_t = draw(robot, direction)
                                        cv2.imshow(winname3, cv2.flip(robot_t, 1))
                                    else : cv2.imshow(winname3, cv2.flip(robot, 1))
                                    if cv2.waitKey(5) & 0xFF == 27:
                                        cap.release()
                                        break
                    window2.close()
                    cv2.destroyAllWindows()
                    plt.close()
                except:
                    pass
        window1.close()
    window1.close()

if __name__ == '__main__':

    main()
