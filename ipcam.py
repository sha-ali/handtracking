import cv2
import pyautogui
import time


wcam, hcam = 640, 480
frameR = 100
smothning = 5
swcam, shcam = pyautogui.size()

cap = cv2.VideoCapture('http://log:log@192.168.200.89:8080/video')
cap.set(3, wcam)
cap.set(4, hcam)

while True:
    success, img = cap.read()


    cv2.imshow("Img", img)
    cv2.waitKey(1)

