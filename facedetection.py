import face_recognition
import cv2
import numpy as np
import pyautogui

video_captured = cv2.VideoCapture(0)
wcam, hcam = 640, 480
frameR = 100
smothning = 5
swcam, shcam = pyautogui.size()
#'http://log:log@192.168.200.89:8080/video'
my_image = face_recognition.load_image_file("sha.jpg")
face_encoding = face_recognition.face_encodings(my_image)[0]

kn_face = [
    face_encoding
]
kn_fname = [
    "SHABIR"
]

while True:
    ret,frame = video_captured(0)
    frame.set(3, wcam)
    frame.set(4, hcam)

    rgb_frame = frame[:, :, ::-1]

    face_loc = face_recognition.face_locations(rgb_frame)
    face_encoding = face_recognition.face_encodings(rgb_frame, face_loc)

    for (top, right, left, bottom), face_encoding in zip(face_loc, face_encoding):
        matches = face_recognition.compare_faces(kn_face, face_encoding)

        name = "unknown"

        face_dis = face_recognition.face_distance(kn_face, face_encoding)
        best_match = np.argmin(face_dis)
        if matches[best_match]:
            name = kn_fname[best_match]

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_ITALIC
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video_captured.release()
cv2.destroyAllWindows()