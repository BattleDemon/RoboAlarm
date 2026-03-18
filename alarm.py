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
    IDLE = 0
    SETTING = 1
    EDITING = 2
    CHALLENGE = 3
    VIEW = 4

class Challenges(Enum):
    LEDMEMORYGAME = 0
    MOTORCONTROLTEST = 1
    COLOURRECOGNITION = 2
    DISTANCECHALLENGE = 3
    GYROCOORDINATION = 4

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

        self.state = State.IDLE

        self.led = Leds()
        self.lcd = Display()
        self.btn = Button()
        self.sound = Sound()

        self.lm = LargeMotor()
    
        self.uss = UltrasonicSensor()
        self.cs = ColorSensor()
        self.gy = GyroSensor()
        self.ts = TouchSensor()

        self.time = datetime.now().time()
        self.alarms :List(Alarm) = []
        self.challenges = []

        def change_state(self):
            pass

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
                    self.change_state(selector)

                time.sleep(0.2)

    def set_alarm(self):
        
        while True:
            self.lcd.clear()
            self.lcd.text_pixels("Set Alarm", 10, 10)

            selector = 0

            # things to edit: Alarm, Time, Alarm sound, Challenge amount

    def edit_alarm(self):
        pass
    
    def view_alarms(self):
        
        while True:
            self.lcd.clear()
            self.lcd.text_pixels("Alarms", 10, 10)

            y_pos = 40

            i = 0

            while i < len(self.alarms):
                alarm = self.alarms[i]
                text = alarm.get_description()

                self.lsd.text_pixels(text,10,y_pos)

                y += 20
                i += 1

            if len(self.alarms) == 0:
                self.lsd.text_pixels("No alarms set", 10, 40)

            self.lds.update()

            if self.btn.any:
                return

            time.wait(0.2)



alarm_bot = AlarmBot()

while true:
    if alarm_bot.state == State.IDLE:
        alarm_bot.main_menu()

    elif alarm_bot.state == State.SETTING:
        alarm_bot.set_alarm()

    elif alarm_bot.state == State.EDITING:
        alarm_bot.edit_alarm()

    elif alarm_bot.state == State.VIEW:
        alarm_bot.view_alarms()

    elif alarm.state == State.CHALLENGE:
        pass

    else:
        print("How are you seeing this?")

    time.sleep(.2)