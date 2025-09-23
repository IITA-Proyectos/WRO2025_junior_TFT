#!/usr/bin/env pybricks-micropython
from Conexiones.connections import *
from Felipe_Funciones import Funciones
from tomi_camarita.camara import detectar_bloques



if __name__ == "__main__":
    Funciones.esperar_boton() # Esta funcion se encarga de esperar a que el boton sea presionado
    """

    Aqui deberia ir su codigo, de instrucciones
    que se ejecutan solo una vez al presionar el boton.

    """
    while True:
        """

        Aqui deberia ir su codigo, de instrucciones
        que se ejecutan en un while(repetidamente)
        al presionar el boton.

        """
        # Beep
        ev3.speaker.beep()
        wait(200)

        # If button pressed again, break to wait for next start
        if touch_sensor.pressed():
            while touch_sensor.pressed():
                wait(10)
            break
