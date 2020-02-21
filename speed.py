from __future__ import print_function
from datetime import datetime
# import qwiic_py
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

def idle(value):
    if -0.5 < value < 0.5:
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

    print("Reading Data of Gyroscope and Accelerometer")

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
        Ax = idle(acc_x/16384.0)
        Ay = idle(acc_y/16384.0)
        Az = idle(acc_z/16384.0)

        Gx = gyro_x/131.0
        Gy = gyro_y/131.0
        Gz = gyro_z/131.0

        # print("Gx=%.2f" % Gx, u'\u00b0' + "/s", "\tGy=%.2f" % Gy, u'\u00b0' + "/s", "\tGz=%.2f" %
        #       Gz, u'\u00b0' + "/s", "\tAx=%.2f g" % Ax, "\tAy=%.2f g" % Ay, "\tAz=%.2f g" % Az)
        # sleep(1)

        # now = datetime.now()
        # currentTime = now.strftime("%H:%M")

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
        oled.print('Ax:' + o_str(Ax))

        oled.set_cursor(2, 20)
        oled.print('Gx:' + o_str(Gx))

        oled.set_cursor(2, 35)
        oled.print('Gy:' + o_str(Gy))

        # set cursor position
        # oled.set_cursor(2, 5)  # top left of screen
        # oled.print('A:' + o_str(Ax))

        # oled.set_cursor(2, 20)
        # oled.print('V:' + o_str(Vx))

        # oled.set_cursor(2, 35)
        # oled.print('D:' + o_str(Dx))

        # if len(accel) > 4:
        #     accel.pop(0)

        # display screen
        oled.display()

        time.sleep(.25)
        oled.clear(oled.PAGE)
