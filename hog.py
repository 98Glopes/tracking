import cv2
import numpy as np 
import imutils

if __name__ == '__main__':

    camera = cv2.VideoCapture('videos/cone3.mp4')

    while True:

        _, im = camera.read()
        #im = imutils.resize(im, width=256, height=512)
        
        im = np.float32(im) / 255.0

        gx = cv2.Sobel(im, cv2.CV_32F, 1, 0, ksize=1)
        gy = cv2.Sobel(im, cv2.CV_32F, 1, 0, ksize=1)

        img = gx + gy

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        T , bin = cv2.threshold(img*255, 50, 255, cv2.THRESH_BINARY)
        cv2.imshow('gx', gx+gy)
        #cv2.imshow('gy', gy)
        if cv2.waitKey(33) == ord('q'): 
            break