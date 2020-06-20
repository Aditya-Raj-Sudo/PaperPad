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
quad_logged = False


while camera.isOpened():
    ret, frame = camera.read()
    frame = cv2.bilateralFilter(frame, 5, 50, 100) # smoothing filter

    if not frame_size_logged:
        print("frame size:", frame.shape[1], frame.shape[0])
        frame_size_logged = True

    for point in points:
        frame = cv2.circle(frame, point, 5, (255,0,0), -1)

    cv2.imshow('original', frame)

    if len(points) >= 1:
        print(frame[points[0][1]-10][points[0][1]-10])

    if not points_logged:
        print("points:", points)
        points_logged = True

    # Keyboard press functions
    k = cv2.waitKey(20) & 0xFF
    if k == 27:  # press ESC to exit
        camera.release()
        cv2.destroyAllWindows()
        break