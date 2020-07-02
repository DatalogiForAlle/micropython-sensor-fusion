import machine
import utime
import lsm9ds1
# Option 1: Mahony algorithm - fast and somewhat precise
from fusion.mahony import Mahony
filter = Mahony()

# Option 2: Madgwick algorithm - slower, but more precise
#from fusion.madgwick import Fusion
#filter = Fusion()

# Option 3: Complementary filter - faster, but less precise
# from fusion.complementary import ComplementaryFilter
# filter = ComplementaryFilter(weight=0.5)

# initialize sensor
i2c = machine.I2C(-1, machine.Pin(17), machine.Pin(16))
magnet_addr, gyro_addr = i2c.scan()
lsm = lsm9ds1.LSM9DS1(i2c, address_gyro=gyro_addr, address_magnet=magnet_addr)

lastUpdate = 0
lastFilterUpdate = 0

while True:
    # read from sensor
    now = utime.ticks_us()
    deltat = ((now - lastUpdate)/1000000.0)
    lastUpdate = now

    filter.update(lsm.read_accel(), lsm.read_gyro(), lsm.read_magnet(), deltat)

    delt = utime.ticks_ms() - lastFilterUpdate

    if delt > 100:
        filter.compute_angles()
        print(filter.pitch, filter.roll, filter.heading)
        lastFilterUpdate = utime.ticks_ms()
