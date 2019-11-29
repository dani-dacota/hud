#!/usr/bin/python
import smbus
import math

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c


class IMU:
    def __init__(self):
        self.bus = smbus.SMBus(1)  # bus = smbus.SMBus(0) for Revision 1
        self.address = 0x68       # via i2cdetect

        # Activate module
        self.bus.write_byte_data(self.address, power_mgmt_1, 0)

    def read_byte(self, reg):
        return self.bus.read_byte_data(self.address, reg)

    def read_word(self, reg):
        h = self.bus.read_byte_data(self.address, reg)
        l = self.bus.read_byte_data(self.address, reg+1)
        value = (h << 8) + l
        return value

    def read_word_2c(self, reg):
        val = self.read_word(reg)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def gyro_x(self):
        return self.read_word_2c(0x43)

    def gyro_y(self):
        return self.read_word_2c(0x45)

    def gyro_z(self):
        return self.read_word_2c(0x47)

    def accel_x(self):
        return self.read_word_2c(0x3b)

    def accel_y(self):
        return self.read_word_2c(0x3d)

    def accel_z(self):
        return self.read_word_2c(0x3f)

    def dist(self, a, b):
        return math.sqrt((a*a)+(b*b))

    def get_y_rotation(self):
        x = self.accel_x
        y = self.accel_y
        z = self.accel_z
        radians = math.atan2(x, self.dist(y, z))
        return -math.degrees(radians)

    def get_x_rotation(self):
        x = self.accel_x
        y = self.accel_y
        z = self.accel_z
        radians = math.atan2(y, self.dist(x, z))
        return math.degrees(radians)


if __name__ == '__main__':
    imu = IMU()
    # print('Distance:', IMU.dist())
    print('Gyro X:', imu.gyro_x())
    print('Gyro Y:', imu.gyro_y())
    print('Gyro Z:', imu.gyro_z())
    # print('Y rotation:', imu.get_y_rotation())
    # print('X rotation:', imu.get_x_rotation())
