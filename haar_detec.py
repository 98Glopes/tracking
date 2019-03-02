# -*- coding: utf-8 -*-
import math
import argparse

import cv2 

from webcam import WebcamVideoStream
from fps import FPS
from hardware import analogWrite
from hsv_filter import filtro_hsv


if __name__ == '__main__':

#Argumentos para chamada via linha de comando
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--source", default='0',
	    help="Camera de onde será extraido as imagens")
    ap.add_argument("-c", "--classifier", default="classifiers/800_25x25_24stages.xml", type=str,
        help="Classificador para as imagens")
    ap.add_argument("-sf", "--scalefactor", default=2.0, type=float,
        help="Scale Factor do detect multi scale")
    ap.add_argument("-n", "--neighbors", default=5, type=int,
        help="minNeighbors do detect multi scale")
    ap.add_argument("-v", "--video", default=None,
        help="Especifica um arquivo de video para saida")
    ap.add_argument("-d", "--debug", default=False, type=bool,
        help="True para ativar o imshow")
    args = vars(ap.parse_args())

    if args['video']:

        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        output = cv2.VideoWriter(args['video'],fourcc, 20.0,(640,480))

    #Verifica se o parametro --source é um mumero (numero de uma camera)
    #ou o caminho para algum arquivo de video
    if args['source'].isnumeric():

        #Se for o indice de uma camera usa a classe WebcamVideoStream
        camera = WebcamVideoStream(src=int(args['source'])).start()
    else:

        #se for uma string inicia com a classe padrão da opencv
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
        cones = df.detectMultiScale(frame,
            scaleFactor = args['scalefactor'], minNeighbors = args['neighbors'],
            minSize = (35,35), flags = cv2.CASCADE_SCALE_IMAGE)

    #Desenha retangulos amarelos na iamgem original (colorida)
        for (x, y, w, h) in cones:
            cv2.rectangle(frame, (x, y), (x + w, y + h), 255, 3)
    
        if args['debug']: cv2.imshow('Cone', frame)

        #Se especificado algum arquivo de video de saida, salva o frame
        if args['video']:
            video_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            output.write(video_frame)

        fps.update()

        if len(cones) == 1:

            x, y, w, h = cones[0]
            #medx = (2*x+h)/2
            #medy = (2*y+w)/2
            #cv2.circle(frame, (int(medx), int(medy)), 50, (0,0,0))

            #angulo = medy/(medx-frame.shape[1]/2)
            #angulo = math.atan(angulo)
            #if angulo < 0: angulo = angulo + math.pi
            #Transforma o angulo em uma escala de 10 bits
            #angulo = int(angulo*(1023/math.pi))
            
            print(int(x+w/2))
            analogWrite(1, int(x+w/2))

        if cv2.waitKey(16) == ord('q'):

            fps.stop()
            print(fps.fps())
            cv2.destroyAllWindows()
            camera.release()
            break

