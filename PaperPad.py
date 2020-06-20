import cv2
import numpy as np
import math

# Camera
camera = cv2.VideoCapture(0) # 0 for built-in webcam, 1 for external webcam
camera.set(10,200)


# Variables
frame_size_logged = False
points = []
uncovered_point = True
points_logged = False
TL = (0, 0)
TR = (0, 0)
BR = (0, 0)
BL = (0, 0)
quad_logged = False


def draw_circle(event,x,y,flags,param):
        global points, points_logged, quad_logged
        if event == cv2.EVENT_LBUTTONDBLCLK:
            uncovered_point = True
            for point in points:
                if len(points) > 0:
                    if abs(point[0]-x) <= 7 and abs(point[1]-y) <= 7:
                        uncovered_point = False
                        del points[points.index(point)]
                        points_logged = False
                        if len(points) <= 4:
                            quad_logged = False
                        break
            if uncovered_point:
                points.append((x, y))
                if len(points) <= 4:
                    quad_logged = False
                points_logged = False


while camera.isOpened():
    ret, frame = camera.read()
    frame = cv2.bilateralFilter(frame, 5, 50, 100) # smoothing filter

    if not frame_size_logged:
        print("frame size:", frame.shape[1], frame.shape[0])
        frame_size_logged = True

    cv2.setMouseCallback('original', draw_circle)
    for point in points:
        frame = cv2.circle(frame, point, 5, (255,0,0), -1)
    
    if len(points) >= 1:
        print(frame[points[0][1]-10][points[0][1]-10])

    if not points_logged:
        print("points:", points)
        points_logged = True

    cv2.imshow('original', frame)
    
    if len(points) >= 4:
        TL = points[0]
        TR = points[1]
        BR = points[2]
        BL = points[3]
    elif len(points) == 3:
        TL = points[0]
        TR = points[1]
        BR = points[2]
        BL = (0, 0)
    elif len(points) == 2:
        TL = points[0]
        TR = points[1]
        BR = (0, 0)
        BL = (0, 0)
    elif len(points) == 1:
        TL = points[0]
        TR = (0, 0)
        BR = (0, 0)
        BL = (0, 0)
    else:
        TL = (0, 0)
        TR = (0, 0)
        BR = (0, 0)
        BL = (0, 0)
    
    if not quad_logged:
        print("quad:", TL, TR, BR, BL)
        quad_logged = True
    
    if len(points) >= 4:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        bound = 100
        lower_bound = np.array([20, 30, 40])
        upper_bound = np.array([60, 90, 90])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        res = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow('mask', mask)
        cv2.imshow('res', res)

    # Keyboard press functions
    k = cv2.waitKey(20) & 0xFF
    if k == 27:  # press ESC to exit
        camera.release()
        cv2.destroyAllWindows()
        break