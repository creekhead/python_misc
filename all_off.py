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

def tv_on():
	run_ssh_command("irsend SEND_ONCE LGTV OFF")

def bed_on():
	run_ssh_command("irsend SEND_ONCE BED BACK_ON")
	time.sleep(1)
	run_ssh_command("irsend SEND_ONCE BED LEGS_ON")
	time.sleep(1)
	run_ssh_command("irsend SEND_ONCE BED BOTH_UP")
	time.sleep(1)
	run_ssh_command("irsend SEND_ONCE BED BOTH_UP")
	time.sleep(1)
	run_ssh_command("irsend SEND_ONCE BED BOTH_UP")
	time.sleep(1)
	run_ssh_command("irsend SEND_ONCE BED BOTH_UP")


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
	print("SSH: "+ssh_command)
	p = paramiko.SSHClient()
	p.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # This script doesn't work for me unless this line is added!
	p.connect("10.1.10.51", port=22, username="pi", password="summer")
	stdin, stdout, stderr = p.exec_command(ssh_command)
	opt = stdout.readlines()
	opt = "".join(opt)
	print(opt)


def main():
	bed_off()
	time.sleep(1)
	tv_voldown()
	time.sleep(1)
	tv_on

main()

