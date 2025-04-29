import cv2
import numpy as np 
import time
import os
import HandTrackingModule as htm

brushThickness = 10
eraserThickness = 80

folderPath = "img_folder"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))

header = overlayList[0]
drawColor = (255, 255, 0)
mode = "selection"
lastMode = None
drawingRectangle = False
rectStart = (0, 0)
rectEnd = (0, 0)
rectangleInProgress = False

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.85)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8) 

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # print(lmList)
        
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        
        fingers = detector.fingersUp()

        if drawingRectangle and (fingers[1] == 0 and fingers[2] == 0):
            cv2.rectangle(imgCanvas, rectStart, (x1, y1), drawColor, brushThickness)
            drawingRectangle = False
            rectangleInProgress = False

        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            if lastMode != "selection":
                print("Selection Mode")
                lastMode = "selection"

            if y1 < 125:
                if 0 <= x1 <= 150:
                    header = overlayList[0]  # White
                    drawColor = (255, 255, 255)
                    mode = "draw"
                elif 210 <= x1 <= 370:
                    header = overlayList[1]  # Red
                    drawColor = (0, 0, 255)
                    mode = "draw"
                elif 440 <= x1 <= 600:
                    header = overlayList[2]  # Green
                    drawColor = (0, 255, 0)
                    mode = "draw"
                elif 670 <= x1 <= 830:
                    header = overlayList[3]  # Blue
                    drawColor = (255, 0, 0)
                    mode = "draw"
                elif 900 <= x1 <= 1040:
                    header = overlayList[4]  # Rectangle Tool
                    mode = "rectangle"
                elif 1130 <= x1 <= 1280:
                    header = overlayList[5]  # Eraser 
                    drawColor = (0, 0, 0)
                    mode = "draw"
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        if fingers[1] and not fingers[2]:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            if lastMode != "drawing":
                print("Drawing Mode")
                lastMode = "drawing"
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if mode == "draw":
                if drawColor == (0, 0, 0):  # Eraser
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)

                else:
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1,y1), drawColor, brushThickness)
                xp, yp = x1, y1

            elif mode == "rectangle":
                if not rectangleInProgress:
                    rectStart = (x1, y1)
                    rectangleInProgress = True
                    drawingRectangle = True
                else:
                    rectEnd = (x1, y1)
                    temp = img.copy()
                    cv2.rectangle(temp, rectStart, rectEnd, drawColor, brushThickness)
                    img = temp

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    img[0:125, 0:1280] = header
    img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1)

    key = cv2.waitKey(1)

    if key == ord('s'):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        cv2.imwrite(f'Drawing_{timestamp}.png', imgCanvas)
        print(f"Canvas saved as Drawing_{timestamp}.png")

    elif key == ord('c'):
        imgCanvas = np.zeros((720, 1280, 3), np.uint8)
        print("Canvas cleared.")

