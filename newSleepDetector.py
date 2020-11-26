from imutils.video import FileVideoStream, VideoStream
from imutils import face_utils
from scipy.spatial import distance as dist
from threading import Thread
import playsound, argparse, imutils, time, dlib, cv2, serial
import numpy as np

s=serial.Serial('\dev\ttyAMA0')

def sound_alarm(path):
    playsound.playsound(path)
    s.write(b'ALERT!! Drowsiness Alert!')

def eye_aspect_ratio(eye):
    a=dist.euclidean(eye[1], eye[5])
    b=dist.euclidean(eye[2], eye[4])
    c=dist.euclidean(eye[0], eye[3])
    ear=(a+b)/(2.0*c)
    return ear

EYE_AR_THRESH=0.3
EYE_AR_CONSEC_FRAMES=3

k=0
alarmIsOn=False

print("*****************VCARE4U WELCOME'S YOU***********************")
print("Sleep Detetor Started")

detector=dlib.get_frontal_face_detector()
predictor=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

(lStart, lEnd)=face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd)=face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

fileStream=True
v=VideoStream(src=0).start()
fileStream=False
time.sleep(1.0)

while True:
    if fileStream and not v.more():
        break

    frame=v.read()
    frame=imutils.resize(frame, width=450)
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    rects=detector(gray, 0)

    for rect in rects:
        shape=predictor(gray, rect)
        shape=face_utils.shape_to_np(shape)

        leftEye=shape[lStart:lEnd]
        rightEye=shape[rStart:rEnd]
        leftEAR=eye_aspect_ratio(leftEye)
        rightEAR=eye_aspect_ratio(rightEye)
        ear=(leftEAR+rightEAR)/2.0
        leftEyeHull=cv2.convexHull(leftEye)
        rightEyeHull=cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        if (ear<EYE_AR_THRESH):
            k+=1

            if k>=EYE_AR_CONSEC_FRAMES:
                if not alarmIsOn:
                    alarmIsOn=True

                    if "alarm.wav"!="":
                        t=Thread(target=sound_alarm, args=("alarm.wav",))
                        t.deamon=True
                        t.start()

                cv2.putText(frame, "ALERT!! Drowsiness Alert!", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (176, 11, 33), 2)

        else:
            k=0
            alarmIsOn=False

        #cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (14, 176, 9), 2)

    cv2.imshow("Sleep Detetor By VCARE4U ", frame)
    key=cv2.waitKey(1) & 0xFF

    if(key == ord("q")):
        break

cv2.destroyAllWindows()
v.stop()
