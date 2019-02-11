from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, print_json, Separator
from examples import custom_style_2

import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

import datetime
import os
import time
import random
import webbrowser
import paramiko
import msvcrt
import keyboard

aCount = 0

def tv_on():
	run_ssh_command("irsend SEND_ONCE LGTV OFF")

def bed_on():
	run_ssh_command("irsend SEND_ONCE BED BACK_ON")
	time.sleep(1)
	run_ssh_command("irsend SEND_ONCE BED LEGS_ON")
	time.sleep(1)
	run_ssh_command("irsend SEND_START BED BOTH_UP")
	time.sleep(2)
	run_ssh_command("irsend SEND_STOP BED BOTH_UP")

def bed_off():
	#TURN OFF SEND, JUST TO BE SURE
	run_ssh_command("irsend SEND_STOP BED BOTH_DOWN")
	time.sleep(1)
	run_ssh_command("irsend SEND_ONCE BED ALL_OFF")
	time.sleep(1)
	run_ssh_command("irsend SEND_START BED BOTH_DOWN")
	time.sleep(20)
	run_ssh_command("irsend SEND_STOP BED BOTH_DOWN")
	time.sleep(1)
	run_ssh_command("irsend SEND_START BED HEAD_UP")
	time.sleep(4)
	run_ssh_command("irsend SEND_STOP BED HEAD_UP")
	time.sleep(1)
	run_ssh_command("irsend SEND_START BED LEGS_DOWN")
	time.sleep(3)
	run_ssh_command("irsend SEND_STOP BED LEGS_DOWN")


def bed_shake():
	global aCount

	run_ssh_command("irsend SEND_ONCE BED BACK_ON")
	time.sleep(1)
	run_ssh_command("irsend SEND_ONCE BED LEGS_ON")
	time.sleep(1)

	#BRING IT DOWN, but only on the first try
	if(aCount == 2):
		run_ssh_command("irsend SEND_START BED BOTH_DOWN")
		time.sleep(7)
		run_ssh_command("irsend SEND_STOP BED BOTH_DOWN")
		time.sleep(1)

	#BOTH UP
	run_ssh_command("irsend SEND_START BED BOTH_UP")
	time.sleep(7)
	run_ssh_command("irsend SEND_STOP BED BOTH_UP")
	time.sleep(1)

	#BRING IT DOWN, but only on the first try
	if(aCount == 2):
		run_ssh_command("irsend SEND_START BED BOTH_DOWN")
		time.sleep(7)
		run_ssh_command("irsend SEND_STOP BED BOTH_DOWN")
		time.sleep(1)

	#BOTH UP
	run_ssh_command("irsend SEND_START BED BOTH_UP")
	time.sleep(7)
	run_ssh_command("irsend SEND_STOP BED BOTH_UP")
	time.sleep(1)

def tv_volup():
	run_ssh_command("irsend SEND_ONCE LGTV VOL_UP")
	time.sleep(1)
	run_ssh_command("irsend SEND_ONCE LGTV VOL_UP")
	time.sleep(1)
	run_ssh_command("irsend SEND_ONCE LGTV VOL_UP")
	time.sleep(1)
	run_ssh_command("irsend SEND_ONCE LGTV VOL_UP")
	time.sleep(1)
	run_ssh_command("irsend SEND_ONCE LGTV VOL_UP")
	time.sleep(1)

def tv_voldown():
	run_ssh_command("irsend SEND_ONCE LGTV VOL_DOWN")
	time.sleep(1)
	run_ssh_command("irsend SEND_ONCE LGTV VOL_DOWN")
	time.sleep(1)
	run_ssh_command("irsend SEND_ONCE LGTV VOL_DOWN")
	time.sleep(1)
	run_ssh_command("irsend SEND_ONCE LGTV VOL_DOWN")
	time.sleep(1)
	run_ssh_command("irsend SEND_ONCE LGTV VOL_DOWN")
	time.sleep(1)

def run_ssh_command(ssh_command):
	#check if key pressed
	if msvcrt.kbhit():
		key = msvcrt.getch()
		stop_alarm()

	print("SSH: "+ssh_command)
	p = paramiko.SSHClient()
	p.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # This script doesn't work for me unless this line is added!
	p.connect("10.1.10.51", port=22, username="pi", password="summer")
	stdin, stdout, stderr = p.exec_command(ssh_command)
	opt = stdout.readlines()
	opt = "".join(opt)
	print(opt)

def wake_up_loop():
	global aCount
	print("Press a key, or FACE the consequences!!!")
	timeout = 120
	startTime = time.time()
	inp = None
	while True:
		if msvcrt.kbhit():
		    inp = msvcrt.getch()
		    break
		elif time.time() - startTime > timeout:
		    break

	if inp:
		stop_alarm()
	else:
	    print("Wake up!!!")
	    aCount += 1
	    ramp_it_up()
	    wake_up_loop()

def ramp_it_up():
	tv_volup()
	time.sleep(1)
	bed_shake()

def stop_alarm():
	print("Alarm stopped...")
	run_ssh_command("irsend SEND_STOP BED BOTH_DOWN")
	time.sleep(1)
	run_ssh_command("irsend SEND_ONCE BED ALL_OFF")
	tv_voldown()
	time.sleep(1)
	tv_on()
	time.sleep(1)
	bed_off()
	exit()

def main():

	# If video URL file does not exist, create one
	if not os.path.isfile("youtube_alarm_videos.txt"):
		print('Creating "youtube_alarm_videos.txt"...')
		with open("youtube_alarm_videos.txt", "w") as alarm_file:
			alarm_file.write("https://www.youtube.com/watch?v=anM6uIZvx74")

	def check_alarm_input(alarm_time):
		"""Checks to see if the user has entered in a valid alarm time"""
		if len(alarm_time) == 1: # [Hour] Format
			if alarm_time[0] < 24 and alarm_time[0] >= 0:
				return True
		if len(alarm_time) == 2: # [Hour:Minute] Format
			if alarm_time[0] < 24 and alarm_time[0] >= 0 and \
			   alarm_time[1] < 60 and alarm_time[1] >= 0:
				return True
		elif len(alarm_time) == 3: # [Hour:Minute:Second] Format
			if alarm_time[0] < 24 and alarm_time[0] >= 0 and \
			   alarm_time[1] < 60 and alarm_time[1] >= 0 and \
			   alarm_time[2] < 60 and alarm_time[2] >= 0:
				return True
		return False

	# Get user input for the alarm time
	print("Set a time for the alarm (Ex. 06:30 or 18:30:00)")
	questions = [
    {
	        'type': 'rawlist',
	        'name': 'time',
	        'message': 'WAKE UP, What time:',
	        'choices': ['08:15', '09:00', '08:30', '09:30',''],
	        'filter': lambda val: val.lower()
	    }
	]

	answers = prompt(questions, style=custom_style_2)
	#print(answers['time'])

	while True:
		alarm_input = input(">> "+answers['time'])
		try:
			if answers['time']!='':
				alarm_time = [int(n) for n in answers['time'].split(":")]
			else:
				alarm_time = [int(n) for n in alarm_input.split(":")]
			if check_alarm_input(alarm_time):
				break
			else:
				raise ValueError
		except ValueError:
			print("ERROR: Enter time in HH:MM or HH:MM:SS format")


	# Convert the alarm time from [H:M] or [H:M:S] to seconds
	seconds_hms = [3600, 60, 1] # Number of seconds in an Hour, Minute, and Second
	alarm_seconds = sum([a*b for a,b in zip(seconds_hms[:len(alarm_time)], alarm_time)])

	# Get the current time of day in seconds
	now = datetime.datetime.now()
	current_time_seconds = sum([a*b for a,b in zip(seconds_hms, [now.hour, now.minute, now.second])])

	# Calculate the number of seconds until alarm goes off
	time_diff_seconds = alarm_seconds - current_time_seconds

	# If time difference is negative, set alarm for next day
	if time_diff_seconds < 0:
		time_diff_seconds += 86400 # number of seconds in a day

	# Display the amount of time until the alarm goes off
	print("Alarm set to go off in %s" % datetime.timedelta(seconds=time_diff_seconds))

	# Sleep until the alarm goes off
	time.sleep(time_diff_seconds)

	# Time for the alarm to go off
	print("Wake Up!")

	# Load list of possible video URLs
	with open("youtube_alarm_videos.txt", "r") as alarm_file:
		videos = alarm_file.readlines()

	# Open a random video from the list
	webbrowser.open(random.choice(videos))

	time.sleep(1)
	tv_on()
	time.sleep(3)
	tv_volup()
	time.sleep(1)
	bed_on()

	wake_up_loop()

main()

