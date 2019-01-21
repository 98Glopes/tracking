import cv2
import imutils
import numpy as np
import time

from webcam import WebcamVideoStream

def write(img, texto, cor=(255,0,0), pos=(20,40)):
    fonte = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, texto, pos, fonte, 0.8, cor, 0, 
                cv2.LINE_AA)

if __name__ == '__main__':

    camera = WebcamVideoStream(src='grama_2.mp4').start()

    while True:
        


        frame = camera.read()
        frame = imutils.resize(frame, width=680)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7, 7 ), 0)
        T , bin = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)

#Soma a quantidade de pontos brancos na imagem
        soma = bin.sum()
#Calcula a porcentagem de pontos brancos na imagem
        area = bin.shape[0] * bin.shape[1] * 255
        percent = soma * 100 / area 

        if percent > 50:

            write(bin, 'Plataforma Localizada', pos=(130,40))

        write(bin, str(round(percent)))
        
        cv2.imshow('Gray', bin)
        cv2.imshow('Original', frame)

        
        if cv2.waitKey(50) == ord('q'):
            
            cv2.destroyAllWindows()
            break      