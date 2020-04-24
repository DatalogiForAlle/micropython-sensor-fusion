import lsm9ds1
import machine
import time

i2c = machine.I2C(-1, machine.Pin(17), machine.Pin(16))
magnet_addr, gyro_addr = i2c.scan()
lsm = lsm9ds1.LSM9DS1(i2c, address_gyro=gyro_addr, address_magnet=magnet_addr)

import complementary
filter = complementary.ComplementaryFilter(weight=0.5)

#import fusion
#filter = fusion.Fusion()

count = 0

while True:
    # Update filter 1000 times per second
    filter.update(lsm.read_accel(), lsm.read_gyro(), lsm.read_magnet())

    # Only use the 100 times per second
    count += 1
    if count == 10:
        print((filter.pitch, filter.roll, filter.heading))
        count = 0

    time.sleep_ms(1)
