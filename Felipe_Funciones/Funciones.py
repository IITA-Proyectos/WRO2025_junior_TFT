#!/usr/bin/env pybricks-micropython
from Conexiones.connections import *
import math, time

def mover_con_pid_sin_reiniciar(distancia_mm, angulo, velocidad=200, kp=1, ki=0.07, kd=0.1):
    robot.reset()             # Reinicia medición de distancia
    target_angle = angulo     # Ángulo objetivo recto
    error_acum = 0            # Integral PID
    error_prev = 0            # Derivativo PID
    while abs(robot.distance()) < abs(distancia_mm):  # Hasta recorrer la distancia
        error = target_angle - gyro.angle()           # Diferencia de ángulo
        error_acum += error                           # Suma de errores (integral)
        derivada = error - error_prev                 # Cambio de error (derivativo)
        error_prev = error
        correction = (kp * error) + (ki * error_acum) + (kd * derivada)  # PID
        # Avanza o retrocede aplicando la corrección
        robot.drive(velocidad if distancia_mm > 0 else -velocidad, correction)
        wait(5)   # Pausa pequeña para estabilidad
    robot.stop()  # Detiene motores al finalizar


def giro_izq(angulo, velocidad=200):
    angulo = angulo + 1
    reloj = StopWatch()
    while gyro.angle() >= angulo and reloj.time() < 6000:
        motor_izquierdo.run(-velocidad)
        motor_derecho.run(velocidad)
        wait(1)
    motor_izquierdo.stop()
    motor_derecho.stop()
    error = angulo - gyro.angle()
    while abs(error) > 1:
        direction = 1 if error > 0 else -1
        motor_izquierdo.run(-direction * 20)
        motor_derecho.run(-direction * 20)
        error = angulo - 1 - gyro.angle()
        wait(0.01)
    motor_izquierdo.stop()
    motor_derecho.stop()
    print(gyro.angle())

def giro_der(angulo, velocidad=200):
    angulo = angulo - 1
    reloj = StopWatch()
    while gyro.angle() <= angulo and reloj.time() < 6000:
        motor_izquierdo.run(velocidad)
        motor_derecho.run(-velocidad)
        wait(1)
    motor_izquierdo.stop()
    motor_derecho.stop()
    error = angulo - gyro.angle()
    while abs(error) > 1:
        direction = 1 if error > 0 else -1
        motor_izquierdo.run(-direction * 20)
        motor_derecho.run(-direction * 20)
        error = angulo - 1 - gyro.angle()
        wait(0.01)
    motor_izquierdo.stop()
    motor_derecho.stop()
    print(gyro.angle())

# Control del brazo
def subir_brazo(altura):
    brazo.run_angle(100, -altura)  # Subir brazo
    wait(500)

def bajar_brazo(altura):
    brazo.run_angle(100, altura)   # Bajar brazo
    wait(500)

# Control de la pala
def subir_pala(altura):
    pala.run_angle(200, altura)    # Subir pala
    wait(500)

def bajar_pala(altura):
    pala.run_angle(200, -altura)   # Bajar pala
    wait(500)


# --------------- Funciones nuevas ---------------
# Funcion para leer el array_sensor de luz en el piso del frente
def leer_array_sensor():
    lecturas = []
    for reg in range(0x42, 0x4A):  # 0x42 to 0x49 inclusive
        value = light_sensor_frontal.read(reg, 1)[0]
        lecturas.append(value)
    return lecturas

def calculate_line_error(values):
    positions = [-400, -300, -200, -100, 100, 200, 300, 400]
    weights = [100 - v for v in values]  # Invert: black = high weight
    total_weight = sum(weights)
    if total_weight == 0:
        return 0  # Avoid division by zero
    error = sum(w * p for w, p in zip(weights, positions)) / total_weight
    return int(error) / 100

def turn_to_angle(target_angle, speed=200):
    initial_angle = gyro.angle()
    if target_angle > 0:
        while gyro.angle() - initial_angle < target_angle:
            motor_izquierdo.run(speed)
            motor_derecho.run(-speed)
        motor_izquierdo.stop()
        motor_derecho.stop()
        # Correction step
        while abs(gyro.angle() - initial_angle - target_angle) > 0.5:
            error = target_angle - (gyro.angle() - initial_angle)
            correction_speed = 100 if error > 0 else -100
            motor_izquierdo.run(correction_speed)
            motor_derecho.run(-correction_speed)
        motor_izquierdo.stop()
        motor_derecho.stop()
    else:
        while gyro.angle() - initial_angle > target_angle:
            motor_izquierdo.run(-speed)
            motor_derecho.run(speed)
        motor_izquierdo.stop()
        motor_derecho.stop()
        # Correction step
        while abs(gyro.angle() - initial_angle - target_angle) > 0.5:
            error = target_angle - (gyro.angle() - initial_angle)
            correction_speed = 100 if error < 0 else -100
            motor_izquierdo.run(-correction_speed)
            motor_derecho.run(correction_speed)
        motor_izquierdo.stop()
        motor_derecho.stop()


def move_distance_cm(distance_cm, max_speed):
    '''
    Move the robot the given distance (in centimeters) using DriveBase (robot) with gyro correction for high precision.
    max_speed: mm/s (positive number)

    Use
        Funciones.move_distance_cm(200, 500) # Go front 200 cm at 500 speed
        wait(3000)
        Funciones.move_distance_cm(-200, 500) # Go back 200 cm at 500 speed
        wait(3000)
    '''
    kp_forward = 2.0  # Proportional gain for forward
    kp_backward = 3.0  # Try higher gain for backward (tune as needed)
    ki = 0.02  # Integral gain (tune as needed)
    max_correction = 200  # Maximum correction value (deg/sec)
    deadband = 0.5  # Ignore angle errors smaller than this (deg)
    min_speed = 80  # Minimum speed (mm/s)
    if max_speed < min_speed:
        max_speed = min_speed

    distance_mm = distance_cm * 10
    initial_angle = gyro.angle()
    robot.reset()

    direction = 1 if distance_mm >= 0 else -1
    total = abs(distance_mm)

    def get_speed(pos):
        # Accelerate for first 10%, cruise, decelerate for last 10%
        accel_dist = total * 0.1
        decel_dist = total * 0.1
        cruise_start = accel_dist
        cruise_end = total - decel_dist
        if pos < cruise_start:
            # Accelerate
            return min_speed + (max_speed - min_speed) * (pos / accel_dist)
        elif pos < cruise_end:
            # Cruise
            return max_speed
        else:
            # Decelerate
            return min_speed + (max_speed - min_speed) * ((total - pos) / decel_dist)

    integral = 0
    while abs(robot.distance()) < total:
        pos = abs(robot.distance())
        speed = get_speed(pos) * direction
        angle_error = gyro.angle() - initial_angle
        # Deadband: ignore very small errors
        if abs(angle_error) < deadband:
            angle_error = 0
        # Integral term (anti-windup: only accumulate if error is not zero)
        if angle_error != 0:
            integral += angle_error
        else:
            integral = 0
        # Correction calculation
        if direction == 1:
            correction = -kp_forward * angle_error - ki * integral
        else:
            correction = -kp_backward * angle_error - ki * integral  # Try same sign, higher gain
        # Limit correction
        if correction > max_correction:
            correction = max_correction
        elif correction < -max_correction:
            correction = -max_correction
        robot.drive(speed, correction)
        wait(10)
    robot.stop()
    # --- Correction step: align to initial angle if deviation remains ---
    final_error = gyro.angle() - initial_angle
    if abs(final_error) > 0.5:  # Only correct if error is significant (tune threshold as needed)
        correction_speed = 60  # Slow speed for correction (deg/sec)
        # Turn in place until aligned
        if final_error > 0:
            # Need to turn left
            while gyro.angle() - initial_angle > 0.5:
                motor_izquierdo.run(-correction_speed)
                motor_derecho.run(correction_speed)
                wait(10)
        else:
            # Need to turn right
            while gyro.angle() - initial_angle < -0.5:
                motor_izquierdo.run(correction_speed)
                motor_derecho.run(-correction_speed)
                wait(10)
        robot.stop()


def line_follower_pid(base_speed=500, kp=800.0, ki=0, kd=200):
    '''
    PID line follower using weighted average of all sensors.
    The robot tries to keep the line centered between sensors 3 and 4.
    Runs indefinitely (while True).4
    '''
    num_sensors = 8
    positions = [i for i in range(num_sensors)]
    integral = 0
    last_error = 0
    last_time = time.time()
    while True:
        try:
            values = leer_array_sensor()
            #print(values)
        except Exception:
            print("Error reading light sensor values")
            continue

        weights = [100 - v for v in values]
        total_weight = sum(weights)
        if total_weight == 0:
            error = 0
        else:
            line_pos = sum(w * p for w, p in zip(weights, positions)) / total_weight
            error = line_pos - 3.5
        #print(error)
        #wait(1000)
        now = time.time()
        dt = now - last_time if last_time else 0.01
        integral += error * dt
        derivative = (error - last_error) / dt if dt > 0 else 0
        correction = kp * error + ki * integral + kd * derivative
        print(correction)
        last_error = error
        last_time = now
        left_speed = base_speed + correction
        right_speed = base_speed - correction
        #left_speed = max(-300, min(300, left_speed))
        #right_speed = max(-300, min(300, right_speed))
        motor_izquierdo.run(left_speed)
        motor_derecho.run(right_speed)
        wait(10)

def line_follower_pid_time(run_time, base_speed=300, kp=300.0, ki=0, kd=50):
    '''
    PID line follower using weighted average of all sensors.
    The robot tries to keep the line centered between sensors 3 and 4.
    Runs for run_time seconds.
    '''
    num_sensors = 8
    positions = [i for i in range(num_sensors)]
    integral = 0
    last_error = 0
    last_time = time.time()
    start_time = last_time
    while (time.time() - start_time) < run_time:
        try:
            values = leer_array_sensor()
        except Exception:
            print("Error reading light sensor values")
            continue
        weights = [100 - v for v in values]
        total_weight = sum(weights)
        if total_weight == 0:
            error = 0
        else:
            line_pos = sum(w * p for w, p in zip(weights, positions)) / total_weight
            error = line_pos - 3.5
        now = time.time()
        dt = now - last_time if last_time else 0.01
        integral += error * dt
        derivative = (error - last_error) / dt if dt > 0 else 0
        correction = kp * error + ki * integral + kd * derivative
        last_error = error
        last_time = now
        left_speed = base_speed + correction
        right_speed = base_speed - correction
        motor_izquierdo.run(left_speed)
        motor_derecho.run(right_speed)
        wait(10)
    motor_izquierdo.stop()
    motor_derecho.stop()


def line_follower_intersections(base_speed=300, kp=400.0, ki=0, kd=100, threshold=50):
    '''
    PID line follower using weighted average of all sensors.
    The robot tries to keep the line centered between sensors 3 and 4.
    Runs indefinitely (while True).4
    '''
    full_intersection_count = 0
    left_intersection = 0
    right_intersection = 0
    num_sensors = 8
    positions = [i for i in range(num_sensors)]
    integral = 0
    last_error = 0
    last_time = time.time()
    while True:
        try:
            values = leer_array_sensor()
            #print(values)
        except Exception:
            print("Error reading light sensor values")
            continue

        weights = [100 - v for v in values]
        total_weight = sum(weights)
        if total_weight == 0:
            error = 0
        else:
            line_pos = sum(w * p for w, p in zip(weights, positions)) / total_weight
            error = line_pos - 3.5
        now = time.time()
        dt = now - last_time if last_time else 0.01
        integral += error * dt
        derivative = (error - last_error) / dt if dt > 0 else 0
        correction = kp * error + ki * integral + kd * derivative
        #print(correction)
        last_error = error
        last_time = now
        left_speed = base_speed + correction
        right_speed = base_speed - correction
        motor_izquierdo.run(left_speed)
        motor_derecho.run(right_speed)
        full_black = all(v < threshold for v in values)
        if full_black:
            full_intersection_count += 1
            print("Full intersection: ", full_intersection_count)
            # The 3 line below stop the robot in intersection, change this if needed
            #motor_izquierdo.stop()
            #motor_derecho.stop()
            #wait(3000)
            if full_intersection_count == 1:
                robot.stop()
                wait(1000)
                while True:
                    ev3.speaker.beep(1000, 100)
                    wait(1000)
            if full_intersection_count == 2:
                pass
        left_black = all(values[i] < threshold for i in range(4))
        if left_black:
            left_intersection += 1
            print("left_intersection", left_intersection)
            # The 3 line below stop the robot in intersection, change this if needed
            #motor_izquierdo.stop()
            #motor_derecho.stop()
            #wait(50)
            if left_intersection == 1:
                #robot.stop()
                #turn_to_angle(-90)
                #wait(100)
                #move_distance_cm(2, 200)
                pass
            if left_intersection == 2:
                pass
        right_black = all(values[i] < threshold for i in range(4,8))
        if right_black:
            right_intersection += 1
            print("right_intersection", right_intersection)
            # The 3 line below stop the robot in intersection, change this if needed
            #motor_izquierdo.stop()
            #motor_derecho.stop()
            #wait(3000)
            if right_intersection == 1:
                pass
            if right_intersection == 2:
                pass

def go_to_full_intersection(base_speed=200, black_threshold=50):
    '''
    Drive forward using DriveBase (robot) until all light sensors detect black (intersection).
    base_speed: speed in mm/s
    black_threshold: value below which a sensor is considered to see black (tune for your sensor)
    '''
    robot.reset()
    while True:
        values = leer_array_sensor()
        robot.drive(base_speed, 0)
        # If all sensors see black (value < threshold), stop
        if all(v < black_threshold for v in values):
            robot.stop()
            break


def go_to_left_intersection(base_speed=200, black_threshold=50):
    '''
    Drive forward using DriveBase (robot) until all light sensors detect black (intersection).
    base_speed: speed in mm/s
    black_threshold: value below which a sensor is considered to see black (tune for your sensor)
    '''
    robot.reset()
    while True:
        values = leer_array_sensor()
        robot.drive(base_speed, 0)
        # If all sensors see black (value < threshold), stop
        if all(values[i] < black_threshold for i in range(4)):
            robot.stop()
            break

def go_to_right_intersection(base_speed=200, black_threshold=50):
    '''
    Drive forward using DriveBase (robot) until all light sensors detect black (intersection).
    base_speed: speed in mm/s
    black_threshold: value below which a sensor is considered to see black (tune for your sensor)
    '''
    robot.reset()
    while True:
        values = leer_array_sensor()
        robot.drive(base_speed, 0)
        # If all sensors see black (value < threshold), stop
        if all(values[i] < black_threshold for i in range(4,8)):
            robot.stop()
            break
