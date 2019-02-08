# -*- coding: utf-8 -*-
import math
import argparse
import glob

import cv2
import numpy as np


if __name__ == '__main__':

#Argumentos para chamada via linha de comando
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--source", default=0,
	    help="Camera de onde será extraido as imagens")
    ap.add_argument("-c", "--classifier", default="classifiers/",
        help="Classificador para as imagens")
    ap.add_argument("-sf", "--scalefactor", default=2.0, type=float,
        help="Scale Factor do detect multi scale")
    ap.add_argument("-n", "--neighbors", default=30, type=int,
        help="minNeighbors do detect multi scale")
    ap.add_argument("-d", "--dataset", type=str,
        help="Dataset para validar e avaliar os classificadores")
    ap.add_argument("-t", "--threshold", type=int, default=33)
    ap.add_argument("-csv", "--csv", default=None,
        help="Especifica um arquivo csv para receber a saida")
    args = vars(ap.parse_args())

    print('[INFO] Avaliando classificadores para o datset: ', args['dataset'])
    print('.................................................................. \n\n')
    #Lista os classificadores *.xml na pasta especificada
    classificadores = glob.glob(args['classifier']+'*.xml')

    #Abre arquivo CSV e adiciona as colunas iniciais
    if args['csv']:
        csv = open(args['csv'], mode='w')
        csv.writelines('classificador;frames;positivos;f_positivos \n')

    for classificador in classificadores:

        #Carrega as o classificador
        df = cv2.CascadeClassifier(classificador)

        #Le o txt com a lista das imagens ROI do dataset especificado
        info = open(args['dataset']+'info.txt', mode='r').readlines()

        #Inicializa contadores para salvar os resultados
        total_frames = 0
        false_pos = 0
        true_pos = 0
        false_postives = []
        true_positves = []

        #Le cada imagem do dataset passado
        for linha in info:
            
            #Separa o path da imagem e ROI da imagem
            image_path = linha.split(' ')[0]
            bbox = linha.rstrip('\n').split(' ')[2:]

            #Carrega a imagem e desenha o bounding box da mesma
            img  = cv2.imread(args['dataset']+image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            #Escreve no topo da imagem o classificador utilizado
            cv2.putText(img, "Classificador: "+classificador, (50,40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,255,0),2)
            #Traça os pontos do retangulos da ROI da imagem
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0]) + int(bbox[2]), int(bbox[1]) + int(bbox[3]))
            cv2.rectangle(img, p1, p2, (255,0,0), 2, 1)  

            #Detecta os objetos da imagem utilizando o classificador
            objetos = df.detectMultiScale(gray,
                scaleFactor = args['scalefactor'], minNeighbors = args['neighbors'],
                minSize = (35,35), flags = cv2.CASCADE_SCALE_IMAGE)
            
            #background binario da imagem original
            background = np.zeros((img.shape[0],img.shape[1]), dtype=np.uint8)
            background[ int(bbox[1]):int(bbox[1])+int(bbox[3]) , int(bbox[0]):int(bbox[0])+int(bbox[2]) ] = 255
            roi_background = np.zeros((img.shape[0],img.shape[1]), dtype=np.uint8)

            #Desenha a area dos objetos encontrados
            for (x, y, w, h) in objetos:
                cv2.rectangle(img, (x, y) , (x+w, y+h), (0,0,255), 2, 1)

            #Analiza se o objeto encontrado está dentro do area de treino
            for (x, y, w, h) in objetos:
                
                #fundo binario para para desenhar a bbox do objeto encontrado
                #e aplicar a intersecção
                roi_background = np.zeros((img.shape[0],img.shape[1]), dtype=np.uint8)
                roi_background[y:y+h, x:x+w] = 255

                #intersecção entre as areas do objeto encontrado e a area de validação
                intersection = cv2.bitwise_and(background, background, mask=roi_background)

                #Calcula a quantiade de pixels brancos na intersecção
                intersection_area = intersection.sum()/255
                percent = (intersection_area * 100)/ (w + h)

                #Verifica se a maior parte da intersecção estava dentro da area de validação
                #E classifica entre falso posito ou verdadeiro positivo
                if percent > args['threshold']:
                    
                    true_pos += 1
                else:

                    false_pos += 1
            
            total_frames += 1
            cv2.imshow('Original', img)

            if cv2.waitKey(1) == ord('q'): break

        print('[INFO] Classificador: ', classificador)
        print('[INFO] Total de frames: ', total_frames)
        print('[INFO] Positivos: ', true_pos)
        print('[INFO] Falsos Positivos: ', false_pos)
        print('....................................... \n ')
        if args['csv']:
            csv.writelines(classificador + ';' + str(total_frames) + ';' \
                           + str(true_pos) + ';' + str(false_pos) + '\n')

        