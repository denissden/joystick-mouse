import serial
import time
import utils

class Joystick:
    serial_: serial.Serial

    top_x: float = 1024.
    middle_x: float = 512.
    bottom_x: float = 0
    top_y: float = 1024.
    middle_y: float = 512.
    bottom_y: float = 0

    x: float = 0
    y: float = 0
    offset_x: float = 0
    offset_y: float = 0
    button: int = 0
    _prev_button: int
    clicked: bool

    def __init__(self, path, rate=38400, **serial_kwargs):
        try:
            self.serial_ = serial.Serial(path, baudrate=rate, **serial_kwargs)
        except PermissionError as e:
            print(f"Not enough permissions to open {path}: {e}")

    def read(self):

        byte = self.serial_.readline()
        s = ''.join(map(chr, byte))
        sp = s.split(":")
        if len(sp) == 2:
            n, values = sp
        else:
            return
        sp = values.strip().split(",")
        if len(sp) == 3:
            self._prev_button = self.button

            self.y, self.x, self.button = [float(i) for i in sp]
            self.get_offset()

            self.clicked = not self._prev_button and self.button
        else:
            print("Wrong read format")

    def get_offset(self):
        if self.x < self.middle_x:
            self.offset_x = 1 - utils.interpolate(self.x, self.bottom_x, self.middle_x)
            self.offset_x *= -1
        else:
            self.offset_x = utils.interpolate(self.x, self.middle_x, self.top_x)
        if self.y < self.middle_y:
            self.offset_y = 1 - utils.interpolate(self.y, self.bottom_y, self.middle_y)
            self.offset_y *= -1
        else:
            self.offset_y = utils.interpolate(self.y, self.middle_y, self.top_y)

    def calibrate(self):
        print("Don't move the joystick for 1 second")
        time.sleep(0.5)
        values_x = []
        values_y = []
        amount = 100
        for i in range(amount):
            self.read()
            values_x.append(self.x)
            values_y.append(self.y)
        print("You can move the joystick now")
        self.middle_x = sum(values_x) / amount
        self.middle_y = sum(values_y) / amount
        print(f"Middle point is {self.x}, {self.y}")
