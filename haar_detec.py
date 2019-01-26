# -*- coding: utf-8 -*-

#Carrega arquivo e converte para tons de cinza
import cv2 
from fps import FPS
import math

from hardware import analogWrite

camera = cv2.VideoCapture('cone.mp4')
fps = FPS().start()
df = cv2.CascadeClassifier('haar_cascade/cascade.xml')

#Criação do detector de faces

while True:

    try:
       r, frame = camera.read()
       frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    except:
        fps.stop()
        print(fps.fps())
        break
 
#Executa a detecção
    faces = df.detectMultiScale(frame,
        scaleFactor = 1.5, minNeighbors = 7,
        minSize = (30,30), flags = cv2.CASCADE_SCALE_IMAGE)

#Desenha retangulos amarelos na iamgem original (colorida)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 3)
#Exibe imagem. Título da janela exibe número de faces
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

    if cv2.waitKey(32) == ord('q'):

        cv2.destroyAllWindows()
        camera.release()
        break
quit()
