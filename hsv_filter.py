import numpy as np 
import cv2

def filtro_hsv(img):

    hsv = img#cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow('', hsv)
    lower_red = np.array([0, 0, 100])

    upper_red = np.array([110, 110, 210])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    cv2.imshow('hsv space', mask)
    res = cv2.bitwise_and(img, img, mask=mask)

    return res

if __name__ == '__main__':

        img = cv2.imread('imagens/cone1.jpg')
        cv2.imshow('original1', img)
        print(img[140,360])
        img = filtro_hsv(img)
        cv2.imshow('hsv space', img)
        cv2.waitKey(0)
    