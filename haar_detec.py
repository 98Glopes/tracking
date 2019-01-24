# -*- coding: utf-8 -*-

#Carrega arquivo e converte para tons de cinza
import cv2 
from fps import FPS

camera = cv2.VideoCapture(0)
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
    print(len(faces))
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 3)
#Exibe imagem. Título da janela exibe número de faces
    cv2.imshow('Cone', frame)
    fps.update()
    cv2.waitKey(1)
quit()
