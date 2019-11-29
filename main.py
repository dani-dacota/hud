import imu
import time

imu = imu.IMU()

while True:
    # print('Distance:', IMU.dist())
    print('Gyro X:', imu.gyro_x(), ', Y:', imu.gyro_y(), ', Z:', imu.gyro_z())
    time.sleep(0.5)
