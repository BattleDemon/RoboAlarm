#!/usr/bin/env python3

# === Import === 
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
import time
import random

# Set font for UI (Used for all print to lcd)
os.system('setfont Lat15-TerminusBold16')

# == State Enum == 
# Controls the state/mode/ui the robot is currenly doing
class State(Enum):
    IDLE = 0        # Main Menu
    SETTING = 1     # Creating and editing alarms
    EDITING = 2     # Selecting what alarm to edit
    CHALLENGE = 3   # Alarm is ringing, need to complete challenges
    VIEW = 4        # Viewing existing alarms

# == Challenge Types Enum ==
class Challenge_types(Enum):
    LEDMEMORYGAME = 0
    MOTORCONTROLTEST = 1
    COLOURRECOGNITION = 2
    DISTANCECHALLENGE = 3
    GYROCOORDINATION = 4

# == Siren Sounds ==
SIRENS = {
    "test1" : {},
    "test2" : {},
    "test3" : {}
}

# Debug mode to speed up countdown (1 second = 1 minute)
FASTMODE = False

# == Alarm Class ==
# Stores a single alarm instance, and handles its logic
class Alarm():
    def __init__(self, owner, target_time, siren, challenge_amount): 
        self.owner = owner      # Reference to AlarmBot
        self.sound = Sound()
        self.siren = siren
        self.target_time = target_time
        self.challenge_amount = challenge_amount

        # Split time into usable integers 
        self.target_hour, self.target_minute = self.target_time.split(":")
        self.target_hour = int(self.target_hour)
        self.target_minute = int(self.target_minute)

        # Thread that handles countdown in background
        self.countdown_thread = Thread(target=self.countdown)
        self.countdown_thread.daemon = True
        self.countdown_thread.start()

        # Thread for alarm ringing
        self.ring_thread = Thread(target=self.ring)
        self.ring_thread.daemon = True
        self.ringing = False

    def ring(self):
        # Switches AlarmBot into challange mode
        self.owner.active_alarm = self
        self.owner.state = State.CHALLENGE
        self.ringing = True

        # Loop until challenges are complete
        while self.ringing:
            self.sound.beep()
            time.sleep(0.3)

    def remake_target_time(self):
        # Remakes the string of time after initial make (because of countdown) and for viewing and editing
        self.target_time = "{}:{}".format(self.target_hour,self.target_minute)

    def countdown(self):
        minutes_pased = 0

        while True:
            # When timer ends it triggers the alarm
            if self.target_hour == 0 and self.target_minute == 0:
                self.ring_thread.start()
                break

            self.target_minute -= 1 
            minutes_pased += 1

            # Rolls over hour
            if minutes_pased == 60:
                minutes_pased = 0
                self.target_hour -= 1
                if self.target_hour < 0:
                    self.target_hour = 0

            # Fast debugging / testing mode and real time
            if FASTMODE:
                time.sleep(1)
            else:
                time.sleep(60)

    def alarm_description(self):
        # Used for displating alarm info in menus 
        self.remake_target_time()
        return " {} | {} | {} Challenges".format(self.target_time, self.siren, self.challenge_amount)

# == Challenge Class ==
class Challenge():
    def __init__(self,owner, challenge_type=Challenge_types):
        self.type = challenge_type
        self.owner = owner

    def run(self):
        # Runs correct challenge from type
        if self.type == Challenge_types.LEDMEMORYGAME:
            return self.led_memory_game()
        elif self.type == Challenge_types.MOTORCONTROLTEST:
            return self.motor_control_test()
        elif self.type == Challenge_types.COLOURRECOGNITION:
            return self.colour_recognition()
        elif self.type == Challenge_types.DISTANCECHALLENGE:
            return self.distance_challenge()
        elif self.type == Challenge_types.GYROCOORDINATION:
            return self.gyro_coordination()

    def led_memory_game(self):
        # Memory game: USer must repeat the shown sequence

        # Only able to use these LEDS/Buttons
        led_buttons = ["LEFT","RIGHT"]

        sequence_amount = random.randint(3,6)
        led_sequence = []

        i = 0
        while i < sequence_amount:
            i += 1
            led = random.choice(led_buttons)
            led_sequence.append(led)

        while True:
            # Display instructions
            self.owner.lcd.text_pixels("== LED GAME ==", clear_screen=False, x=10, y=20, text_color='black')
            self.owner.lcd.text_pixels("Watch the LED's", clear_screen=False, x=10, y=40, text_color='black')
            self.owner.lcd.text_pixels("Remember the order", clear_screen=False, x=10, y=60, text_color='black')
            self.owner.lcd.update()

            # Show sequence
            for i in led_sequence:
                self.owner.led.set_color(i,'AMBER')
                time.sleep(0.75)
                self.owner.led.set_color(i,'BLACK')
                time.sleep(0.25)

            # Display other instructions
            self.owner.lcd.text_pixels("== LED GAME ==", clear_screen=True, x=10, y=20, text_color='black')
            self.owner.lcd.text_pixels("Press the Buttons in \n the order shown", clear_screen=False, x=10, y=40, text_color='black')
            self.owner.lcd.update()

            try_sequence = []
            pressed = 0

            while pressed < sequence_amount:
                if self.owner.btn.left:
                    try_sequence.append("LEFT")
                    pressed += 1
                    self.owner.btn.wait_for_released('LEFT')
                if self.owner.btn.right:
                    try_sequence.append("RIGHT")
                    pressed += 1
                    self.owner.btn.wait_for_released('RIGHT')

                time.sleep(0.2)

            # Check correct
            if try_sequence == led_sequence:
                # Show correct message
                self.owner.lcd.text_pixels("== LED GAME ==", clear_screen=True, x=10, y=20, text_color='black')
                self.owner.lcd.text_pixels("Correct", clear_screen=False, x=10, y=40, text_color='black')
                self.owner.lcd.update()

                time.sleep(1)
                return True
            else:
                # Show fail message
                self.owner.lcd.text_pixels("== LED GAME ==", clear_screen=True, x=10, y=20, text_color='black')
                self.owner.lcd.text_pixels("Wrong Try Again", clear_screen=False, x=10, y=40, text_color='black')
                self.owner.lcd.update()
                
                # Loop again if wrong
                time.sleep(1)

    def motor_control_test(self):
        # User must match and hold a specific motor speed
        target_speed = random.randint(300, 750)
        tolerance = 75
        hold_time = 3 

        start_time = None

        while True:
            current_speed = self.owner.lm.speed
            current_speed = abs(int(current_speed))

            # Display instructions
            self.owner.lcd.text_pixels("== MOTOR TEST ==", clear_screen=True, x=10, y=20, text_color='black')
            self.owner.lcd.text_pixels("Target: {} +/- {}".format(target_speed, tolerance), clear_screen=False, x=10, y=40, text_color='black')
            self.owner.lcd.text_pixels("Speed: {}".format(current_speed), clear_screen=False, x=10, y=60, text_color='black')
            self.owner.lcd.text_pixels("Hold that speed for 3 seconds", clear_screen=False, x=10, y=80, text_color='black')
            self.owner.lcd.update()

            # Check if speed is in correct range
            if abs(current_speed - target_speed) <= tolerance:
                if start_time is None:
                    start_time = time.time()

                if time.time() - start_time >= hold_time:
                    # Show success message
                    self.owner.sound.beep()
                    self.owner.lcd.text_pixels("Complete", clear_screen=False, x=10, y=80, text_color='black')
                    self.owner.lcd.update()

                    time.sleep(3)
                    return True
                
            else:
                # Reset timer if out of range
                start_time = None 

            time.sleep(0.3)

    def gyro_coordination(self):
        # User must follow a changing angle
        tolerance = 5
        duration = 5

        start_time = time.time()
        target = random.randint(-90, 90)
        last_change = time.time()

        while True:
            angle = self.owner.gy.angle

            # Target changes ever second
            if time.time() - last_change >= 1:
                change = random.randint(-20,20)
                target += change
                last_change = time.time()

            # Display instructions
            self.owner.lcd.text_pixels("== FOLLOW ANGLE ==", clear_screen=True, x=10, y=20, text_color='black')
            self.owner.lcd.text_pixels("Target: {}".format(target), clear_screen=False, x=10, y=40, text_color='black')
            self.owner.lcd.text_pixels("Angle: {}".format(int(angle)), clear_screen=False, x=10, y=60, text_color='black')
            self.owner.lcd.update()

            # If user is not in range tell them and reset
            if abs(angle - target) > tolerance:
                self.owner.lcd.text_pixels("Not close enough", clear_screen=False, x=10, y=80, text_color='black')
                self.owner.lcd.update()

                time.sleep(1)
                start_time = time.time()
                target = random.randint(-90, 90)
                last_change = time.time()

            # Stayed within range and display message
            if time.time() - start_time >= duration:
                self.owner.lcd.text_pixels("== FOLLOW ANGLE ==", clear_screen=True, x=10, y=20, text_color='black')
                self.owner.lcd.text_pixels("Followed Correctly", clear_screen=False, x=10, y=60, text_color='black')
                self.owner.lcd.update()

                time.sleep(1)

                return True

            time.sleep(0.2)

    def colour_recognition(self):
        # User must show correct colour to sensor
        colours = [
            "Black",
            "Blue",
            "Green",
            "Yellow",
            "Red",
            "White",
            "Brown"
        ]

        target = random.choice(colours)
        last_reroll_time = time.time()

        while True:
            detected = self.owner.cs.color_name

            # Display Instructions
            self.owner.lcd.text_pixels("== COLOUR TEST ==", clear_screen=True, x=10, y=20, text_color='black')
            self.owner.lcd.text_pixels("Target: {}".format(target), clear_screen=False, x=10, y=40, text_color='black')
            self.owner.lcd.text_pixels("Seen: {}".format(detected), clear_screen=False, x=10, y=60, text_color='black')
            self.owner.lcd.text_pixels("Back Touch Sensor = confirm", clear_screen=False, x=10, y=80, text_color='black')
            self.owner.lcd.text_pixels("Press enter to reroll \nonly after 10 seconds", clear_screen=False, x=10, y=90, text_color='black')
            self.owner.lcd.update()

            # Confirm with touch sensor (so you can't just wave the sensor around until it detects correct)
            if self.owner.ts.is_pressed:
                if detected == target:
                    self.owner.lcd.text_pixels("== COLOUR TEST ==", clear_screen=True, x=10, y=20, text_color='black')
                    self.owner.lcd.text_pixels("Correct", clear_screen=False, x=10, y=80, text_color='black')
                    self.owner.lcd.update()

                    time.sleep(1)
                    return True

            # Reroll after delay (incase no colour near) but not availble until 10 seconds 
            if self.owner.btn.enter:
                if time.time() - last_reroll_time >= 10:
                    target = random.choice(colours)
                    last_reroll_time = time.time()

            time.sleep(0.1)

    def distance_challenge(self):
        # User must position alarm at correct distance
        target = random.randint(10, 50)  
        tolerance = 3

        while True:
            distance = self.owner.uss.distance_centimeters
            distance = int(distance)

            # Display instructions
            self.owner.lcd.text_pixels("== DISTANCE ==", clear_screen=True, x=10, y=20, text_color='black')
            self.owner.lcd.text_pixels("Target: {}cm".format(target), clear_screen=False, x=10, y=40, text_color='black')
            self.owner.lcd.text_pixels("Now: {}cm".format(distance), clear_screen=False, x=10, y=60, text_color='black')
            self.owner.lcd.text_pixels("Back Touch Sensor = confirm", clear_screen=False, x=10, y=80, text_color='black')
            self.owner.lcd.update()

            # Confirm same way as colour
            if self.owner.ts.is_pressed:
                if abs(distance - target) <= tolerance:
                    self.owner.sound.beep()
                    self.owner.lcd.text_pixels("== DISTANCE ==", clear_screen=True, x=10, y=20, text_color='black')
                    self.owner.lcd.text_pixels("Correct", clear_screen=False, x=10, y=60, text_color='black')
                    self.owner.lcd.update()

                    time.sleep(3)

                    return True

            time.sleep(0.1)

# == Alarm Bot ==
# Main controller that handles UI, Sensors, and the state
class AlarmBot():
    def __init__(self):

        self.state = State.IDLE

        self.led = Leds()
        self.lcd = Display()
        self.btn = Button()
        self.sound = Sound()

        self.lm = LargeMotor()
        self.lm.stop(stop_action='coast')
    
        self.uss = UltrasonicSensor()
        self.cs = ColorSensor()
        self.gy = GyroSensor()
        self.ts = TouchSensor()

        # Alarms
        self.alarms = [Alarm(self,"00:02","test1",4)]
        self.active_alarm = None

        # Challenges and Menu Options in Main
        self.challenges = []
        self.menu_items = ["Set Alarm", "Edit Alarm", "View Alarms"]

    def clear_screen(self):
        # Helper to clear screens quicker
        self.lcd.clear()

    def change_state(self, selection=None, sub_menu=None):
        # Handles transition between modes from menu input
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

        while self.state == State.IDLE:
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
            self.state = State.SETTING
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
                    value = "{:02d}".format(hour)
                elif label == "Minute":
                    value = "{:02d}".format(minute)
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
                    line = "{}{}: {}".format(prefix,label,value)
                else:
                    line = "{}{}".format(prefix,label)

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
                    alarm_time = "{:02d}:{:02d}".format(hour,minute)
                    siren = siren_names[siren_index]
                    if existing_alarm is not None:
                        self.alarms.remove(existing_alarm)
                    new_alarm = Alarm(self,alarm_time, siren, challenge_amount)
                    self.alarms.append(new_alarm)

                    self.clear_screen()
                    self.lcd.text_pixels("Alarm Added", clear_screen=False, x=10, y=20, text_color='black')
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

            time.sleep(0.05)
    
    def view_alarms(self):
        while self.state == State.VIEW:
            self.clear_screen()
            self.lcd.text_pixels("Alarms", 10, 10)

            y_pos = 40
            i = 0

            while i < len(self.alarms):
                alarm = self.alarms[i]
                
                self.lcd.text_pixels(alarm.alarm_description(), clear_screen=False, x=10, y=y_pos, text_color='black')

                y_pos += 20
                i += 1

            if len(self.alarms) == 0:
                self.lcd.text_pixels("No alarms set", clear_screen=False, x=10, y=40, text_color='black')

            if self.btn.enter:
                self.state = State.IDLE
                return

            self.lcd.update()

            time.sleep(0.2)

    def randomise_challenges(self):
        challenge_amount = self.active_alarm.challenge_amount
        challenges = []

        for i in range(challenge_amount):
            challenge_type = random.choice(list(Challenge_types))
            challenges.append(Challenge(self,challenge_type))

        return challenges

    def challenge_active(self):
        challenges = self.randomise_challenges()
        #challenges = [Challenge(self,Challenge_types.MOTORCONTROLTEST)]

        for challenge in challenges:
            success = False

            while not success:
                self.clear_screen()
                self.lcd.update()

                success = challenge.run()

        self.active_alarm.ringing = False
        self.active_alarm = None
        self.state = State.IDLE

alarm_bot = AlarmBot()
alarm_bot.sound.beep()
time.sleep(0.5)
alarm_bot.sound.beep()

# == Main loop ==
while True:
    if alarm_bot.state == State.IDLE:
        alarm_bot.main_menu()

    elif alarm_bot.state == State.SETTING:
        alarm_bot.alarm_editor()

    elif alarm_bot.state == State.EDITING:
        alarm_bot.edit_alarm()

    elif alarm_bot.state == State.VIEW:
        alarm_bot.view_alarms()

    elif alarm_bot.state == State.CHALLENGE:
        alarm_bot.challenge_active()

    else:
        print("How are you seeing this?")

    time.sleep(.2)


    #future ideas
    #   Save alarms (json)
    #   Snooze for 5 minutes but after it increases challange amount by 2 and only usable once
    #   Add more alarm sirens then just beep
    #   A way to delete alarms
    #   Show remaining challenges