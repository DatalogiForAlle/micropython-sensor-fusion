import math
from deltat import DeltaT

#GYROSCOPE_SENSITIVITY = 65.536
GYROSCOPE_SENSITIVITY = 8.75
class ComplementaryFilter:
    def __init__(self, weight=0.05):
        self.pitch = 0
        self.roll = 0
        self.heading = 0
        self.weight = weight
        self.deltat = DeltaT(None)

    def update_nomag(self, acceleration, gyro):
        """
        dt: Time since last call to process in milliseconds
        """
        dt = self.deltat(None)
        #dt = dt / 1000
        acc_x = acceleration[0]
        acc_y = acceleration[1]
        acc_z = acceleration[2]
        gyro_x = gyro[0]
        gyro_y = gyro[1]
        gyro_z = gyro[2]
        w = self.weight

        if acc_x == 0 or acc_y == 0 or acc_z == 0:
            return None

        # Complementary filter on roll estimation
        roll_acc = math.degrees(math.atan2(acc_y, acc_z))
        roll_gyro = (gyro_x / GYROSCOPE_SENSITIVITY) * dt + self.roll
        self.roll = roll_acc * w + (1-w) * roll_gyro

        # Complementary filter on pitch estimation
        pitch_acc = math.degrees(math.atan(-1*acc_x/math.sqrt(pow(acc_y,2) + pow(acc_z,2))))
        pitch_gyro = (gyro_y / GYROSCOPE_SENSITIVITY) * dt + self.pitch
        self.pitch = (1-w) * pitch_gyro + w * pitch_acc

        
    def update(self, acceleration, gyro, magnetometer):
        """
        dt: Time since last call to process in milliseconds
        """
        self.update_nomag(acceleration, gyro)
        acc_x = acceleration[0]
        acc_y = acceleration[1]
        acc_z = acceleration[2]
        mag_x = magnetometer[0]
        mag_y = magnetometer[1]
        mag_z = magnetometer[2]

        # Normalize accelerometer raw values
        l = math.sqrt(pow(acc_x, 2) + pow(acc_y, 2) + pow(acc_z, 2))
        accXnorm = acc_x / l
        accYnorm = acc_y / l

        # Calculate pitch and roll for compensated yaw
        magPitch = math.asin(accXnorm)
        magRoll = -math.asin(accYnorm / math.cos(magPitch))

        # Calculate the new tilt compensated values
        magXcomp = mag_x * math.cos(magPitch) + mag_z * math.sin(magPitch)
        magYcomp = (mag_x * math.sin(magRoll) * math.sin(magPitch)
                    + mag_y * math.cos(magRoll)
                    - mag_z * math.sin(magRoll) * math.cos(magPitch))

        # Calculate tilt compensated heading
        self.heading = math.degrees(math.atan2(magYcomp, magXcomp))
        if self.heading < 0:
            self.heading += 360
