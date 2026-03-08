# RoboAlarm

## Table of Contents

## Preplanning

### Overview

Many people rely on alarms to wake up in the morning, but normal alarms are often easy to ignore. It is common for people to turn the alarm off or hit snooze and go back to sleep, which can cause them to miss classes, work, or other important events.

To help solve this problem I designed RoboAlarm, a robotic alarm system that actively helps the user wake up. The device allows the user to set alarms, choose from a range of alarm sounds, and select how much help they need waking up. Instead of simply turning the alarm off, the user must complete a number of small challenges before the alarm will stop. These challenges require physical or mental interaction with the robot, making it much harder for the user to fall back asleep.

### Setting the Alarm

When setting the alarm the system will first determine the current time. This may be retrieved automatically if the CPU has access to a real time clock (RTC). If this is not available the time will need to be entered manually.

After the current time is known the user will select when the alarm should go off. This can either be a specific time or a duration until the alarm activates. Once the time has been chosen the user will then select an alarm sound and how much help they need to wake up.

#### Editing Alarm

Existing alarms can also be edited. The user will be able to change the time the alarm goes off, the alarm sound, and how many challenges are required to turn the alarm off.

#### Setting Multiple Alarms

The system will support multiple alarms. Each alarm can be set to activate at a different time.

If a new alarm goes off while another alarm is still active, the system will add extra challenges to the current alarm rather than starting a completely new one. This prevents the user from avoiding alarms by delaying challenges.

#### Multiple Views

The device will have multiple views to make it easier to manage alarms.

The main view will show a large countdown timer for the closest upcoming alarm. It will also display a list of other alarms below it. Selecting an alarm will allow the user to edit its settings.

The second view will display the current time and a list of all alarms with their scheduled times.

The third view will be the alarm creation screen where the user can create and configure new alarms.

### Challenges

The challenge system is designed to stop the user from simply turning the alarm off and going back to sleep. The alarm will only stop once the required number of challenges have been completed.

When the alarm activates, a challenge will be randomly selected from a set of available tasks. After the user completes one challenge another will be selected until the required number has been completed.

#### Setting Challenges

While setting the alarm the user will be prompted on how much help they need waking up, they can choose between "Some" which will give the user three challenges, "More" the user will need to complete four challenges, "Most" the user will need to complete all five challenges.

#### 0 - LEDS

LEDs will flash in an order than turn off, you will have to reproduce this order to continue.

#### 1 - Motor

Display will show a range of target speeds as well as the current speed, you will have to spin the motor and have it stay within the acceptable range for a few seconds.

#### 2 - Color Sensor

Display will ask you to show a color, You will need to show that color to the color sensor then press the push sensor on the back to confirm. If you can't find that color you must first wait 10 seconds then click a button on the device it will select a new color.

#### 3 - Ultrasonic Sensor

Display will show a distance target and your current distance, get within a range of that distance then press the push sensor to confirm.

#### 4. Gyro Sensor

Display will show current angle and a target angle, you must rotate your device to match that angel (again with a range), then must answer two or three questions while keeping the device within that range.

### Robot Design

After coming up with the general plan for the Alarm, I constructed the below robot alarm. This may change entirely or slightly since I have built it at the end of the preplanning phase so other problems or ideas might require me to change its design in some way, if i do this it will be noted in that development stage.

#### Eugonomics and Usability

Part of the design focused on ergonomics and usability for the device, with the ultrasonic and color sensor in the front to allow you to properly point them at either the wall or a specific color. Up front is also a Gyro mounted behind the color and ultrasonic sensors, which has it monitor left and right rotational movement, next to this is the tough sensor pointing back (towards the user) equiped with a button like design similar to some controlers. Lastly mounted at the base near is the motor.

### Development Plan

#### Flowchart

#### If I Get More Time

### Technical Constraints

## Development

### Prototype 0: Setting and Editing the Alarm

#### Discussion

#### Code Snippets

#### Video of Functionality

#### Video of Non-Developer Use

#### Issues and Solutions

### Prototype 1: Multiple views and Multiple Alarms

#### Discussion

#### Code Snippets

#### Video of Functionality

#### Video of Non-Developer Use

#### Issues and Solutions

### Prototype 2: Randomising based on Challenge Level, LED Challenge

#### Discussion

#### Code Snippets

#### Video of Functionality

#### Video of Non-Developer Use

#### Issues and Solutions

### Prototype 3: Motor and Ultrasonic Sensor Challenges

#### Discussion

#### Code Snippets

#### Video of Functionality

#### Video of Non-Developer Use

#### Issues and Solutions

### Prototype 4: Color and Gyro Sensor Challenges

#### Discussion

#### Code Snippets

#### Video of Functionality

#### Video of Non-Developer Use

#### Issues and Solutions

## Final Overview 

### Features

### System Architechture

### Final Testing

### Video of Full Functunality

### Video of Full Funcctionality from a non-Developer

## Reflection

### What do you think of the overall design?

### What changes would you make?

### What issues did you experience?

### What techniques did you use to solve these issues?

### What changes would you make if repeating this project?

### What have you learnt from the project?

## Sources

### Code References

### Hardware Documentation

### Tutorials or Guides Used
