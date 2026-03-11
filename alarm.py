#!/usr/bin/env python3
from ev3dev2.sensor import INPUT_2, INPUT_3, INPUT_4,  INPUT_1
from ev3dev2.sensor.lego import *
from ev3dev2.motor import *
from ev3dev2.sound import *
from ev3dev2.button import *
from ev3dev2.display import *
from ev3dev2.fonts import *
from ev3dev2.led import Leds

from enum import Enum
from datetime import datetime

from threading import *

import os

os.system('setfont Lat15-TerminusBold14')

import time
import random

class State(Enum):
    setting = 0
    editing = 1
    idle = 2
    challenges = 3

class Challenges(Enum):
    pass

class Siren():
    pass

class Alarm():
    def __init(self):
        self.siren : Siren
        self.target_time
        self.challenge_amount

class AlarmBot():
    def __init__(self):

        self.state :State = State.idle

        # Robot Sensors and Output Init
        self.led = Leds()
        self.lcd = Display()
        self.btn = Button()
        self.sound = Sound()

        self.lm = LargeMotor()
    
        self.uss = UltrasonicSensor()
        self.cs = ColorSensor()
        self.gy = GyroSensor()
        self.ts = TouchSensor()

        #
        self.time = datetime.now().time()
        self.alarms :List(Alarm) = []
    
    def set_alarm():
        pass

    def set_siren():
        pass

    def set_target_time_until():
        pass

    def set_target_time():
        pass

    def set_challenge_amount():
        pass

    def edit_alarm():
        pass


alarm = AlarmBot()

while true:

    time.sleep(.2)