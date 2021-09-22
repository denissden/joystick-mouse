import serial
from pymouse import PyMouse
from joystick import Joystick
from utils import interpolate_power

mouse = PyMouse()
remainder_x, remainder_y = 0., 0.


# path to arduino device
device = "/dev/ttyACM0"

# mouse settings
# acceleration 
#####
#          .-~|
#      .-`    |                 
#    .`       |        
#   .         |          
#  .          |
# ------------+
# power = 0.5  
#####
#            .|
#           . |                 
#          .  |        
#       .-`   |          
#  ..--`      |
# ------------+
# power = 2      
power = 2
# threshold to reach before movement starts
thresh = 0.05
# cursor speed
speed = 4

def int_remainder(v):
    vint = int(v)
    rem = v - vint
    return vint, rem


# allows to move mouse less than one pixel by
# saving the remainder of float conversion
# to int. 
def move_mouse(x, y):
    global remainder_x, remainder_y
    mx, my = mouse.position()
    x, r = int_remainder(x)
    remainder_x += r
    if abs(remainder_x) > 1:
        rx, remainder_x = int_remainder(remainder_x)
        x += rx

    y, r = int_remainder(y)
    remainder_y += r
    if abs(remainder_y) > 1:
        ry, remainder_y = int_remainder(remainder_y)
        y += ry

    # print(x, remainder_x, " : ", y, remainder_y)
    mouse.move(int(mx + x), int(my + y))


def main():
    joy = Joystick(device, rate=38400)
    joy.calibrate()

    while joy.serial_.is_open:
        joy.read()
        x, y = joy.offset_x, joy.offset_y
        if abs(x) < thresh:
            x = 0
        if abs(y) < thresh:
            y = 0

        inter_x = interpolate_power(x, power)
        # mirror vertical movements
        inter_y = interpolate_power(y, power) * -1 

        inter_x *= speed
        inter_y *= speed

        move_mouse(inter_x, inter_y)

        if joy.clicked:
            mouse.click(*mouse.position(), button=1)


if __name__ == '__main__':
    main()
