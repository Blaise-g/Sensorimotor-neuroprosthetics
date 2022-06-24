#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

# for 1st Motor on ENA
ENA1 = 37
IN1 = 35
IN2 = 33


# set pin numbers to the board's
GPIO.setmode(GPIO.BOARD)

# initialize EnA1, In1 and In2
GPIO.setup(ENA1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)

print(GPIO.input(33))
print(GPIO.input(35))
print(GPIO.input(37))

print('\nStart 1')
GPIO.output(ENA1, GPIO.HIGH)
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)
time.sleep(1)
print(GPIO.input(33))
print(GPIO.input(35))
print(GPIO.input(37))

print('\nForward 1')
GPIO.output(IN1, GPIO.HIGH)
GPIO.output(IN2, GPIO.LOW)
time.sleep(1)
print(GPIO.input(33))
print(GPIO.input(35))
print(GPIO.input(37))

print('\nStop')
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)
time.sleep(1)
print(GPIO.input(33))
print(GPIO.input(35))
print(GPIO.input(37))

print('\nBackward 1')
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.HIGH)
time.sleep(1)
print(GPIO.input(33))
print(GPIO.input(35))
print(GPIO.input(37))

print('\nStop')
GPIO.output(ENA1, GPIO.LOW)
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)
time.sleep(1)
print(GPIO.input(33))
print(GPIO.input(35))
print(GPIO.input(37))

GPIO.cleanup()
# set pin numbers to the board's
GPIO.setmode(GPIO.BOARD)

# motor 2
ENA2 = 19
IN3 = 23
IN4 = 21


# initialize EnA2, In3 and In4
GPIO.setup(ENA2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

print(GPIO.input(19))
print(GPIO.input(23))
print(GPIO.input(21))

print('\nStart 2')
GPIO.output(ENA2, GPIO.HIGH)
GPIO.output(IN3, GPIO.LOW)
GPIO.output(IN4, GPIO.LOW)
time.sleep(1)
print(GPIO.input(19))
print(GPIO.input(23))
print(GPIO.input(21))

print('\nForward 2')
GPIO.output(IN3, GPIO.HIGH)
GPIO.output(IN4, GPIO.LOW)
time.sleep(1)
print(GPIO.input(19))
print(GPIO.input(23))
print(GPIO.input(21))

print('\nStop')
GPIO.output(IN3, GPIO.LOW)
GPIO.output(IN4, GPIO.LOW)
time.sleep(1)
print(GPIO.input(19))
print(GPIO.input(23))
print(GPIO.input(21))

print('\nBackward 2')
GPIO.output(IN3, GPIO.LOW)
GPIO.output(IN4, GPIO.HIGH)
time.sleep(1)
print(GPIO.input(19))
print(GPIO.input(23))
print(GPIO.input(21))

print('\nStop')
GPIO.output(ENA2, GPIO.LOW)
GPIO.output(IN3, GPIO.LOW)
GPIO.output(IN4, GPIO.LOW)
time.sleep(1)
print(GPIO.input(19))
print(GPIO.input(23))
print(GPIO.input(21))

GPIO.cleanup()
