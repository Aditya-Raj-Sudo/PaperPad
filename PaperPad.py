import cv2
import numpy as np
import math

# Camera
camera = cv2.VideoCapture(0) # 0 for built-in webcam, 1 for external webcam
camera.set(10,200)
fgbg = cv2.createBackgroundSubtractorMOG2(history=1)


# Variables
frame_size_logged = False
points = []
uncovered_point = True
points_logged = False
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

    # Keyboard press functions
    k = cv2.waitKey(20) & 0xFF
    if k == 27:  # press ESC to exit
        camera.release()
        cv2.destroyAllWindows()
        break