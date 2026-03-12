# RoboAlarm
## Table of Contents
- [Preplanning](#preplanning)
  - [Overview](#overview)
  - [Setting the Alarm](#setting-the-alarm)
    - [Editing the Alarm](#editing-alarm)
- [Development](#development)
- [Final Design and Capabilities](#final-design-and-capabilities)
- [Reflection](#reflection)

## Preplanning
### Overview
Many people rely on alarms to wake up in the morning, but normal alarms are often easy to ignore. It is common for people to turn the alarm off or hit snooze and go back to sleep, which can cause them to miss classes, work, or other important events.

To help solve this problem I designed RoboAlarm, a robotic alarm system that actively helps the user wake up. The device allows the user to set alarms, choose from a range of alarm sounds, and select how much help they need waking up. Instead of simply turning the alarm off, the user must complete a number of small challenges before the alarm will stop. These challenges require physical or mental interaction with the robot, making it much harder for the user to fall back asleep.

### Setting the Alarm
When setting the alarm the system will first determine the current time. This may be retrieved automatically if the CPU has access to a real time clock. If this is not available the time will need to be entered manually.

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
When creating the alarm the user chooses how much help they need waking up.

| Setting | # of Challenges |
| ------- | --------------- |
| Some | 3 |
| More | 4 |
| Most | 5 |

#### 0 - LED Memory Game
A sequence of LEDs will flash in a certain order before turning off. The user must reproduce the same sequence in order to continue.

#### 1 - Motor Control Test
The display will show a target speed range along with the current speed. The user must spin the motor and keep it within the acceptable speed range for several seconds.

#### 2 - Colour Recognition
The display will ask the user to present a specific colour. The user must show an object with that colour to the colour sensor and then press the push sensor on the back of the device to confirm.

If the user cannot find the required colour they must first wait ten seconds before pressing a button to generate a new colour.

#### 3 - Distance Challenge
The display will show a target distance along with the current distance being measured. The user must move the device until the measured distance is within the acceptable range, then press the push sensor to confirm.

#### 4. Gyro Coordination Test
The display will show the current angle of the device and a target angle. The user must rotate the device until the angle matches the target range.

Once the correct angle is reached the user must answer two or three questions while keeping the device within that angle range.

### Robot Design
After planning the features of the RoboAlarm I constructed a prototype robot that could support the required sensors and interactions. This design represents the initial layout of the device.

The design may change during development as new issues or improvements are discovered. Any changes made later will be recorded in the development section of the project.

#### Front View

![Image of the front view](images/preFront.jpg)

#### Back View

![Image of back view,](images/preBack.jpg)

#### Side View

![Image of side view](images/preSide.jpg)

![Image of other side view](images/preSide2.jpg)

#### Eugonomics and Usability
Part of the design focused on making the device easy to interact with.

The ultrasonic and colour sensors are mounted on the front of the device so the user can easily point them at a wall or coloured object when completing challenges.

Behind these sensors is the gyro sensor, which is positioned to detect rotational movement when the device is turned.

The touch sensor is mounted at the back of the device facing the user. It is fitted with a button style design similar to those found on controllers so it is easy to press when confirming actions.

Finally the motor is mounted near the base of the device where it can easily be spun during the motor challenge.

### Development Plan

#### System Flow and Development

![[mermaid-diagram-2026-03-11-150143.png]]
#### User Flowchart

```mermaid
stateDiagram-v2

[*] --> CountDown

CountDown --> AlarmTimes

AlarmTimes --> CountDown

  

CountDown --> ConfigAlarm

ConfigAlarm --> CountDown

  

CountDown --> EditAlarm

EditAlarm --> CountDown

AlarmTimes --> EditAlarm

EditAlarm --> AlarmTimes

  

CountDown --> AlarmRings

ConfigAlarm --> AlarmRings

AlarmTimes --> AlarmRings

EditAlarm --> AlarmRings

  

AlarmRings

  

AlarmRings --> Challenges

  

Challenges --> Challenge1

  

Challenge1 --> Challenge2

  

Challenge2 --> ChallengeX

  

ChallengeX --> AlarmOff

  

AlarmOff --> CountDown
```

#### Pseudocode Code

```pseudocode

Import all libraries

Initialise robot outputs
Initialise sensors

Enum State
	idle
	setting
	editing
	challenges
	
Enum Challenges
	led_memory_game
	motor_control_test
	colour_recognition
	distance_challange
	gyro_coordination

Class Alarm
	Init
		siren
		target_time
		challenge_amount
		
	Ring
		play alarm sound
		start vibration
		
Class Challenge
	Init
		type = Challenges.random
	
	Run
		if type = led_memory_game
			run LED memory sequence
			get user button input
			check sequence
			
		if type = motor_control_test
			generate target speed range
			read motor speed
			check speed for a few sseconds
			
		if type = colour_recognition
			generate random colour
			wait for press 
			read colour sensor
			
		if distance_challenge
			generate target distance
			read distance
			press confirm when in range
			
		if type = gyro_coordination
			generate target angle
			read gyro sensor
			ask questions while hold at angle
	
Class AlarmRobot
	Init
		state = idle
		alarms = empty list
		current_time = system time
		
		initialise sensors
		initialise motors
		inisialise outputs
		
	set_alarm
		create new Alarm
		
		ask user for alarm sound
		store sound
		
		ask user for challenge level
			some = 3
			more = 4
			most = 5
		
		ask user for target time or duration until alarm 
		
		add alarm to alarm list
		
	edit_alarm
		display list of alarms
		user selects alarm
		
		allow editing of 
			time
			sound 
			challenge amount
			
	check_alarms
		for each alarm in alarms
			if current_time >= alarm.target_time
				return alarm
				
		return none
			
	run_challenges
		completed = 0
		required = alarm.challenge_amount
		
		while completed < required
			challenge = new challenge
			challenge.Run()
			
			if success
				completed += 1
				
		stop alarm sound
		retunr to idle

alarm = AlarmRobot

Loop

	update current time could be thread
	
	if alarm.state = idle
		check larms
		if alarm triggered
			alarm.Ring() as thread
			alarm.state = challenges
			
	if alarm.state = setting
		alarm.Set_alarm()
		alarm.state = idle
		
	if alarm.state = editing 
		alarm.Edit_alarm()
		alarm.state = idle
		
	if alarm.state = challenges
		alarm.run_challenges()
		
	wait short time 

```

#### If I Get More Time

This and that

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

## Final Design and Capabilities

### Features

### System Architechture

### Final Testing

### Final Robot Design

### Video of Full Use and Capabilities

### Video of Use from a non-Developer

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
