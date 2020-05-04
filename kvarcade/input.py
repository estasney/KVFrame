# Read button input through an SN74LS165 shift register.
# Adapted from the Arduino version at
# https://playground.arduino.cc/Code/ShiftRegSN74HC165N

import RPi.GPIO as GPIO
from time import sleep


class SN74LS165:
    pulse_width = 5e-6
    poll_delay = 1e-3

    def __init__(self, clockPin=17, shiftPin=27, dataPin=4, clockInhibitPin=23, n_chips=1,
                 setup=True):
        """

        Parameters
        ----------
        clockPin
        shiftPin
        dataPin
        clockInhibitPin
        n_chips
        setup : bool
            If True, calls `setup` on init

        Notes
        -----

        3 - 6 V

        +----------/---/-----------------+
       1| shiftPin /   /    Vin       |16
       2| clockPin ///// clockInhibit |15
       3|                             |14
       4|                             |13
       5|                             |12
       6|                             |11
       7|                             |10
       8| Vout                dataPin |9
        +-------------------------------+

        IC Pins
        ----
            - Inputs : 3, 4, 5, 6, 11, 12, 13, 14
            - Power (Vcc) : 16
            - Ground : 8
            - Clock : 2
            - Clock Inhibit : 15
            - Serial In: 10
            - Shift/Load : 1
            - Out : 9
            - Out (complementary) : 7

        """
        self.shiftPin = shiftPin
        self.clockPin = clockPin
        self.dataPin = dataPin
        self.clockInhibitPin = clockInhibitPin
        self.n_chips = n_chips
        self.datawidth = self.n_chips * 8

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.shiftPin, GPIO.OUT)
        GPIO.setup(self.clockInhibitPin, GPIO.OUT)
        GPIO.setup(self.clockPin, GPIO.OUT)
        GPIO.setup(self.dataPin, GPIO.IN)

        if setup:
            self.setup()

    def setup(self):
        GPIO.output(self.clockPin, GPIO.LOW)
        GPIO.output(self.shiftPin, GPIO.HIGH)

    def shift_load(self):
        GPIO.output(self.clockInhibitPin, GPIO.HIGH)
        GPIO.output(self.shiftPin, GPIO.LOW)
        sleep(self.pulse_width)
        GPIO.output(self.shiftPin, GPIO.HIGH)
        GPIO.output(self.clockInhibitPin, GPIO.LOW)

    def pulse_clock(self):
        GPIO.output(self.clockPin, GPIO.HIGH)
        sleep(self.pulse_width)
        GPIO.output(self.clockPin, GPIO.LOW)

    def poll(self):
        is_high = set([])
        for i in range(self.datawidth):
            bitVal = GPIO.input(self.dataPin)
            if bitVal > 0:
                is_high.add(i)
            self.pulse_clock()
        return is_high
