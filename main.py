from RpiMotorLib import rpi_dc_lib

left_motor = rpi_dc_lib.L298NMDc(24 ,23 ,12 ,60 ,False, "left_motor")
right_motor = rpi_dc_lib.L298NMDc(17 ,27 ,13 ,60 ,False, "right_motor")

def set_left(p):
    if p >= 0:
        left_motor.forward(p)
    else:
        left_motor.backward(p)

def set_right(p):
    if p >= 0:
        right_motor.forward(p)
    else:
        right_motor.backward(p)

try:
    while True:
        set_left(int(input()))
except KeyboardInterrupt:
    left_motor.brake()
    right_motor.brake()