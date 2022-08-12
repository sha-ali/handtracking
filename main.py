import cv2
import time
import numpy as np
import handtrackingmodule as htm
import math
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wcam, hcam = 640, 480
frameR = 100
smothning = 5
swcam, shcam = pyautogui.size()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVole = volRange[0]
maxVole = volRange[1]

cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
pTime = 0

plocx, plocy = 0, 0
clocx, clocy = 0, 0

detector = htm.handDetectore(detection=0.7)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    fingers = []

    if lmList != None:
        fingers = detector.fingersup(lmList)

    # print(fingers)

    if fingers == [1, 1, 0, 0, 0]:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        # Hand range 50 - 300
        # volume Range -65 - 0

        vol = np.interp(length, [50, 300], [minVole, maxVole])
        # print(vol)

        volume.SetMasterVolumeLevel(vol, None)

    if lmList != None:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        cv2.rectangle(img, (frameR, frameR), (wcam - frameR, hcam - frameR), (255, 0, 255), 2)
        if fingers == [0, 1, 0, 0, 0]:
            print("mouse")

            x3 = np.interp(x1, (frameR, wcam - frameR), (0, swcam))
            y3 = np.interp(y1, (frameR, hcam - frameR), (0, shcam))
            clocx = plocx + (x3 - plocx) / smothning
            clocy = plocy + (y3 - plocy) / smothning

            pyautogui.moveTo(swcam - clocx, clocy)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocx, plocy = clocx, clocy
        if fingers == [0, 1, 1, 0, 0]:
            length, img, lineinfo = detector.finddistance(8, 12, img)

            if length < 42:
                cv2.circle(img, (lineinfo[4], lineinfo[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()
        # mousex = np.interp([100, 300])
        # pyautogui.moveTo(mousex, 75)

    if lmList != None:
        if fingers == [0,1,1,1,0]:
            pyautogui.scroll(-30)
            print("mouse scroll")

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)