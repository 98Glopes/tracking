# -*- coding: utf-8 -*
"""
Script para sinalizar quando o carro estiver sobre a plataforma
"""
import argparse
import time

import cv2
import imutils
import numpy as np

from webcam import WebcamVideoStream
from fps import FPS
from hardware import digitalWrite

def write(img, texto, cor=(255,0,0), pos=(20,40)):
    fonte = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, texto, pos, fonte, 0.8, cor, 0, 
                cv2.LINE_AA)

if __name__ == '__main__':

#Argumentos para chamada via linha de comando
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--source", type=int, default=0,
	    help="Camera de onde será extraido as imagens")
    ap.add_argument("-g", "--gaussian", type=int, default=7,
	    help="Dim. da caixa do filtro gaussiano, insira valores impares")
    ap.add_argument("-t", "--threshold", type=int, default=160,
        help="Treshold da binarização" )
    ap.add_argument("-l", "--limite", type=int, default=50,
        help="Porcentagem de branco minima encontrada para ativar a saída")
    args = vars(ap.parse_args())

#Classe para ler os frames da camera/video com multithread
    camera = WebcamVideoStream(src=args['source']).start()
#Classe para contar o FPS do código
    fps = FPS().start()

    while True:

#Le o frame disponivel da camera através da classe WebcamVideoStream
        r, frame = camera.read()
#        frame = imutils.resize(frame, width=680)

#Converte para escala de cinza, aplica um filtro gaussiano e binariza
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (args['gaussian'], args['gaussian'] ), 0)
        T , bin = cv2.threshold(blur, args['threshold'], 255, cv2.THRESH_BINARY)

#Soma a quantidade de pontos brancos na imagem
        soma = bin.sum()
#Calcula a porcentagem de pontos brancos na imagem
        area = bin.shape[0] * bin.shape[1] * 255
        percent = soma * 100 / area 

#Verifica se a porcentagem de branco esta maior que o limite
        if percent > args['limite']:

            digitalWrite(True)
            write(bin, 'Plataforma Localizada', pos=(130,40))
        else:

            digitalWrite(False)
#Escreve na Imagem a porcentagem de branco e mostra as imagens    
        write(bin, str(round(percent)))
        cv2.imshow('Gray', bin)
        cv2.imshow('Original', frame)
        fps.update()

      
        if cv2.waitKey(1) == ord('q'):
            
            fps.stop()
            camera.release()
            print(fps.elapsed())
            print(fps.fps())
            cv2.destroyAllWindows()
            break      