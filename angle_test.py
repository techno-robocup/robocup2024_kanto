#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from techno_client.techno_client.techno_client import TechnoClient
import urequests
import socket
import time
MOTORARMBASE = Motor(Port.B)
MOTORARMHANDS = Motor(Port.A)

while True:
  print(MOTORARMBASE.run_target(100,int(input())))
