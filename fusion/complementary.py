import math
from .deltat import DeltaT

#GYROSCOPE_SENSITIVITY = 65.536
GYROSCOPE_SENSITIVITY = 8.75
class ComplementaryFilter:
    def __init__(self, weight=0.05):
        self.pitch = 0
        self.roll = 0
        self.heading = 0
        self.weight = weight
        self.deltat = DeltaT(None)

    def update_nomag(self, acceleration, gyro, dt=None):
        """
        dt: Time since last call to process in milliseconds
        """
        acc_x, acc_y, acc_z = acceleration
        gyro_x, gyro_y, gyro_z = gyro

        if acc_x == 0 or acc_y == 0 or acc_z == 0:
            return None

        deltat = self.deltat(dt)

        # Complementary filter on roll estimation
        roll_acc = math.degrees(math.atan2(acc_y, acc_z))
        roll_gyro = (gyro_x / GYROSCOPE_SENSITIVITY) * deltat + self.roll
        self.roll = roll_acc * self.weight + (1-self.weight) * roll_gyro

        # Complementary filter on pitch estimation
        pitch_acc = math.degrees(math.atan(-1*acc_x/math.sqrt(pow(acc_y,2) + pow(acc_z,2))))
        pitch_gyro = (gyro_y / GYROSCOPE_SENSITIVITY) * deltat + self.pitch
        self.pitch = (1-self.weight) * pitch_gyro + self.weight * pitch_acc

        
    def update(self, acceleration, gyro, magnetometer, dt=None):
        """
        dt: Time since last call to process in milliseconds
        """
        self.update_nomag(acceleration, gyro, dt)
        acc_x, acc_y, acc_z = acceleration
        mag_x, mag_y, mag_z = magnetometer

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

    def compute_angles(self):
        # For compatibility with other approaches
        pass
