import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

import subprocess as sp
from datetime import datetime, timedelta
from time import sleep


class Backlight(object):
    SCREEN_ON = 0
    SCREEN_OFF = 1
    BL_FP = '/sys/devices/platform/rpi_backlight/backlight/rpi_backlight/bl_power'

    def __init__(self):
        self.state = self.read_state()

    def read_state(self):
        with open(self.BL_FP, 'r') as fp:
            status = int(fp.read(1))

        return status

    def write_state(self, state):
        p = sp.Popen(['sudo', 'su'], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        command = 'echo {} > {}'.format(state, self.BL_FP).encode()
        p.stdin.write(command)
        p.communicate()
        return state

    def switch_backlight(self):
        new_state = self.SCREEN_ON if self.state == self.SCREEN_OFF else self.SCREEN_OFF
        self.state = self.write_state(new_state)
        return new_state


class MotionDetect(object):

    def __init__(self, channel, poll_interval, screen_time, gpio):
        self.channel = channel
        self.poll_interval = poll_interval
        self.screen_time = screen_time
        self.last_motion = datetime.now()
        self.gpio = gpio
        self.bl = Backlight()
        self._setup_pin()

    def _setup_pin(self):
        self.gpio.setup(self.channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.gpio.add_event_detect(self.channel, self.gpio.RISING)
        self.gpio.add_event_callback(self.channel, self.motion_detected)

    def loop_once(self):
        """
        Check if any motion events have been detected within self.screen_time
        :return:
        """
        time_since_last_motion = (datetime.now() - self.last_motion)
        if time_since_last_motion <= self.screen_time:
            sleep(self.poll_interval)
            return
        else:
            if self.bl.state == Backlight.SCREEN_ON:
                print("No Motion Detected, Switching Screen Off")
                self.bl.switch_backlight()
            sleep(self.poll_interval)
            return

    def motion_detected(self, *args, **kwargs):
        print("Motion Detected")
        self.last_motion = datetime.now()
        if self.bl.state == Backlight.SCREEN_OFF:
            self.bl.switch_backlight()
        return

if __name__ == '__main__':
    md = MotionDetect(channel=4, poll_interval=1, gpio=GPIO, screen_time=timedelta(seconds=30))
    while True:
        md.loop_once()