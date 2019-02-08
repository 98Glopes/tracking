# -*- coding: utf-8 -*-
import math
import argparse

import cv2 

from fps import FPS
from hardware import analogWrite
from hsv_filter import filtro_hsv


if __name__ == '__main__':

#Argumentos para chamada via linha de comando
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--source", default=0,
	    help="Camera de onde será extraido as imagens")
    ap.add_argument("-c", "--classifier", default="classifiers/1900_15stages.xml",
        help="Classificador para as imagens")
    ap.add_argument("-sf", "--scalefactor", default=2.0, type=float,
        help="Scale Factor do detect multi scale")
    ap.add_argument("-n", "--neighbors", default=30, type=int,
        help="minNeighbors do detect multi scale")
    args = vars(ap.parse_args())

    camera = cv2.VideoCapture(args['source'])
    fps = FPS().start()
    df = cv2.CascadeClassifier(args['classifier'])

    #Criação do detector de faces

    while True:

        try:

            r, frame = camera.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #frame = cv2.blur(frame, (3, 3))
            #frame = cv2.equalizeHist(frame)

        except:

            fps.stop()
            print(fps.fps())
            break
    
    #Executa a detecção
        faces = df.detectMultiScale(frame,
            scaleFactor = args['scalefactor'], minNeighbors = args['neighbors'],
            minSize = (35,35), flags = cv2.CASCADE_SCALE_IMAGE)

    #Desenha retangulos amarelos na iamgem original (colorida)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), 255, 3)
    #Exibe imagem. Título da janela exibe número de faces

        if len(faces) == 1:

            x, y, w, h = faces[0]
            medx = (2*x+h)/2
            medy = (2*y+w)/2
            cv2.circle(frame, (int(medx), int(medy)), 50, (0,0,0))

            angulo = medy/(medx-frame.shape[1]/2)
            angulo = math.atan(angulo)
            print(angulo)

        cv2.imshow('Cone', frame)
        fps.update()

        if len(faces) == 1:

            x, y, w, h = faces[0]
            medx = (2*x+h)/2
            medy = (2*y+w)/2
            cv2.circle(frame, (int(medx), int(medy)), 50, (0,0,0))

            angulo = medy/(medx-frame.shape[1]/2)
            angulo = math.atan(angulo)
            if angulo < 0: angulo = angulo + math.pi
            #Transforma o angulo em uma escala de 10 bits
            angulo = int(angulo*(1023/math.pi))
            print(angulo)
            analogWrite(angulo)

        if cv2.waitKey(1) == ord('q'):

            fps.stop()
            print(fps.fps())
            cv2.destroyAllWindows()
            camera.release()
            break

