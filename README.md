# Embedded 3D Spatial Mapping System

This 3D Hallway Mapping project was based around the Texas Instruments MSP432E402Y microcontroller along with the VL53L1X time of flight sensor, and the ULN2003 stepper motor. The microcontroller I/O pins were configured using a C++ program on Keil. This system collected distance measurement data in a 360-degree path, every set interval of horizontal distance. This data was communicated to Python and mapped in a 3D graphical representation using matplotlib.
