# -*- coding: utf-8 -*-
import numpy as np

import time

import cv2

import glob

import os

from fps import FPS
from webcam import WebcamVideoStream

def convexHullIsPointingUp(hull):
    x, y, w, h = cv2.boundingRect(hull)


    aspectRatio = float(w) / h

    if aspectRatio > 0.8:

        return False


    listOfPointsAboveCenter = []

    listOfPointsBelowCenter = []

    intYcenter = y + h / 2

# step through all points in convex hull

    for point in hull:

# and add each point to

# list of points above or below vertical center as applicable

        if point[0][1] < intYcenter:

            listOfPointsAboveCenter.append(point)


        if point[0][1] >= intYcenter:


            return False


    listOfPointsAboveCenter = []

    listOfPointsBelowCenter = []

    intYcenter = y + h / 2

# step through all points in convex hull

    for point in hull:

# and add each point to

# list of points above or below vertical center as applicable

        if point[0][1] < intYcenter:

            listOfPointsAboveCenter.append(point)


        if point[0][1] >= intYcenter:

            listOfPointsBelowCenter.append(point)
            listOfPointsBelowCenter.append(point)


    intLeftMostPointBelowCenter = listOfPointsBelowCenter[0][0][0]

    intRightMostPointBelowCenter = listOfPointsBelowCenter[0][0][0]


# determine left most point below center

    for point in listOfPointsBelowCenter:

        if point[0][0] < intLeftMostPointBelowCenter:

            intLeftMostPointBelowCenter = point[0][0]


# determine right most point below center

    for point in listOfPointsBelowCenter:

        if point[0][0] >= intRightMostPointBelowCenter:

            intRightMostPointBelowCenter = point[0][0]

# step through all points above center

    for point in listOfPointsAboveCenter:

        if point[0][0] < intLeftMostPointBelowCenter or \
            point[0][0] > intRightMostPointBelowCenter:

            return False

# if we get here, shape has passed pointing up check

    return True



def testcone(img, file='', stream=False):

    print('Image shape ', img.shape)

# convert to HSV color space, this will produce better color filtering

    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


# Threshold on low range of HSV red

    low_redl = np.array([0, 135, 135])

    low_redh = np.array([15, 255, 255])

    imgThreshLow = cv2.inRange(imgHSV, low_redl, low_redh)


# threshold on high range of HSV red

    high_redl = np.array([159, 135, 135])

    high_redh = np.array([179, 255, 255])

    imgThreshHigh = cv2.inRange(imgHSV, high_redl, high_redh)


# combine low range red thresh and high range red thresh

    imgThresh = cv2.bitwise_or(imgThreshLow, imgThreshHigh)


# clone/copy thresh image before smoothing

    imgThreshSmoothed = imgThresh.copy()

# open image (erode, then dilate)

    kernel = np.ones((3, 3), np.uint8)

    imgThreshSmoothed = cv2.erode(imgThresh, kernel, iterations=1)

    imgThreshSmoothed = cv2.dilate(imgThreshSmoothed, kernel, iterations=1)
# Gaussian blur

    imgThreshSmoothed = cv2.GaussianBlur(imgThreshSmoothed, (5, 5), 0)


    imgCanny = cv2.Canny(imgThreshSmoothed, 160, 80)

    contours = None


    image, contours, hierarchy = cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


    listOfContours = []

    if len(contours) != 0:

        for cnt in contours:

            pol = cv2.approxPolyDP(cnt, 6.7, True)

            listOfContours.append(pol)


# print file + ' listOfContours ' , len(listOfContours)


    listOfCones = []

    for contour in listOfContours:

        hull = cv2.convexHull(contour)

# print 'convexHull',len(temp)

        if (len(hull) >= 3 and len(hull) <= 10):

            imghull2 = cv2.drawContours(img.copy(), hull, 1, (0, 0, 255), 5)

        else:

            continue


        if convexHullIsPointingUp(hull):

            listOfCones.append(hull)


# print(listOfCones)


    orig = (img.shape[1] / 2, img.shape[0] - 1)


    for cone in listOfCones:

        x = 0

        y = 0

        for side in cone:

            x += side[0][0]

            y += side[0][1]

        x = x / len(cone)

        y = y / len(cone)

        print('Centroid for cone: ', x, ' - ', y)

        cv2.circle(img, (x, y), 4, (0, 255, 0), 2)

        cv2.line(img, orig, (x, y), (0, 255, 0), 2)


    imghull = None


    imghull = cv2.drawContours(img, listOfCones, -1, (0, 255, 0), 3)


    if not stream:

        cv2.imshow('hull ', imghull)

    else:

        cv2.imwrite('processed/' + str(time.time()) + '.jpg', imghull)


    print('Found ', len(listOfCones), ' Cones')


    return


def from_files():


# get the files

    files = glob.glob(os.path.join('.', 'images', '*.jpg'))


    for file in files:

        print('Processing file ' + file)

        testcone(cv2.imread(file, -1), file=file)

        print('Done Processing file ' + file)

        cv2.waitKey(0)

        cv2.destroyAllWindows()


def from_stream():

    fps = FPS().start()
    cam = WebcamVideoStream().start()

    max_frames = 50
    i = 0


    while True:


        frame = cam.read()


        if i > max_frames:

            fps.stop()
            print(fps.elapsed())
            print(fps.fps())
            break


        i += 1



        testcone(frame, stream=True)
        fps.update()
        cv2.imshow('', frame)
        cv2.waitKey(1)


from_stream()

