import cv2
import numpy as np
import math

# Camera
camera = cv2.VideoCapture(0) # 0 for built-in webcam, 1 for external webcam
camera.set(10,200)

while camera.isOpened():
    ret, frame = camera.read()
    frame = cv2.bilateralFilter(frame, 5, 50, 100)

    cv2.imshow("window", frame)

    k = cv2.waitKey(20) & 0xFF

    if k == 27:
        camera.release()
        cv2.destroyAllWindows()
        break