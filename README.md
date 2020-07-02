Evaluating MicroPython Sensor Fusion alternatives
=================================================
This repository collects and evaluates various approaches for sensor
fusion, together with their implementations in MicroPython. Both for
6DoF and 9DoF IMU's.

There are several algorithms which seems popular for doing sensor
fusion on microcontrollers:
 - Madgwick
 - Mahony
 - Complementary Filter
 - Kalman Filter

Which algorithm to pick, depends on the situation, as they perform
differently in terms of precision, response time, and computational
requirements. 

The most stable and precise seems to be the Madgwick and Mahony
algorithms, whereas computationally more efficient Complementary
Filter have several shortcomings. We will go through each of the four
algorithms mentioned above, and discuss pros/cons.

Madgwick filter
---------------
The Madgwick algorithm is already ported to MicroPython, however, it's
response time is around 2-10 seconds, which is not appropriate for all
situations.
https://github.com/micropython-IMU/micropython-fusion

Mostly suitable for applications with 9DoF IMU's that requires
relative high precision.

The original implementation available here in both C, C# and Matlab: https://x-io.co.uk/open-source-imu-and-ahrs-algorithms/
(also includes an optimized implementation of the Mahony algorithm and a rather detailed tech report)

Mahony filter
-------------
Seems to be the most widely applicable algorithm for embedded devices,
as it is less computationally demanding than Madgwick.

Adafruit seems to recommend the Mahony algorithm, though only
providing an Arduino C++ version of the algorithm.
https://learn.adafruit.com/ahrs-for-adafruits-9-dof-10-dof-breakout/sensor-fusion-algorithms
Their implementation can be seen here:
https://github.com/adafruit/Adafruit_AHRS/blob/master/src/Adafruit_AHRS_Mahony.cpp
with an example here:
https://github.com/adafruit/Adafruit_AHRS/blob/master/examples/calibrated_orientation/calibrated_orientation.ino

Complementary filter
--------------------
If faster response time is necessary, than what can be obtained from
the Mahony filter, and if precision is not important, the much simpler
Complementary Filter might be interesting.

Kalman filter
-------------
TODO. Not implemented yet. 

Here are a few references:
http://www.cs.unc.edu/~welch/media/pdf/kalman_intro.pdf
https://cybernetist.com/2019/01/13/apollo-kalman-filter-and-go/

Visualizing Yaw/Pitch/Roll
--------------------------
 - https://diydrones.com/profiles/blogs/arduimu-groundstation-written


References
----------
 - The following Google Tech Talk: https://www.youtube.com/watch?v=C7JQ7Rpwn2k
 - Another comparison is available here: http://www.olliw.eu/2013/imu-data-fusing/
 - The implementation in RTIMULib is also mentioned a lot in Arduino communities
 https://github.com/RTIMULib/RTIMULib-Arduino/tree/master/libraries/RTIMULib
 - How to read gyroscope datasheets: https://www.youtube.com/watch?v=anMzEbbbrp8
 - A blog post from Oculus developers: https://developer.oculus.com/blog/sensor-fusion-keeping-it-simple/
 - Implementation from Google Cardboard https://github.com/Zomega/Cardboard/blob/master/src/com/google/vrtoolkit/cardboard/sensors/internal/OrientationEKF.java
 - Quaternion based implementation for Arduino with blogpost
 https://josephmalloch.wordpress.com/portfolio/imu-sensor-fusion/
 https://github.com/malloch/Arduino_IMU/blob/master/firmware/imu.c

 
