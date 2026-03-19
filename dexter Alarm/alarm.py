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

class Challenge_types(Enum):
    LEDMEMORYGAME = 0
    MOTORCONTROLTEST = 1
    COLOURRECOGNITION = 2
    DISTANCECHALLENGE = 3
    GYROCOORDINATION = 4

SIRENS = {}

class Alarm():
    def __init__(self, target_time, siren, challenge_amount): 
        self.siren = siren
        self.target_time = target_time
        self.challenge_amount = challenge_amount

    def ring(self):
        pass

    def alarm_description(self):
        return f"{self.target_time} | {self.siren} | {self.challenge_amount} Challenges"

class Challenge():
    def __init__(self,challenge_type=Challenge_types):
        self.type = challenge_type

    def run(self):
        if self.type == Challange_types.LEDMEMORYGAME:
            pass
        elif self.type == Challange_types.MOTORCONTROLTEST:
            pass
        elif self.type == Challange_types.COLOURRECOGNITION:
            pass
        elif self.type == Challange_types.DISTANCECHALLENGE:
            pass
        elif self.type == Challange_types.GYROCOORDINATION:
            pass

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

        self.current_time = datetime.now().time()
        self.alarms = []
        self.challenges = []
        self.menu_items = ["Set Alarm", "Edit Alarm", "View Alarms"]

    def clear_screen(self):
        self.lcd.clear()

    def change_state(self, selection=None, sub_menu=None):
        if selection is not None:
            if selection >= len(self.menu_items):
                print("Invalid selection")
            else:
                if selection == 0:
                    self.state = State.SETTING
                elif selection == 1:
                    self.state = State.EDITING
                elif selection == 2:
                    self.state = State.VIEW
        elif sub_menu is not None:
            self.state = State.IDLE
        else:
            self.state = State.CHALLENGE

    def main_menu(self):
        selector = 0

        while self.state == state.IDLE:
            self.clear_screen()
            self.lcd.text_pixels("== RoboAlarm ==", clear_screen=False, x=10, y=20, text_color='black')

            y_pos = 30
            i = 0

            while i < len(self.menu_items):
                text = self.menu_items[i]

                if i == selector:
                    text = ">> " + text
                else:
                    text = "   " + text

                self.lcd.text_pixels(text,clear_screen=False, x=10, y=y_pos, text_color='black')

                y_pos += 15
                i += 1
            
            self.lcd.update()

            if self.btn.up:
                selector -= 1
                if selector < 0:
                    selector = len(self.menu_items) - 1

            if self.btn.down:
                selector += 1
                if selector > len(self.menu_items):
                    selector = 0 

            if self.btn.enter:
                self.change_state(selection=selector)

            time.sleep(0.05)

    def alarm_editor(self, existing_alarm=None):
        siren_names = list(SIRENS.keys())

        if existing_alarm is None:
            hour = 7
            minute = 0
            siren_index = 0
            challenge_amount = 1
            title = "== Set Alarm =="
        else:
            hour_str, minute_str = existing_alarm.target_time.split(":")
            hour = int(hour_str)
            minute = int(minute_str)

            siren_index = siren_names.index(existing_alarm.siren)

            challenge_amount = existing_alarm.challenge_amount
            title = "== Edit Alarm =="

        fields = ["Hour", "Minute", "Siren", "Challenges", "Save", "Cancel"]
        selector = 0

        while self.state == State.SETTING:
            self.clear_screen()
            self.lcd.text_pixels(title, clear_screen=False, x=10, y=10, text_color='black')

            y_pos = 30
            i = 0

            while i < len(fields):
                label = fields[i]

                if label == "Hour":
                    value = f"{hour:02}" # :02 pads the values to always have two numbers "01" but keep as "11"
                elif label == "Minute":
                    value = f"{minute:02}"
                elif label == "Siren":
                    value = siren_names[siren_index]
                elif label == "Challenges":
                    value = str(challenge_amount)
                else:
                    value = ""

                if i == selector:
                    prefix = ">> "
                else:
                    prefix = "   "

                if value != "":
                    line = f"{prefix}{label}: {value}"
                else:
                    line = f"{prefix}{label}"

                self.lcd.text_pixels(line, clear_screen=False, x=10, y=y_pos, text_color='black')
                y_pos += 15
                i += 1

            self.lcd.update()

            if self.btn.up:
                selector -= 1
                if selector < 0:
                    selector = len(fields) - 1
                time.sleep(0.05)

            elif self.btn.down:
                selector += 1
                if selector >= len(fields):
                    selector = 0
                time.sleep(0.05)

            elif self.btn.left:
                if selector == 0:
                    hour -= 1
                    if hour < 0:
                        hour = 23
                elif selector == 1:
                    minute -= 1
                    if minute < 0:
                        minute = 59
                elif selector == 2:
                    siren_index -= 1
                    if siren_index < 0:
                        siren_index = len(siren_names) - 1
                elif selector == 3:
                    challenge_amount -= 1
                    if challenge_amount < 1:
                        challenge_amount = 1
                time.sleep(0.05)

            elif self.btn.right:
                if selector == 0:
                    hour += 1
                    if hour > 23:
                        hour = 0
                elif selector == 1:
                    minute += 1
                    if minute > 59:
                        minute = 0
                elif selector == 2:
                    siren_index += 1
                    if siren_index >= len(siren_names):
                        siren_index = 0
                elif selector == 3:
                    challenge_amount += 1
                    if challenge_amount > 10:
                        challenge_amount = 10
                time.sleep(0.05)

            elif self.btn.enter:
                if selector == 4:
                    alarm_time = f"{hour:02}:{minute:02}"
                    siren = siren_names[siren_index]
                    if existing_alarm is not None:
                        self.alarms.remove(existing_alarm)
                    new_alarm = Alarm(alarm_time, siren, challenge_amount)
                    self.alarms.append(new_alarm)

                    self.clear_screen()
                    self.lcd.text_pixels("Alarm Added!", clear_screen=False, x=10, y=20, text_color='black')
                    self.lcd.text_pixels(new_alarm.alarm_description(), clear_screen=False, x=10, y=40, text_color='black')
                    self.lcd.update()

                    self.sound.beep()
                    time.sleep(1)
                    self.state = State.IDLE

                elif selector == 5:
                    self.state = State.IDLE

                time.sleep(0.05)

    def edit_alarm(self):
        if len(self.alarms) == 0:
            self.lcd.clear()
            self.lcd.text_pixels("== Edit Alarm ==", clear_screen=False, x=10, y=10, text_color='black')
            self.lcd.text_pixels("No alarms set", clear_screen=False, x=10, y=35, text_color='black')
            self.lcd.update()

            while not self.btn.enter:
                time.sleep(0.05)
            
            self.state = State.IDLE
            return

        selector = 0

        while self.state == State.EDITING:
            self.clear_screen()
            self.lcd.text_pixels("Select Alarm", clear_screen=False, x=10, y=10, text_color='black')

            y_pos = 30
            i = 0
            while i < len(self.alarms):
                alarm = self.alarms[i]
                line = alarm.alarm_description()

                if i == selector:
                    line = ">> " + line
                else:
                    line = "   " + line

                self.lcd.text_pixels(line, clear_screen=False, x=10, y=y_pos, text_color='black')
                y_pos += 15
                i += 1

            self.lcd.text_pixels("   Back", clear_screen=False, x=10, y=y_pos + 5, text_color='black')
            if selector == len(self.alarms):
                self.lcd.text_pixels(">> Back", clear_screen=False, x=10, y=y_pos + 5, text_color='black')

            self.lcd.update()

            if self.btn.up:
                selector -= 1
                if selector < 0:
                    selector = len(self.alarms)
                time.sleep(0.2)

            elif self.btn.down:
                selector += 1
                if selector > len(self.alarms):
                    selector = 0
                time.sleep(0.2)

            elif self.btn.enter:
                if selector == len(self.alarms):
                    self.state = State.IDLE
                    return
                else:
                    selected_alarm = self.alarms[selector]
                    self.alarm_editor(existing_alarm=selected_alarm)
                    return
    
    def view_alarms(self):
        while self.state == State.VIEW:
            self.clear_screen()
            self.lcd.text_pixels("Alarms", 10, 10)

            y_pos = 40
            i = 0

            while i < len(self.alarms):
                alarm = self.alarms[i]
                
                self.lcd.text_pixels(alarm.alarm_description(), clear_screen=False, x=10, y=40, text_color='black')

                y += 20
                i += 1

            if len(self.alarms) == 0:
                self.lsd.text_pixels("No alarms set", clear_screen=False, x=10, y=40, text_color='black')

            self.lds.update()

            time.wait(0.2)

alarm_bot = AlarmBot()

alarm_bot.sound.beep()

time.sleep(0.5)

alarm_bot.sound.beep()

while True:
    if alarm_bot.state == State.IDLE:
        alarm_bot.main_menu()

    elif alarm_bot.state == State.SETTING:
        alarm_bot.alarm_editor()

    elif alarm_bot.state == State.EDITING:
        alarm_bot.edit_alarm()

    elif alarm_bot.state == State.VIEW:
        alarm_bot.view_alarms()

    elif alarm.state == State.CHALLENGE:
        pass

    else:
        print("How are you seeing this?")

    time.sleep(.2)