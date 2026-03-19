#!/usr/bin/env python3

from enum import Enum
from datetime import datetime
import os
import time


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


SIRENS = {
    "Classic Beep": "beep",
    "Fast Beep": "fast_beep",
    "Buzz": "buzz"
}


class Alarm:
    def __init__(self, target_time, siren, challenge_amount):
        self.siren = siren
        self.target_time = target_time
        self.challenge_amount = challenge_amount

    def ring(self):
        print(f"\nALARM RINGING: {self.target_time} | {self.siren}")

    def alarm_description(self):
        return f"{self.target_time} | {self.siren} | {self.challenge_amount} Challenges"


class Challenge:
    def __init__(self, challenge_type=Challenge_types.LEDMEMORYGAME):
        self.type = challenge_type

    def run(self):
        if self.type == Challenge_types.LEDMEMORYGAME:
            print("Running LED Memory Game...")
        elif self.type == Challenge_types.MOTORCONTROLTEST:
            print("Running Motor Control Test...")
        elif self.type == Challenge_types.COLOURRECOGNITION:
            print("Running Colour Recognition...")
        elif self.type == Challenge_types.DISTANCECHALLENGE:
            print("Running Distance Challenge...")
        elif self.type == Challenge_types.GYROCOORDINATION:
            print("Running Gyro Coordination...")


class TerminalSound:
    def beep(self):
        print("[BEEP]")


class AlarmBot:
    def __init__(self):
        self.state = State.IDLE
        self.sound = TerminalSound()

        self.current_time = datetime.now().time()
        self.alarms = []
        self.challenges = []
        self.menu_items = ["Set Alarm", "Edit Alarm", "View Alarms", "Quit"]

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def get_input(self, prompt="Input (w/s/e/b): "):
        return input(prompt).strip().lower()

    def change_state(self, selection=None, sub_menu=None):
        if selection is not None:
            if selection >= len(self.menu_items):
                print("Invalid selection.")
            else:
                if selection == 0:
                    self.state = State.SETTING
                elif selection == 1:
                    self.state = State.EDITING
                elif selection == 2:
                    self.state = State.VIEW
                elif selection == 3:
                    raise SystemExit
        elif sub_menu is not None:
            self.state = State.IDLE
        else:
            self.state = State.CHALLENGE

    def main_menu(self):
        selector = 0

        while self.state == State.IDLE:
            self.clear_screen()
            print("=== RoboAlarm ===\n")

            i = 0
            while i < len(self.menu_items):
                text = self.menu_items[i]

                if i == selector:
                    print(f">> {text}")
                else:
                    print(f"   {text}")

                i += 1

            print("\nControls: w=up, s=down, e=enter")
            choice = self.get_input()

            if choice == "w":
                selector -= 1
                if selector < 0:
                    selector = len(self.menu_items) - 1

            elif choice == "s":
                selector += 1
                if selector >= len(self.menu_items):
                    selector = 0

            elif choice == "e":
                self.change_state(selection=selector)

            time.sleep(0.05)

    def set_alarm(self):
        while self.state == State.SETTING:
            self.clear_screen()
            print("=== Set Alarm ===\n")

            print("Create a new alarm.")
            print("Type 'b' at any prompt to go back.\n")

            alarm_time = input("Enter time (HH:MM): ").strip()
            if alarm_time.lower() == "b":
                self.state = State.IDLE
                break

            print("\nAvailable sirens:")
            siren_names = list(SIRENS.keys())

            i = 0
            while i < len(siren_names):
                print(f"{i + 1}. {siren_names[i]}")
                i += 1

            siren_choice = input("\nChoose siren number: ").strip()
            if siren_choice.lower() == "b":
                self.state = State.IDLE
                break

            challenge_amount = input("Enter number of challenges: ").strip()
            if challenge_amount.lower() == "b":
                self.state = State.IDLE
                break

            try:
                datetime.strptime(alarm_time, "%H:%M")
                siren_index = int(siren_choice) - 1
                challenge_amount = int(challenge_amount)

                if siren_index < 0 or siren_index >= len(siren_names):
                    raise ValueError

                siren = siren_names[siren_index]
                new_alarm = Alarm(alarm_time, siren, challenge_amount)
                self.alarms.append(new_alarm)

                print("\nAlarm added successfully.")
            except ValueError:
                print("\nInvalid input. Alarm was not created.")

            input("\nPress Enter to continue...")
            self.state = State.IDLE

    def edit_alarm(self):
        while self.state == State.EDITING:
            self.clear_screen()
            print("=== Edit Alarm ===\n")

            if len(self.alarms) == 0:
                print("No alarms to edit.")
                input("\nPress Enter to go back...")
                self.state = State.IDLE
                break

            i = 0
            while i < len(self.alarms):
                print(f"{i + 1}. {self.alarms[i].alarm_description()}")
                i += 1

            print("\nOptions:")
            print("Enter alarm number to delete it")
            print("Type 'b' to go back")

            choice = input("\nChoice: ").strip().lower()

            if choice == "b":
                self.state = State.IDLE
                break

            try:
                index = int(choice) - 1
                if index < 0 or index >= len(self.alarms):
                    raise ValueError

                removed_alarm = self.alarms.pop(index)
                print(f"\nRemoved: {removed_alarm.alarm_description()}")
            except ValueError:
                print("\nInvalid choice.")

            input("\nPress Enter to continue...")
            self.state = State.IDLE

    def view_alarms(self):
        while self.state == State.VIEW:
            self.clear_screen()
            print("=== Alarms ===\n")

            if len(self.alarms) == 0:
                print("No alarms set")
            else:
                i = 0
                while i < len(self.alarms):
                    alarm = self.alarms[i]
                    text = alarm.alarm_description()
                    print(f"{i + 1}. {text}")
                    i += 1

            print("\nPress b to go back")
            choice = self.get_input("Input: ")

            if choice == "b":
                self.state = State.IDLE

            time.sleep(0.05)


alarm_bot = AlarmBot()

alarm_bot.sound.beep()
time.sleep(0.5)
alarm_bot.sound.beep()

while True:
    if alarm_bot.state == State.IDLE:
        alarm_bot.main_menu()

    elif alarm_bot.state == State.SETTING:
        alarm_bot.set_alarm()

    elif alarm_bot.state == State.EDITING:
        alarm_bot.edit_alarm()

    elif alarm_bot.state == State.VIEW:
        alarm_bot.view_alarms()

    elif alarm_bot.state == State.CHALLENGE:
        print("Challenge mode not implemented yet.")
        alarm_bot.state = State.IDLE

    else:
        print("How are you seeing this?")

    time.sleep(0.2)