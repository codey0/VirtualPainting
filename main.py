import cv2
import numpy as np
frameWidth = 640
frameHeight = 480
capture = cv2.VideoCapture(0)
capture.set(3, frameWidth)
capture.set(4, frameHeight)
capture.set(10, 150)

# put the 6 values below in the order: hue minimum, saturation minimum, value minimum,
#                                      hue maximum, saturation maximum, value maximum
myColors = [[5, 107, 0, 19, 160, 255],  # orange
           [133, 56, 0, 170, 156, 255],  # purple
           [27, 78, 187, 42, 145, 255],  # yellow   ->  highlighter
           [0, 92, 134, 10, 137, 255],  # red
           [57, 69, 0, 100, 255, 255]]  # green  (57, 76, 0, 100, 255, 255) or (57, 69, 97, 88, 157, 255)
           # [90, 48, 0, 118, 255, 255]]  # blue
myColorValues = [[51, 153, 255],  # write in format of BGR, not RGB
                 [255, 0, 255],
                 [0, 255, 255],
                 [0, 0, 255],
                 [0, 255, 0]]
                 # [255, 0, 0]]

myPoints = []  # x, y, colorID

def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    counter = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 10, myColorValues[counter], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, counter])
        counter += 1
        # cv2.imshow(str(color[0]), mask)
    return newPoints

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # retrieves extreme outer contours
    x, y, width, height = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            perimeter = cv2.arcLength(cnt, True)
            approximation = cv2.approxPolyDP(cnt, 0.02*perimeter, True)
            x, y, width, height = cv2.boundingRect(approximation)
    return x+width//2, y

def drawOnCanvas(myPointsm, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)

while True:
    success, img = capture.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)

    cv2.imshow("Video", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'): # adds delays and looks for key press 'q' to break the loop
        break
