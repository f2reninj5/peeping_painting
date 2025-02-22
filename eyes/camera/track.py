import cv2
import numpy as np

def setup_camera():
    global face_cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    global camera
    camera = cv2.VideoCapture(0) # cv2.CAP_DSHOW for windows (fast)
    # print("Got Capture")

    camera.set(3, 1280)
    # print("Set Width")
    camera.set(4, 720)
    # print("Set Height")

    global eye_center_x
    global eye_center_y

    eye_center_x = 0
    eye_center_y = 0

def track():
    ret, frame = camera.read()
    if not ret:
        print("Failed to grab frame")
        return

    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(grey_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    closest_face = (np.int32(0), np.int32(0), np.int32(0), np.int32(0))

    for (x, y, w, h) in faces:
        if w > closest_face[2] or h > closest_face[3]:
            closest_face = (x, y, w, h)

    eye_center_x = np.int32(closest_face[0] + (0.5 * closest_face[2]))
    eye_center_y = np.int32(closest_face[1] + (0.4 * closest_face[3]))

    print("x =", eye_center_x, "; y =", eye_center_y)