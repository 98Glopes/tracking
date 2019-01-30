# -*- coding: utf-8 -*-
import sys
import math
import argparse

import cv2
import imutils

from webcam import WebcamVideoStream
from fps import FPS
from hardware import analogWrite
from hsv_filter import filtro_hsv

if __name__ == '__main__' :

#Argumentos para chamada via linha de comando
 
    #Cria um objeto para o tracker KCF
    tracker = cv2.TrackerKCF_create()
    
    #Escolher a partir dos argumentos entre acessar a camera ou abrir um video
    video = cv2.VideoCapture('videos/cone.mp4')
    #Inicializa o detector por HAAR Cascades
    df = cv2.CascadeClassifier('haar_cascade/1900_15stages.xml')

    # Read first frame.
    r, frame = video.read()

    if r == False:
        print('erro')
    i = 0
    #Loop para detectar os cones com Haar Cascade
    while True:

        r, frame = video.read()
        frame = filtro_hsv(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        #Aplica o detector de cones, retorna uma lista com as 
        #Bounding box dos cones encontrados
        cones = df.detectMultiScale(gray,
                scaleFactor=1.5, minNeighbors=22,
                minSize=(50,50), flags=cv2.CASCADE_SCALE_IMAGE)

    #Desenha retangulos amarelos na iamgem original (colorida)
        for (x, y, w, h) in cones:
            cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 255), 3)

        cv2.imshow('Procurando Cone', gray)
        if cv2.waitKey(1) == ord('q'): break

        #Verfica se existe apenas um cone na imagem
        
        if len(cones) == 1:

            #Transfora bbox encontrada em tupla
            #bbox = (x, y, w, h)
            bbox = tuple(cones[0])
            cv2.destroyAllWindows()
            print("Cone Localizado")
            break

    # Uncomment the line below to select a different bounding box
    #bbox = cv2.selectROI(frame, False)

    # Initialize tracker with first frame and bounding box
    last_bbox = bbox
    ok = tracker.init(frame, bbox)

    while True:
        # Read a new frame
        r, frame = video.read()
        frame = filtro_hsv(frame)
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #frame = cv2.equalizeHist(frame)
        #frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        #Iniciliza o timer para medir o fps
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            last_bbox = bbox
        else :
            # Tracking failure
            bbox = (1, 1, 1, 1)
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        # Display tracker type on frame
        cv2.putText(frame, 'KCF ' + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
    
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
        #print(fps)
        # Display result

        x, y, w, h = bbox
        medx = (2*x+h)/2
        medy = (2*y+w)/2
        cv2.circle(frame, (int(medx), int(medy)), 50, (0,0,0))
        #print(medx, frame.shape[1]/2, medy)

        angulo = medy/(medx-frame.shape[1]/2)
        angulo = math.atan(angulo)

        if angulo < 0: angulo = angulo + math.pi
        #Transforma o angulo em uma escala de 10 bits
        angulo = int(angulo*(1023/math.pi))
        
        print(angulo)
        analogWrite(angulo)
        cv2.imshow("Tracking", frame)
        
        # Exit if ESC pr
        k = cv2.waitKey(10) & 0xff
        if k == ord('q') : 

            video.release()
            cv2.destroyAllWindows()
            quit()
