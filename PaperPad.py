import cv2
import numpy as np
import math
import mousecontrol

# Camera
camera = cv2.VideoCapture(0) # 0 for built-in webcam, 1 for external webcam
camera.set(10,200)
fgbg = cv2.createBackgroundSubtractorMOG2(history=1)


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
last_thumb_point = (9999, 9999)
thumb_pos_locked = False


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


def round_up_to_even(num):
    return math.ceil(num / 2.0) * 2


while camera.isOpened():
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.bilateralFilter(frame, 5, 50, 100) # smoothing filter

    if not frame_size_logged:
        print("frame size:", frame.shape[1], frame.shape[0])
        frame_size_logged = True

    cv2.setMouseCallback('original', draw_circle)
    for point in points:
        cv2.circle(frame, point, 5, (255,0,0), -1)
    
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

    fgmask = fgbg.apply(frame)

    try:
        kernel = np.ones((3,3),np.uint8)

        # define roi which is a small square on screen
        roi = frame[100:500, 100:500]
        cv2.rectangle(frame,(100,100),(500,500),(0,255,0),0)
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # range of the skin colour is defined
        lower_skin = np.array([0,48,80], dtype=np.uint8)
        upper_skin = np.array([20,255,255], dtype=np.uint8)

        # extract skin colur image
        mask = cv2.inRange(hsv, lower_skin, upper_skin)

        # dilate the hand to fill dark spots in it
        mask = cv2.dilate(mask,kernel,iterations = 4)

        # blur image
        mask = cv2.GaussianBlur(mask,(5,5),100)

        # find contours
        contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        # find contour of max area (hand)
        cnt = max(contours, key = lambda x: cv2.contourArea(x))

        # approx the contour
        epsilon = 0.0005*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)

        # make convex hull around hand
        hull = cv2.convexHull(cnt)

        # define area of hull and area of hand
        areahull = cv2.contourArea(hull)
        areacnt = cv2.contourArea(cnt)

        # find the percentage of area not covered by hand in convex hull
        arearatio = ((areahull-areacnt)/areacnt)*100

        # find the defects in convex hull with respect to hand
        hull = cv2.convexHull(approx, returnPoints=False)
        defects = cv2.convexityDefects(approx, hull)

        # no. of defects
        num_defects = 0

        # thumb variable
        thumb_point = (9999, 9999)

        # code for finding no. of defects due to fingers
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(approx[s][0])
            end = tuple(approx[e][0])
            far = tuple(approx[f][0])
            pt = (100,180)

            # find length of all sides of triangle
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            s = (a+b+c)/2
            ar = math.sqrt(s*(s-a)*(s-b)*(s-c))

            # distance between point and convex hull
            d = (2*ar)/a

            # apply cosine law
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57

            # ignore angles > 90 and ignore points very close to convex hull (they generally come due to noise)
            if angle <= 90 and d > 30:
                num_defects += 1
                # cv2.circle(roi, far, 3, [255,0,0], -1)

            # draw lines around hand
            cv2.line(roi, start, end, [0,255,0], 2)

            # identify thumb point
            x_trans = 73
            y_trans = 103
            if start[0] < thumb_point[0]:
                if thumb_pos_locked:
                    if math.sqrt(abs(start[0]+x_trans-thumb_point[0])**2 + abs(start[1]+y_trans-thumb_point[1])**2) < 20:
                        thumb_point = (round_up_to_even(start[0]+x_trans), round_up_to_even(start[1]+y_trans))
                    else:
                        thumb_point = last_thumb_point
                else:
                    thumb_point = (round_up_to_even(start[0]+x_trans), round_up_to_even(start[1]+y_trans))
            if end[0] < thumb_point[0]:
                if thumb_pos_locked:
                    if math.sqrt(abs(end[0]+x_trans-thumb_point[0])**2 + abs(end[1]+y_trans-thumb_point[1])**2) < 20:
                        thumb_point = (round_up_to_even(end[0]+x_trans), round_up_to_even(end[1]+y_trans))
                    else:
                        thumb_point = last_thumb_point
                else:
                    thumb_point = (round_up_to_even(end[0]+x_trans), round_up_to_even(end[1]+y_trans))
        
        last_thumb_point = thumb_point
        cv2.circle(frame, thumb_point, 5, (0,0,255), -1)
        mousecontrol.mouse_move(int(thumb_point[0]), frame.shape[0]-int(thumb_point[1]))

        num_defects += 1

        cv2.imshow('frame', frame)

    except Exception as e:
        print("Exception:", e)

    # Keyboard press functions
    k = cv2.waitKey(20) & 0xFF
    if k == 27:  # press ESC to exit
        camera.release()
        cv2.destroyAllWindows()
        break
    elif k == ord('a'):
        if not thumb_pos_locked:
            thumb_pos_locked = True
        else:
            thumb_pos_locked = False