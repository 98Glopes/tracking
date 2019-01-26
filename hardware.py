# -*- coding: utf-8 -*-
"""
Módulo para se comunicar com o hardware da Jetson TX2
"""
try:
    import Hardware_API_JTX2
except:
    pass

def digitalWrite(bool):
    
    try:
        #Inserir aqui código para acessar hardware da JTX2
        print("ok")
        return True
    except:

        return False

def analogWrite(int):

    try:
        #Inserir aqui código para acessar hardware da JTX2
        return True
    
    except:

        return False