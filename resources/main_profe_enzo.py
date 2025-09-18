#!/usr/bin/env pybricks-micropython
from Conexiones.connections import *
from Felipe_Funciones import Funciones
from tomi_camarita.camara import detectar_bloques



if __name__ == "__main__":
    Funciones.move_distance_cm(10, 200) # Avanza para salir de la zona de salida
    Funciones.go_to_left_intersection() # Avanza hsata la primera interseccion izquierda
    Funciones.turn_to_angle(-90) # Gira 90 grados hacia la izquierda
    Funciones.move_distance_cm(1, 200) # Avanza un poco para alejarse de la esquina
    Funciones.line_follower_pid_time(2) # Avanza or 3 segundo con el seguidor de linea para centrarlo
    Funciones.go_to_full_intersection() # Avanza recto hasta la primera full intersection
