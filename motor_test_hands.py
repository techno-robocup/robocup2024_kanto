#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from techno_client.techno_client.techno_client import TechnoClient
from techno_client.techno_client.techno_data import RescueData
import urequests
import socket
import time
import copy

# while True:
#     pass

EV3 = EV3Brick()
MOTORL = Motor(Port.C)
MOTORR = Motor(Port.D)
MOTORARMBASE = Motor(Port.B)
MOTORARMHANDS = Motor(Port.A)
TOUCHL = TouchSensor(Port.S4)
TOUCHR = TouchSensor(Port.S3)
BACKCOLOR = ColorSensor(Port.S1)
while True:
  MOTORARMHANDS.run(-300)