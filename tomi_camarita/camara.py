#!/usr/bin/env python3
'''
Hello to the world from ev3dev.org
'''
from Conexiones.connections import *
from Felipe_Funciones import Funciones

box_amarillo=0
box_roja=0
box_blanca=0
box_verde=0

detecciones = []

def detectar_bloques():
    global box_amarillo, box_roja, box_blanca, box_verde
    pixy2.set_lamp(1, 1)
    Funciones.move_distance_cm(23, 100)
    wait(200)
    # Repito la accion de detectar y avanzar 6 veces
    for i in range(6):
        pieza = detect_signature()
        if pieza != None:
            if pieza== "white_box":
                box_blanca=i+1
            elif pieza=="green_box":
                box_verde=i+1
            elif pieza=="red_box":
                box_roja=i+1
            elif pieza=="yellow_box":
                box_amarillo=i+1
        #detecciones.append(pieza)
        if i < 5: # Solo avanzo 5 veces, la sexta no
            Funciones.move_distance_cm(9.3, 100)
            wait(200)

    # Finalizo el bucle y limpio la lista de detecciones
    #detecciones = ["Vacio" if x is None else x for x in detecciones]
    print("------------------------------")
    print("amarillo: ",box_amarillo)
    print("rojo: ",box_roja)
    print("verde: ",box_verde)
    print("blanco: ",box_blanca)


# Estos colores pueden cambiar, debe coincidir con los configurados en PixyMon
colores = {'1': "white_box", '2': "red_box", '3': "yellow_box", '4': "green_box"}



# Función para detectar la firma y devolver el color machea con la lista de colores, OJO !
# Si no detecta nada, devuelve None
def detect_signature():
    nr_blocks, blocks = pixy2.get_blocks(15, 1) # Con el valor 15 devuelve la deteccion de hasta el 4 signature
    try:
        #debug_print("nro: ", nr_blocks, "blocks: ", blocks[0])
        if nr_blocks >= 1:
            sig = blocks[0].sig
            x = blocks[0].x_center
            y = blocks[0].y_center
            w = blocks[0].width
            h = blocks[0].height
            #debug_print("signature: ", colores.get(str(sig)))
            #debug_print("X center: ", x)
            #debug_print("Y center: ", y)
            #debug_print("width: ", w)
            #debug_print("height: ", h)
            return colores.get(str(sig))
    except:
        pass
    #debug_print("----------------------------------------")

if __name__ == '__main__':
    pass
"""
    # Get version
    version = pixy2.get_version()
    debug_print('Hardware: ', version.hardware)
    debug_print('Firmware: ', version.firmware)
    resolution = pixy2.get_resolution()
    debug_print('Frame width:  ', resolution.width)
    debug_print('Frame height: ', resolution.height)
    pixy2.set_lamp(1, 1) # Turn on the Pixy2 lamp
"""
