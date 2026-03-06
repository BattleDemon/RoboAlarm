#!/usr/bin/env python3
from ev3dev2.sensor import INPUT_2, INPUT_3, INPUT_4,  INPUT_1
from ev3dev2.sensor.lego import *
from ev3dev2.motor import *
from ev3dev2.sound import *
from ev3dev2.button import *
from ev3dev2.display import *
from ev3dev2.fonts import *
from threading import *

import os

os.system('setfont Lat15-TerminusBold14')

import time
import random

sound = Sound()

ultraSonSen = UltrasonicSensor()
colorSen = ColorSensor()
gyroSen = GyroSensor()
touchSen = TouchSensor()

