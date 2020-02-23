from __future__ import print_function
from datetime import datetime
import numpy as np
import qwiic
import sys
import mpu
import time


def integrate(values):
    x = np.trapz(values['x'])
    y = np.trapz(values['y'])
    z = np.trapz(values['z'])

    return [x, y, z]

def mag(a,b,c=0):
    return (a**2 + b**2 + c**2)**0.5

def idle(value):
    if -1 < value < 1:
        return 0
    return round (value, 1)

def o_str(value):
    return str(round(value,1))

def run():
    # Define oled screen and initialize
    oled = qwiic.QwiicMicroOled()
    oled.begin()

    # clear the screen
    oled.clear(oled.PAGE)
    oled.display()

    # set the font size
    oled.set_font_type(1)

    mpu.MPU_Init()

    #display code version
    oled.set_cursor(2, 5)  # top left of screen
    oled.print('V-0.1.2')
    oled.display()
    time.sleep(2)
    oled.clear(oled.PAGE)

    accel = {'x':[], 'y':[], 'z':[]}
    speed = {'x':[], 'y':[], 'z':[]}

    while True:
        # Read Accelerometer raw value
        acc_x = mpu.read_raw_data(mpu.ACCEL_XOUT_H)
        acc_y = mpu.read_raw_data(mpu.ACCEL_YOUT_H)
        acc_z = mpu.read_raw_data(mpu.ACCEL_ZOUT_H)

        # Read Gyroscope raw value
        gyro_x = mpu.read_raw_data(mpu.GYRO_XOUT_H)
        gyro_y = mpu.read_raw_data(mpu.GYRO_YOUT_H)
        gyro_z = mpu.read_raw_data(mpu.GYRO_ZOUT_H)

        # Full scale range +/- 250 degree/C as per sensitivity scale factor
        Ax = acc_x/16384.0
        Ay = acc_y/16384.0
        Az = acc_z/16384.0

        Gx = gyro_x/131.0
        Gy = gyro_y/131.0
        Gz = gyro_z/131.0

        #add accel
        accel['x'].append(Ax)
        accel['y'].append(Ay)
        accel['z'].append(Az)

        #get_speed from accel
        Vx, Vy, Vz = integrate(accel)

        #add speed
        speed['x'].append(Vx)
        speed['y'].append(Vy)
        speed['z'].append(Vz)

        #get distance from speed
        Dx, Dy, Dz = integrate(speed)

        oled.set_cursor(2, 5)  # top left of screen
        oled.print('X:' + o_str(Ax))

        oled.set_cursor(2, 20)
        oled.print('Y:' + o_str(Ay))

        oled.set_cursor(2, 35)
        oled.print('Z:' + o_str(Az))

        oled.display()
        time.sleep(0.5)
        oled.clear(oled.PAGE)


        oled.set_cursor(2, 5)  # top left of screen
        oled.print('X:' + o_str(Gx))

        oled.set_cursor(2, 20)
        oled.print('Y:' + o_str(Gy))

        oled.set_cursor(2, 35)
        oled.print('Z:' + o_str(Gz))

        oled.display()
        time.sleep(0.5)
        oled.clear(oled.PAGE)
