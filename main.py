#!/usr/bin/env pybricks-micropython
from Conexiones.connections import *
from Felipe_Funciones import Funciones
from tomi_camarita.camara import detectar_bloques



if __name__ == "__main__":
    Funciones.move_distance_cm(10, 200) # Avanza para salir de la zona de salida
    #Funciones.line_follower_pid_time(2)
    Funciones.go_to_left_intersection() # Avanza hsata la primera interseccion izquierda
    Funciones.turn_to_angle(-90) # Gira 90 grados hacia la izquierda
    Funciones.move_distance_cm(1, 200) # Avanza un poco para alejarse de la esquina
    Funciones.line_follower_pid_time(2) # Avanza or 3 segundo con el seguidor de linea para centrarlo
    Funciones.go_to_full_intersection() # Avanza recto hasta la primera full intersection
    wait(200)
    Funciones.move_distance_cm(2.8, 200)
    wait(200)
    Funciones.turn_to_angle(-90)
    Funciones.move_distance_cm(-11, 200)
    Funciones.bajar_brazo(90)
    Funciones.move_distance_cm(12, 200)
    Funciones.bajar_pala(240)
    Funciones.subir_brazo(85)
    Funciones.move_distance_cm(15, 200)
    Funciones.move_distance_cm(-13, 200)
    Funciones.subir_pala(80)
    #Funciones.bajar_pala(80)
    # Funciones.move_distance_cm(10, 200)
    # Funciones.move_distance_cm(-10, 200)
    Funciones.turn_to_angle(90)
    Funciones.line_follower_pid_time(2)
    Funciones.go_to_left_intersection()
    Funciones.turn_to_angle(90)
    Funciones.move_distance_cm(8, 200)
    Funciones.bajar_brazo(90)
    Funciones.move_distance_cm(-12, 200)
    Funciones.subir_brazo(30)
    Funciones.move_distance_cm(-2, 200)
    Funciones.subir_brazo(20)
    Funciones.move_distance_cm(-4, 200)
    Funciones.subir_pala(30)
    Funciones.go_to_right_intersection()
    Funciones.turn_to_angle(90)
    Funciones.line_follower_pid_time(2)
    wait(500)
    Funciones.go_to_right_intersection()
    wait(500)
    Funciones.move_distance_cm(-2.8, 200)
    Funciones.turn_to_angle(90)
    wait(500)
    Funciones.bajar_pala(240)

