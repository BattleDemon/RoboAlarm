#!/usr/bin/env python3

from enum import Enum
from datetime import datetime
from threading import Thread
import time
import os
import random


# === STATES ===
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


# === SOUND ===
class TerminalSound:
    def beep(self):
        print("[BEEP]")


# === ALARM ===
class Alarm:
    def __init__(self, owner, target_time, siren, challenge_amount):
        self.owner = owner
        self.target_time = target_time
        self.siren = siren
        self.challenge_amount = challenge_amount

        self.hour, self.minute = map(int, target_time.split(":"))

        self.thread = Thread(target=self.countdown, daemon=True)
        self.thread.start()

    def countdown(self):
        while True:
            if self.hour == 0 and self.minute == 0:
                self.trigger()
                break

            time.sleep(1)  # faster for testing (change to 60 later)

            self.minute -= 1
            if self.minute < 0:
                self.minute = 59
                self.hour -= 1
                if self.hour < 0:
                    self.hour = 0

    def trigger(self):
        self.owner.active_alarm = self
        self.owner.state = State.CHALLENGE

    def alarm_description(self):
        return f"{self.hour:02}:{self.minute:02} | {self.siren} | {self.challenge_amount} Challenges"


# === CHALLENGE ===
class Challenge:
    def __init__(self, challenge_type):
        self.type = challenge_type

    def run(self):
        print(f"\nRunning {self.type.name}...")
        input("Press Enter to complete challenge...")


# === MAIN BOT ===
class AlarmBot:
    def __init__(self):
        self.state = State.IDLE
        self.sound = TerminalSound()

        self.alarms = []
        self.active_alarm = None
        self.menu_items = ["Set Alarm", "Edit Alarm", "View Alarms", "Quit"]

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def get_input(self):
        return input("Input (w/s/e/b): ").strip().lower()

    def change_state(self, selection=None):
        if selection == 0:
            self.state = State.SETTING
        elif selection == 1:
            self.state = State.EDITING
        elif selection == 2:
            self.state = State.VIEW
        elif selection == 3:
            raise SystemExit

    # === MENU ===
    def main_menu(self):
        selector = 0

        while self.state == State.IDLE:
            self.clear()
            print("=== RoboAlarm ===\n")

            for i in range(len(self.menu_items)):
                prefix = ">>" if i == selector else "  "
                print(f"{prefix} {self.menu_items[i]}")

            choice = self.get_input()

            if choice == "w":
                selector = (selector - 1) % len(self.menu_items)
            elif choice == "s":
                selector = (selector + 1) % len(self.menu_items)
            elif choice == "e":
                self.change_state(selector)

    # === SET / EDIT ===
    def alarm_editor(self, existing=None):
        sirens = list(SIRENS.keys())

        if existing:
            hour, minute = existing.hour, existing.minute
            siren_index = sirens.index(existing.siren)
            challenges = existing.challenge_amount
        else:
            hour, minute = 7, 0
            siren_index = 0
            challenges = 1

        while True:
            self.clear()
            print("=== Alarm Editor ===\n")
            print(f"1. Hour: {hour}")
            print(f"2. Minute: {minute}")
            print(f"3. Siren: {sirens[siren_index]}")
            print(f"4. Challenges: {challenges}")
            print("5. Save")
            print("b. Back")

            choice = input("\nChoice: ").lower()

            if choice == "1":
                hour = (hour + 1) % 24
            elif choice == "2":
                minute = (minute + 1) % 60
            elif choice == "3":
                siren_index = (siren_index + 1) % len(sirens)
            elif choice == "4":
                challenges = max(1, challenges + 1)
            elif choice == "5":
                if existing:
                    self.alarms.remove(existing)

                new_alarm = Alarm(
                    self,
                    f"{hour:02}:{minute:02}",
                    sirens[siren_index],
                    challenges
                )
                self.alarms.append(new_alarm)

                print("\nSaved!")
                input("Enter to continue...")
                self.state = State.IDLE
                return

            elif choice == "b":
                self.state = State.IDLE
                return

    # === EDIT MENU ===
    def edit_alarm(self):
        if not self.alarms:
            print("No alarms.")
            input("Enter...")
            self.state = State.IDLE
            return

        while True:
            self.clear()
            print("=== Edit Alarm ===\n")

            for i, alarm in enumerate(self.alarms):
                print(f"{i+1}. {alarm.alarm_description()}")

            print("b. Back")

            choice = input("\nSelect: ").lower()

            if choice == "b":
                self.state = State.IDLE
                return

            try:
                idx = int(choice) - 1
                self.alarm_editor(self.alarms[idx])
                return
            except:
                pass

    # === VIEW ===
    def view_alarms(self):
        self.clear()
        print("=== Alarms ===\n")

        if not self.alarms:
            print("No alarms set")
        else:
            for a in self.alarms:
                print(a.alarm_description())

        input("\nPress Enter...")
        self.state = State.IDLE

    # === CHALLENGE SYSTEM ===
    def start_challenges(self):
        alarm = self.active_alarm

        print(f"\nALARM TRIGGERED: {alarm.alarm_description()}")

        challenges = [
            Challenge(random.choice(list(Challenge_types)))
            for _ in range(alarm.challenge_amount)
        ]

        for c in challenges:
            c.run()

        print("\nAlarm dismissed.")
        self.active_alarm = None
        self.state = State.IDLE


# === RUN ===
bot = AlarmBot()

bot.sound.beep()
time.sleep(0.5)
bot.sound.beep()

while True:
    if bot.state == State.IDLE:
        bot.main_menu()
    elif bot.state == State.SETTING:
        bot.alarm_editor()
    elif bot.state == State.EDITING:
        bot.edit_alarm()
    elif bot.state == State.VIEW:
        bot.view_alarms()
    elif bot.state == State.CHALLENGE:
        bot.start_challenges()

    time.sleep(0.1)