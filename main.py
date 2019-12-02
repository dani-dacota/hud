from __future__ import print_function
from datetime import datetime
# import qwiic_py
import qwiic
import sys
import mpu
import time

if __name__ == "__main__":
    # Define oled screen and initialize
    oled = qwiic.QwiicMicroOled()
    oled.begin()

    # clear the screen
    oled.clear(oled.PAGE)
    oled.display()

    # set the font size
    oled.set_font_type(1)

    mpu.MPU_Init()

    print(" Reading Data of Gyroscope and Accelerometer")

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

        # print("Gx=%.2f" % Gx, u'\u00b0' + "/s", "\tGy=%.2f" % Gy, u'\u00b0' + "/s", "\tGz=%.2f" %
        #       Gz, u'\u00b0' + "/s", "\tAx=%.2f g" % Ax, "\tAy=%.2f g" % Ay, "\tAz=%.2f g" % Az)
        # sleep(1)

        # now = datetime.now()
        # currentTime = now.strftime("%H:%M")

        # set cursor position
        oled.set_cursor(2, 10)  # top left of screen
        oled.print('Ax:' + str(Ax))

        oled.set_cursor(2, 20)
        oled.print('Ay:' + str(Ay))

        oled.set_cursor(2, 30)
        oled.print('Az:' + str(Az))

        # display screen
        oled.display()

        time.sleep(.5)
        oled.clear(oled.PAGE)
