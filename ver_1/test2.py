# ver 2. taking live video capture

import cv2
import numpy as np

cam = cv2.VideoCapture(0)
while True:
    _, frame = cam.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # converting bgr to hsv

    # black
    low_black = np.array([0,0,0])
    high_black = np.array([14,255,111])
    black_mask =  cv2.inRange(hsv_frame, low_black, high_black)
    # black  = cv2.bitwise_and(frame, frame, mask = black_mask)
    black = cv2.bitwise_not(black_mask)

    # brown
    low_brown = np.array([5,220,24])
    high_brown = np.array([10,255,101])
    brown_mask = cv2.inRange(hsv_frame, low_brown, high_brown)
    brown = cv2.bitwise_and(frame, frame, mask = brown_mask)

    # red
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask =  cv2.inRange(hsv_frame, low_red, high_red)
    red  = cv2.bitwise_and(frame, frame, mask = red_mask)

    # orange
    low_orange = np.array([4,31,198])
    high_orange = np.array([10,255,255])
    orange_mask =  cv2.inRange(hsv_frame, low_orange, high_orange)
    orange  = cv2.bitwise_and(frame, frame, mask = orange_mask)

    # yellow
    low_yellow = np.array([21, 95, 42])
    high_yellow = np.array([28,255,241])
    yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)
    yellow = cv2.bitwise_and(frame, frame, mask = yellow_mask)

    # green
    low_green = np.array([54, 41, 0])
    high_green = np.array([77, 255, 157])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green = cv2.bitwise_and(frame, frame, mask = green_mask)

    # blue
    low_blue = np.array([94, 80, 2])
    high_blue = np.array([126, 255, 255])
    blue_mask =  cv2.inRange(hsv_frame, low_blue, high_blue)
    blue  = cv2.bitwise_and(frame, frame, mask = blue_mask)

    # violet
    low_violet = np.array([121, 64, 65])
    high_violet = np.array([169, 202, 255])
    violet_mask =  cv2.inRange(hsv_frame, low_violet, high_violet)
    violet  = cv2.bitwise_and(frame, frame, mask = violet_mask)

    # gray

    # white
    low_white = np.array([8, 71, 139])
    high_white = np.array([22, 108, 242])
    white_mask =  cv2.inRange(hsv_frame, low_white, high_white)
    white  = cv2.bitwise_and(frame, frame, mask = white_mask)

    cv2.imshow("frame", frame)
    # cv2.imshow("black mask", black)
    cv2.imshow("brown mask", brown)
    # cv2.imshow("red mask", red)
    # cv2.imshow("orange mask", orange)
    # cv2.imshow("yellow mask", yellow)
    # cv2.imshow("green mask", green)
    # cv2.imshow("blue mask", blue)
    # cv2.imshow("violet mask", violet)
    # cv2.imshow("white mask", white)

    key = cv2.waitKey(1)
    if key == 27: # esc key
        break