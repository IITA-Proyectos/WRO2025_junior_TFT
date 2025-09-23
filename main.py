#!/usr/bin/env pybricks-micropython
from Conexiones.connections import *
from Felipe_Funciones import Funciones
from tomi_camarita.camara import detectar_bloques



if __name__ == "__main__":
    Funciones.esperar_boton()
    Funciones.mover_con_pid_sin_reiniciar(270, 0)    #Avanza al primer punto
    Funciones.giro_izq(-90)                          #gira 90 a la izquierda
    Funciones.mover_con_pid_sin_reiniciar(-100, -90) #
    Funciones.mover_con_pid_sin_reiniciar(380, -90)  #avanza hacia el rover
    Funciones.giro_izq(-180)                         #gira mirando a las pelotitas
    Funciones.mover_con_pid_sin_reiniciar(-90, -180) #retrocede llendo hacia el rover
    Funciones.bajar_brazo(95)                        #baja el brazo
    Funciones.mover_con_pid_sin_reiniciar(100, -180) #baja el panel solar
    Funciones.subir_brazo(85)                        #sube el brazo
    Funciones.turn_to_angle(90)                      #
    Funciones.mover_con_pid_sin_reiniciar(170, -90)  #avanza a la mitad de las pelotas y la caja
    Funciones.turn_to_angle(90)                      #
    Funciones.move_distance_cm(100, 200)             #agarra 3 bloques como max y va hasta el fondo
    Funciones.turn_to_angle(-90)                     #Se acomoda para llevar las pelotas
    Funciones.move_distance_cm(25, 200)              #'''
    Funciones.turn_to_angle(90)                      #'''
    Funciones.move_distance_cm(57, 300)              #deposita los tres bloques
    Funciones.move_distance_cm(-75, 400)             #Retrocede un metro para agarrar los otros tres bloques
    Funciones.turn_to_angle(90)
    Funciones.move_distance_cm(80, 200)              #Avanza hacia el dron
    Funciones.turn_to_angle(90)
    Funciones.move_distance_cm(100, 300)
    Funciones.move_distance_cm(-100, 300)
    Funciones.turn_to_angle(90)
    Funciones.move_distance_cm(-10, 200)
    Funciones.move_distance_cm(30, 200)
    Funciones.turn_to_angle(-90)
    Funciones.move_distance_cm(20, 200)
    motor_derecho.run_angle(400, 1800)
    Funciones.move_distance_cm(97, 300)             #Deja los ultimos bloques
