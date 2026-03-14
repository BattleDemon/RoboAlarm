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

led = Leds()
lcd = Display()
btn = Button()
sound = Sound()

lm = LargeMotor()
    
uss = UltrasonicSensor()
cs = ColorSensor()
gy = GyroSensor()
ts = TouchSensor()

class State(Enum):
    setting = 0
    editing = 1
    idle = 2
    challenges = 3

class Challenges(Enum):
    led_memory_game = 0
	motor_control_test = 1
	colour_recognition = 2
	distance_challange = 3
	gyro_coordination = 4

class siren():
    def __init__(self):
        self.name

class Alarm():
    def __init(self, target_time, siren, challenge_amount): 
        self.siren = siren
        self.target_time = target_time
        self.challenge_amount = challenge_amount

    def play_alarm():
        pass

    def alarm_description(self):
        return f"{self.target_time} | {self.siren.name} | {self.challenge_amount} Challenges"

class AlarmBot():
    def __init__(self):

        self.state = State.idle

        #
        self.time = datetime.now().time()
        self.alarms :List(Alarm) = []
        self.challenges = []

        def main_menu(self):
            menu_items = ["Set Alarm", "Edit Alarm", "View Alarms"]

            selector = 0

            while True:
                self.lcd.clear()
                self.lcd.text_pixels("RoboAlarm", 20, 10)

                y_pos = 40
                i = 0

                while i < len(menu_items):

                    text = menu_items[i]

                    if i == selector:
                        text = ">> " + text

                    else:
                        text = "   " + text

                    self.lcd.text_pixels(text,10,y_pos)

                    y_pos += 20
                    i += 1
                
                self.lcd.update()

                if self.btn.up:
                    selector -= 1

                    if selector < 0:
                        selector = len(menu_items)

                if self.btn.down:
                    selector += 1

                    if selector > len(menu_items):
                        selector = 0

                if self.btn.enter:
                    return selector

                time.sleep(0.2)

    def set_alarm(self):
        pass

    def edit_alarm(self):
        pass
    
    def view_alarms(self):
        
        while True:
            self.lcd.clear()
            self.lcd.text_pixels("Alarms", 10, 10)



alarm = AlarmBot()


while true:
    if alarm.state == State.idle:
        pass

    elif alarm.state == State.setting:
        pass

    elif alarm.state == State.editing:
        pass

    elif alarm.state == State.challenges:
        pass

    else:
        print("How are you seeing this?")

    time.sleep(.2)