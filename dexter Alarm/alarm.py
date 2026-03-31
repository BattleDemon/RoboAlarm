#!/usr/bin/env python3

# === Import === 
# EV3 Imports
from ev3dev2.sensor import INPUT_2, INPUT_3, INPUT_4,  INPUT_1
from ev3dev2.sensor.lego import *
from ev3dev2.motor import *
from ev3dev2.sound import *
from ev3dev2.button import *
from ev3dev2.display import *
from ev3dev2.fonts import *
from ev3dev2.led import Leds
# Other Imports
from enum import Enum
from datetime import datetime
from threading import *
import os
import time
import random

# Tim did you know you can make angry comments?
# !Angry ( On my theme this appears red) it might not be angry on yours, if so that is sad

# It turns out there are other types 

# Normal 
# !Angry
# *Calm
# ?Sad

# Using helvB14 causes a massive latency or similar spike,
# my theory is it loads the font from memory for each text pixel to screen instead of saving a local address (a lot of compute for little)
USEFONT = None #'helvB14'

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

# This could of also been an enum but i have already writen things that need it to be a dictionary so it will stay a dictionary
# == Siren Sounds ==
SIRENS = {
    "test1" : {}, # IDK what to name these alarms 
    "test2" : {},
    "test3" : {},
    'other' : {}
}

# Debug mode to speed up countdown (1 second = 1 minute)
FASTMODE = True

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
        # Checks if an alarm is already running if so put this in que
        if self.owner.active_alarm is not None:
            self.owner.alarms_que = self
            return
        else:
            self.owner.active_alarm = self
            if self.owner.state == State.CHALLENGE:
                # This is needed because it checks if there a multiple alarms before leaving the challenge func (before state.IDLE),
                # meaning if i were to just change the state to challenge it would not run the challenges
                self.owner.challenge_active()
            else:
                self.owner.state = State.CHALLENGE
            self.ringing = True

        # Loop until challenges are complete
        while self.ringing:
            if self.siren == "test1":
                self.sound.beep()
                self.sound.beep()
                time.sleep(0.25)
                self.sound.beep()
                time.sleep(0.5)

            elif self.siren == "test2":
                self.sound.beep()
                self.sound.beep()
                time.sleep(0.1)
                self.sound.beep()
                self.sound.beep()
                time.sleep(0.1)
                self.sound.beep()
                time.sleep(0.5)
        
            elif self.siren == "test3":
                self.sound.beep()
                self.sound.beep()
                time.sleep(0.25)
                self.sound.beep()
                time.sleep(0.5)
                self.sound.beep()
                self.sound.beep()
                time.sleep(0.1)
                self.sound.beep()
                self.sound.beep()
                time.sleep(0.1)
                self.sound.beep()
                time.sleep(0.5)

            else:
                self.sound.beep()
                time.sleep(0.3)

    def remake_target_time(self):
        # Remakes the string of time after initial make (because of countdown) and for viewing and editing
        self.target_time = "{}:{}".format(self.target_hour,self.target_minute)

    def countdown(self):
        while True:
            # When timer ends it triggers the alarm
            if self.target_hour == 0 and self.target_minute == 0:
                self.ring_thread.start()
                break
            
            # Handle hours 
            if self.target_minute == 0:
                self.target_hour -= 1
                self.target_minute = 60

            # Countdown minute
            self.target_minute -= 1

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
        self.owner = owner  # Refrence to the alarmbot

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

        # Randomises the amount of elements in the order
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
            self.owner.update()

            # Show sequence
            for i in led_sequence:
                self.owner.led.set_color(i,'AMBER')
                time.sleep(0.75)
                self.owner.led.set_color(i,'BLACK')
                time.sleep(0.25)

            # Display other instructions
            self.owner.lcd.text_pixels("== LED GAME ==", clear_screen=True, x=10, y=20, text_color='black')
            self.owner.lcd.text_pixels("Press the Buttons in \n the order shown", clear_screen=False, x=10, y=40, text_color='black')
            self.owner.update()

            try_sequence = []
            pressed = 0

            # Get the users input sequence
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
                self.owner.update()

                time.sleep(1)
                return True
            else:
                # Show fail message
                self.owner.lcd.text_pixels("== LED GAME ==", clear_screen=True, x=10, y=20, text_color='black')
                self.owner.lcd.text_pixels("Wrong Try Again", clear_screen=False, x=10, y=40, text_color='black')
                self.owner.update()
                
                # Loop again if wrong
                time.sleep(1)

    def motor_control_test(self):
        # User must match and hold a specific motor speed
        target_speed = random.randint(250, 550)
        tolerance = 100
        hold_time = 3 

        start_time = None

        while True:
            current_speed = self.owner.lm.speed
            current_speed = abs(int(current_speed)) # Get speed ingnore forward or back

            # Display instructions
            self.owner.lcd.text_pixels("== MOTOR TEST ==", clear_screen=True, x=10, y=20, text_color='black')
            self.owner.lcd.text_pixels("Target: {} +/- {}".format(target_speed, tolerance), clear_screen=False, x=10, y=40, text_color='black')
            self.owner.lcd.text_pixels("Speed: {}".format(current_speed), clear_screen=False, x=10, y=60, text_color='black')
            self.owner.lcd.text_pixels("Hold that speed for 3 seconds", clear_screen=False, x=10, y=80, text_color='black')
            self.owner.update()

            # Check if speed is in correct range
            if abs(current_speed - target_speed) <= tolerance:
                if start_time is None:
                    start_time = time.time()

                if time.time() - start_time >= hold_time:
                    # Show success message
                    self.owner.sound.beep()
                    self.owner.lcd.text_pixels("Complete", clear_screen=False, x=10, y=80, text_color='black')
                    self.owner.update()

                    time.sleep(3)
                    return True
                
            else:
                # Reset timer if out of range
                start_time = None 

            time.sleep(0.3)

    def gyro_coordination(self):
        # Gyro tolerance 
        tolerance = 2
        target_angle = random.randint(-60,60) # Ransomise the angle 

        remaining = 3 # Have to do more than one 

        self.owner.gy.reset()

        # Loops while you havent done all 3
        while remaining > 0:
            # Updates the angle
            angle = self.owner.gy.angle

            # Ui and Instructions
            self.owner.lcd.text_pixels("== Match Angle ==", clear_screen=True, x=10, y=20, text_color='black')
            self.owner.lcd.text_pixels("Target: {}".format(target_angle), clear_screen=False, x=10, y=40, text_color='black')
            self.owner.lcd.text_pixels("Angle: {}".format(int(angle)), clear_screen=False, x=10, y=60, text_color='black')
            self.owner.update()

            # Check if the angle is in range
            if abs(angle - target_angle) <= tolerance:
                self.owner.lcd.text_pixels("== Match Angle ==", clear_screen=True, x=10, y=20, text_color='black')
                self.owner.lcd.text_pixels("Good", clear_screen=False, x=10, y=60, text_color='black')
                self.owner.update()

                time.sleep(2)

                # Reduces the remaining angles and randomises
                remaining -= 1
                target_angle = random.randint(-60,60)

        return True

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

        # Randomises the target colour and sets the reroll time
        target = random.choice(colours)
        last_reroll_time = time.time()

        # Loops
        while True:
            # Get the detected colour
            detected = self.owner.cs.color_name 

            # Display Instructions
            self.owner.lcd.text_pixels("== COLOUR TEST ==", clear_screen=True, x=10, y=20, text_color='black')
            self.owner.lcd.text_pixels("Target: {}".format(target), clear_screen=False, x=10, y=40, text_color='black')
            self.owner.lcd.text_pixels("Seen: {}".format(detected), clear_screen=False, x=10, y=60, text_color='black')
            self.owner.lcd.text_pixels("Back Touch Sensor = confirm", clear_screen=False, x=10, y=80, text_color='black')
            self.owner.lcd.text_pixels("Press enter to reroll \nonly after 10 seconds", clear_screen=False, x=10, y=90, text_color='black')
            self.owner.update()

            # Confirm with touch sensor (so you can't just wave the sensor around until it detects correct)
            if self.owner.ts.is_pressed:
                # Checks if the colour is correct 
                if detected == target:
                    self.owner.lcd.text_pixels("== COLOUR TEST ==", clear_screen=True, x=10, y=20, text_color='black')
                    self.owner.lcd.text_pixels("Correct", clear_screen=False, x=10, y=80, text_color='black')
                    self.owner.update()

                    time.sleep(1)
                    return True

            # Reroll after delay (incase no colour near) but not availble until 10 seconds 
            if self.owner.btn.enter:
                # Checks if the time has elapsed 
                if time.time() - last_reroll_time >= 10:
                    # Randomised colour and resets the time
                    target = random.choice(colours)
                    last_reroll_time = time.time() 

            time.sleep(0.1)

    def distance_challenge(self):
        # User must position alarm at correct distance
        target = random.randint(10, 50)  
        tolerance = 3

        while True:
            # Updates the current distance
            distance = self.owner.uss.distance_centimeters
            # Rounds from a float to an int
            distance = int(distance)

            # Display instructions
            self.owner.lcd.text_pixels("== DISTANCE ==", clear_screen=True, x=10, y=20, text_color='black')
            self.owner.lcd.text_pixels("Target: {}cm".format(target), clear_screen=False, x=10, y=40, text_color='black')
            self.owner.lcd.text_pixels("Now: {}cm".format(distance), clear_screen=False, x=10, y=60, text_color='black')
            self.owner.lcd.text_pixels("Back Touch Sensor = confirm", clear_screen=False, x=10, y=80, text_color='black')
            self.owner.update()

            # Confirm same way as colour
            if self.owner.ts.is_pressed:
                # Check if it is in the correct range
                if abs(distance - target) <= tolerance:
                    self.owner.sound.beep()
                    self.owner.lcd.text_pixels("== DISTANCE ==", clear_screen=True, x=10, y=20, text_color='black')
                    self.owner.lcd.text_pixels("Correct", clear_screen=False, x=10, y=60, text_color='black')
                    self.owner.update()

                    time.sleep(3)

                    return True

            time.sleep(0.1)

# == Alarm Bot ==
# Main controller that handles UI, Sensors, and the state
class AlarmBot():
    def __init__(self):

        # Set the menu state into idle
        self.state = State.IDLE

        # Initialise all the used Motors, Sensors, and inputs/outputs
        self.led = Leds()
        self.lcd = Display()
        self.btn = Button()
        self.sound = Sound()

        self.lm = LargeMotor()
        self.lm.stop(stop_action='coast') # Makes easier to turn (for Motor Challenge)
    
        self.uss = UltrasonicSensor()
        self.cs = ColorSensor()
        self.gy = GyroSensor()
        self.ts = TouchSensor()

        # Alarms
        self.alarms = [Alarm(self,"01:00","test1",1)] 
        self.alarms_que = []
        self.active_alarm = None

        # Challenges and Menu Options in Main
        self.challenges = [] # IDk why i didn't make this a local variable
        self.menu_items = ["Set Alarm", "Edit Alarm", "View Alarms"] # same with this. But its done now why change

    def clear_screen(self):
        # Helper to clear screens quicker 
        self.lcd.clear()

    def update(self):
        # Helper to update screen quicker 
        self.lcd.update()

    def change_state(self, selection=None, sub_menu=None):
        # My original plan for this was to use it as a form of controller but aside from the main menu, 
        # I ended up just changing the state and putting this inside a while in correct state

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
        # Tracks which menu item is selected acts as a cursor
        selector = 0

        # Breaks out when not in idle such as when alrms ring
        while self.state == State.IDLE:
            self.clear_screen()

            # Print Title
            self.lcd.text_pixels("== RoboAlarm ==", clear_screen=False, x=10, y=20, text_color='black',font=USEFONT)

            # Y Position for ui and current index
            y_pos = 35
            i = 0

            # Draw menu items with selection indicator
            while i < len(self.menu_items):
                text = self.menu_items[i]

                # add selector
                if i == selector:
                    text = ">> " + text
                else:
                    text = "   " + text

                self.lcd.text_pixels(text,clear_screen=False, x=10, y=y_pos, text_color='black',font=USEFONT)

                # Increment y position and index
                y_pos += 15 
                i += 1 
            
            self.update() # Update UI

            # Navigation logic
            if self.btn.up:
                selector -= 1
                if selector < 0:
                    # Wrap around
                    selector = len(self.menu_items) - 1 

            if self.btn.down:
                selector += 1
                if selector > len(self.menu_items):
                    # Wrap around
                    selector = 0 

            # Selection confirmation
            if self.btn.enter:
                self.change_state(selection=selector)

            # Allow a way for the fast mode to be turned on while running
            if self.ts.pressed:
                start_time = time.time()

                ts.wait_for_released()

                # Only changes if held touch sensor for 5 seconds 
                if time.time() - start_time <= 5:
                    FASTMODE = not FASTMODE 

            time.sleep(0.1)

    def alarm_editor(self, existing_alarm=None):
        # Get possible siren option 
        siren_names = list(SIRENS.keys())

        # Initialise values depending on if create or edit
        if existing_alarm is None:
            hour = 8 # Since its a countdown now the alarm is initialy set to the required sleep for an adult
            minute = 0
            siren_index = 0
            challenge_amount = 1
            title = "== Set Alarm =="

        else:
            # Loads values from existing alarm
            self.state = State.SETTING
            hour_str, minute_str = existing_alarm.target_time.split(":")
            # Turn from a string into an Int
            hour = int(hour_str)
            minute = int(minute_str)

            # Get the siren index (this is why it can't be a bool)
            siren_index = siren_names.index(existing_alarm.siren)

            challenge_amount = existing_alarm.challenge_amount
            title = "== Edit Alarm =="

        # Editable fields 
        fields = ["Hour", "Minute", "Siren", "Challenges", "Save", "Cancel"]
        selector = 0

        # Editing Loop
        while self.state == State.SETTING:
            # Clear screen then display title
            self.clear_screen()
            self.lcd.text_pixels(title, clear_screen=False, x=10, y=10, text_color='black',font=USEFONT)

            # Set y position and index
            y_pos = 30
            i = 0

            # Show each fields current value
            while i < len(fields):
                label = fields[i]

                # Update all the elements to show their values
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

                # Show current field
                if i == selector:
                    prefix = ">> "
                else:
                    prefix = "   "

                # Add things to gether if needed
                if value != "":
                    line = "{}{}: {}".format(prefix,label,value)
                else:
                    line = "{}{}".format(prefix,label)

                # Display line 
                self.lcd.text_pixels(line, clear_screen=False, x=10, y=y_pos, text_color='black',font=USEFONT)

                # Increment the y position and index
                y_pos += 15
                i += 1

            # Display UI to screen
            self.update()

            # Move selction up/down
            if self.btn.up:
                selector -= 1
                if selector < 0:
                    # Wrap around
                    selector = len(fields) - 1

            elif self.btn.down:
                selector += 1
                if selector >= len(fields):
                    # Wrap around
                    selector = 0

            # Modify selected value (down)
            elif self.btn.left:
                if selector == 0:
                    hour -= 1
                    if hour < 0:
                        # Wrap around to full day
                        hour = 24

                elif selector == 1:
                    minute -= 1
                    if minute < 0:
                        # Wrap around to end of hour
                        minute = 59

                elif selector == 2:
                    siren_index -= 1
                    if siren_index < 0:
                        # Wrap around to last siren
                        siren_index = len(siren_names) - 1

                elif selector == 3:
                    challenge_amount -= 1
                    if challenge_amount < 1:
                        # Set minimum challenge amount
                        challenge_amount = 1

            # Modify selected value (up)
            elif self.btn.right:
                if selector == 0:
                    hour += 1
                    if hour > 24:
                        # Wrap around to no hours
                        hour = 0 

                elif selector == 1:
                    minute += 1
                    if minute > 59:
                        # Wrap to no minutes
                        minute = 0

                elif selector == 2:
                    siren_index += 1
                    if siren_index >= len(siren_names):
                        siren_index = 0

                elif selector == 3:
                    challenge_amount += 1
                    if challenge_amount > 10:
                        # Cap challenge amount to 10
                        challenge_amount = 10

            elif self.btn.enter:
                if selector == 4:
                    # Save alarm (create or replace)
                    alarm_time = "{:02d}:{:02d}".format(hour,minute)
                    siren = siren_names[siren_index]

                    # Remove the old version of the alarm
                    if existing_alarm is not None:
                        self.alarms.remove(existing_alarm)

                    # Save the configured infromation as a new alarm then push to the list
                    new_alarm = Alarm(self,alarm_time, siren, challenge_amount)
                    self.alarms.append(new_alarm)

                    # Show added
                    self.clear_screen()
                    self.lcd.text_pixels("Alarm Added", clear_screen=False, x=10, y=20, text_color='black',font=USEFONT)
                    self.lcd.text_pixels(new_alarm.alarm_description(), clear_screen=False, x=10, y=40, text_color='black',font=USEFONT)
                    self.update()

                    self.sound.beep()
                    time.sleep(1)

                    # Return to main menu
                    self.state = State.IDLE 

                elif selector == 5:
                    # Cancel 
                    self.state = State.IDLE

            time.sleep(0.1)

    def edit_alarm(self):
        # Handle if no alrm exists
        if len(self.alarms) == 0:
            # Clear screen and set Ui
            self.lcd.clear()
            self.lcd.text_pixels("== Edit Alarm ==", clear_screen=False, x=10, y=10, text_color='black',font=USEFONT)
            self.lcd.text_pixels("No alarms set", clear_screen=False, x=10, y=35, text_color='black',font=USEFONT)
            self.update()

            # Wait until user leaves
            while not self.btn.enter:
                time.sleep(0.05)
            
            # Return to main menu
            self.state = State.IDLE
            return

        # Create the cursor 
        selector = 0

        # Loops while still editing, breaks if state chnages (alarm goes off or other)
        while self.state == State.EDITING:
            # Clear then add UI
            self.clear_screen()
            self.lcd.text_pixels("Select Alarm", clear_screen=False, x=10, y=10, text_color='black')
            self.lcd.text_pixels("Hold Left for 1 second to Delete", clear_screen=False, x=10, y=30, text_color='black', font=USEFONT)

            # Set Y Position and Index
            y_pos = 35
            i = 0

            # Display all alarms
            while i < len(self.alarms):
                # Get the first alarm and its description
                alarm = self.alarms[i]
                line = alarm.alarm_description()

                # Show selections
                if i == selector:
                    line = ">> " + line
                else:
                    line = "   " + line

                # add the alarm and pointer if selected
                self.lcd.text_pixels(line, clear_screen=False, x=10, y=y_pos, text_color='black',font=USEFONT)

                # Increment Y position and index
                y_pos += 15
                i += 1

            # Allow user to leave
            self.lcd.text_pixels("   Back", clear_screen=False, x=10, y=y_pos + 5, text_color='black',font=USEFONT)
            if selector == len(self.alarms):
                self.lcd.text_pixels(">> Back", clear_screen=False, x=10, y=y_pos + 5, text_color='black',font=USEFONT)

            # Display UI
            self.update()

            # Menu navigation
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
                    # Edit selcted alarm
                    selected_alarm = self.alarms[selector]
                    self.alarm_editor(existing_alarm=selected_alarm)
                    return
            
            # Delete Alarm
            elif self.btn.left:
                # Only delete if acutally selecting an alarm
                if selector < len(self.alarms):
                    # Need to hold left for delete
                    pressed_time = time.time()
                    self.btn.wait_for_released('left')
                    end_time = time.time()

                    if end_time - pressed_time >= 1:
                        deleted_alarm = self.alarms.pop(selector)

                        self.clear_screen()
                        self.lcd.text_pixels("Deleted", clear_screen=False, x=10, y=20, text_color='black', font=USEFONT)
                        self.lcd.text_pixels(deleted_alarm.alarm_description(), clear_screen=False, x=10, y=40, text_color='black', font=USEFONT)
                        self.update()

                        self.sound.beep()
                        time.sleep(1)

            time.sleep(0.1)
    
    def view_alarms(self):
        # View all alarms
        while self.state == State.VIEW:
            self.clear_screen()
            self.lcd.text_pixels("== Alarm List ==", 10, 10,font=USEFONT)
            self.lcd.text_pixels(" Press enter to leave", 10, 30)

            y_pos = 45
            i = 0

            # List all alarms
            while i < len(self.alarms):
                alarm = self.alarms[i]
                
                self.lcd.text_pixels(alarm.alarm_description(), clear_screen=False, x=10, y=y_pos, text_color='black',font=USEFONT)

                y_pos += 20
                i += 1

            # If no alarms
            if len(self.alarms) == 0:
                self.lcd.text_pixels("No alarms set", clear_screen=False, x=10, y=40, text_color='black',font=USEFONT)

            # leave
            if self.btn.enter:
                self.state = State.IDLE
                return

            self.update()

            time.sleep(0.1)

    def randomise_challenges(self):
        # Runs challenges untill all are complete
        challenge_amount = self.active_alarm.challenge_amount
        challenges = []

        # Randomise for each challenge its type and add to list
        for i in range(challenge_amount):
            challenge_type = random.choice(list(Challenge_types))
            challenges.append(Challenge(self,challenge_type))

        return challenges 

    def challenge_active(self):
        self.challenges = self.randomise_challenges()
        #challenges = [Challenge(self,Challenge_types.LEDMEMORYGAME)]

        self.lcd.text_pixels("Alarm Ringing", clear_screen=True, x=10, y=20, text_color='black',font=USEFONT)
        self.lcd.text_pixels("Complete Challenges to silence", clear_screen=False, x=10, y=40, text_color='black',font=USEFONT)
        #self.lcd.text_pixels("press any button", clear_screen=False, x=10, y=60, text_color='black',font=USEFONT)
        self.update()

        #self.btn.wait_for_pressed(['up', 'down', 'left', 'right', 'enter'])
        time.sleep(5)

        completed = 0

        for challenge in self.challenges:
            success = False

            while not success:
                self.clear_screen()
                self.update()

                # Although the use of this as a True/False didn't end up happening since i loop in the challenges, i will keep it
                success = challenge.run()
                completed += 1

            self.lcd.text_pixels("== Challenges ==", clear_screen=True, x=10, y=20, text_color='black',font=USEFONT)
            self.lcd.text_pixels("Challenges remaining {}".format(len(self.challenges)-completed), clear_screen=False, x=10, y=40, text_color='black',font=USEFONT)
            #self.lcd.text_pixels("press any button", clear_screen=False, x=10, y=60, text_color='black',font=USEFONT)
            self.update()

            time.sleep(5)
            #self.btn.wait_for_pressed(['up', 'down', 'left', 'right'])


        # Stop alarm when all challenges are complete 
        self.active_alarm.ringing = False
        self.active_alarm = None

        # Make sure there isn't an alarm in the que
        self.check_alarm_que()

        # Returns to main menu
        self.state = State.IDLE

    # Before I was just sleeping for a bit then checking again to handle multiple alarms but i releised this could create a race case if multiple are waiting to ring
    def check_alarm_que(self):
        # Checks if there is a waiting alarm
        if self.alarms_que != []:
            next_alarm = self.alarm_que.pop(0) # Removes it 
            next_alarm.ring_thread.start() # Starts the ringing thread

# == Program Starts ==
alarm_bot = AlarmBot()

# boot sounds
alarm_bot.sound.beep()
time.sleep(0.5)
alarm_bot.sound.beep()

# == Main loop ==
# State machine soft of thing
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