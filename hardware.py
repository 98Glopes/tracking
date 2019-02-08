# -*- coding: utf-8 -*-
"""
Módulo para se comunicar com o hardware da Jetson TX2
"""
class PCA9685:
    """
    PWM motor controler using PCA9685 boards.
    This is used for most RC Cars
    """
    def __init__(self, channel, frequency=60):
        import Adafruit_PCA9685
        # Initialise the PCA9685 using the default address (0x40).
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(frequency)
        self.channel = channel

    def set_pulse(self, pulse):
        try:
            self.pwm.set_pwm(self.channel, 0, pulse)
        except OSError as err:
            print("Unexpected issue setting PWM (check wires to motor board): {0}".format(err))

    def run(self, pulse):
        self.set_pulse(pulse)

def digitalWrite(channel, value):
    
    try:
        #Inserir aqui código para acessar hardware da JTX2
        c = PCA9685(channel)
        c.run(value)
        print("ok")
        return True
    except:

        return False

def analogWrite(channel, value):

    try:
        #Inserir aqui código para acessar hardware da JTX2
        c = PCA9685(channel)
        c.run(value)
        return True
    
    except:

        return False
