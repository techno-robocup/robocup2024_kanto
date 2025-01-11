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

from techno_client.techno_client.techno_client import TechnoClient
EV3 = EV3Brick()
MOTORL = Motor(Port.C)
MOTORR = Motor(Port.D)
MOTORARMBASE = Motor(Port.B)
MOTORARMHANDS = Motor(Port.A)
TOUCHL = TouchSensor(Port.S4)
TOUCHR = TouchSensor(Port.S3)
BACKCOLOR = ColorSensor(Port.S1)
EV3.light.off()
client = TechnoClient(host="roboberry.local", port=8085)
CLIENT_LEFT_TOP_X = 408
CLIENT_LEFT_TOP_Y = 0
CLIENT_RIGHT_BOTTOM_X = 4208
CLIENT_RIGHT_BOTTOM_Y = 2592
HORIZONTAL_BOX = 3
VERTICAL_BOX = 3
HORIZONTAL_GAP = 500
VERTICAL_GAP = 100


class LINE:

    def __init__(self):
        client.line_info(CLIENT_LEFT_TOP_X, CLIENT_LEFT_TOP_Y,
                         CLIENT_RIGHT_BOTTOM_X, CLIENT_RIGHT_BOTTOM_Y,
                         HORIZONTAL_BOX, VERTICAL_BOX, HORIZONTAL_GAP,
                         VERTICAL_GAP)

    def getdata(self):
        return client.line(debug=True)


class RESCUE_OBJ_DETECTION:

    def getdata(self):
        return client.rescue(debug=True)


LINE_TRACE_SENSOR = LINE()
RESCUE_OBJECT_DETECTION_SENSOR = RESCUE_OBJ_DETECTION()

while True:
    now = RESCUE_OBJECT_DETECTION_SENSOR.getdata()
    print(now)
