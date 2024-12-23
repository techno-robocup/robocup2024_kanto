#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import urequests
import socket
import time

EV3 = EV3Brick()
MOTORL = Motor(Port.C)
MOTORR = Motor(Port.D)
MOTORARMBASE = Motor(Port.B)
MOTORARMHANDS = Motor(Port.A)
# TOUCHL = TouchSensor(Port.S4)
# TOUCHR = TouchSensor(Port.S3)

DEBUGPRINT = False
DEBUGMOTOR = False
DEBUGCOLORSENSOR = False
DEFAULTSPEED = 50
DEFAULTPROPORTION = 0.1
DEFAULTI = 0.2
DEFAULTD = 0.03
ACCUMI = 0
ACCUMD = 0
BOTTOM_LEFT = 0
BOTTOM_RIGHT = 0
BOTTOM_MIDDLE = 0
WHITETHRESHOLD = 100
BLACKTHRESHOLD = 40
BEFLNUM = 0
BEFRNUM = 0
cnt = 0

# MOTORARMBASE.run(-100)

class LINE:

    def __init__(self, vertical, horizontal):
        self.target_url = "http://roboberry.local:81/techno_cam/line_colors?latlx=408&latly=0&labrx=4208&labry=2592&bc_h=3&bc_v=3&bg_h=1200&bg_v=500"

    def getdata(self):
        try:
            json_data = urequests.get(self.target_url).json()
        except:
            return None
        return json_data["colors"]


class RESCUE_OBJ_DETECTION:

    def __init__(self):
        self.target_url = "http://roboberry.local:81/techno_cam/rescue_objects"

    def getdata(self):
        try:
            json_data = urequests.get(self.target_url).json()
        except:
            return None
        return json_data["objects"]


def isgreenhue(hue: int):
    return 150 <= hue <= 210


LINE_TRACE_SENSOR = LINE(3, 3)
RESCUE_OBJECT_DETECTION_SENSOR = RESCUE_OBJ_DETECTION()

# while True:
#     MOTORARMHANDS.run(-200)

def updatedata():
    global BOTTOM_LEFT, BOTTOM_MIDDLE, BOTTOM_RIGHT, ACCUMI, ACCUMD
    now = LINE_TRACE_SENSOR.getdata()
    BOTTOM_LEFT = now[2][2]
    BOTTOM_MIDDLE = now[5][2]
    BOTTOM_RIGHT = now[8][2]
    ACCUMI = BOTTOM_LEFT - BOTTOM_RIGHT
    ACCUMD = (BEFLNUM - BEFRNUM) - (BOTTOM_LEFT - BOTTOM_RIGHT)

while True:
    cnt += 1
    if Button.CENTER in EV3.buttons.pressed():
        MOTORL.brake()
        MOTORR.brake()
        EV3.speaker.beep()
        time.sleep(0.5)
        while True:
            if Button.CENTER in EV3.buttons.pressed():
                EV3.speaker.beep()
                time.sleep(0.5)
                break
    updatedata()
    MOTORL.run(DEFAULTSPEED+DEFAULTPROPORTION*(BOTTOM_LEFT-BOTTOM_RIGHT)+DEFAULTI*ACCUMI+DEFAULTD*ACCUMD)
    MOTORR.run(DEFAULTSPEED+DEFAULTPROPORTION*(BOTTOM_RIGHT-BOTTOM_LEFT)-DEFAULTI*ACCUMI-DEFAULTD*ACCUMD)
    if BOTTOM_RIGHT < BLACKTHRESHOLD and cnt > 10:
        MOTORL.brake()
        MOTORR.brake()
        EV3.speaker.beep()
        print("!!")
        while not BOTTOM_RIGHT < BLACKTHRESHOLD:
            updatedata()
            MOTORL.run(70)
            MOTORR.run(70)
        MOTORL.run(100)
        MOTORR.run(100)
        time.sleep(0.3)
        updatedata()
        while not BOTTOM_RIGHT < BLACKTHRESHOLD:
            updatedata()
            MOTORL.run(40)
            MOTORR.run(-40)
        while not BOTTOM_MIDDLE < BLACKTHRESHOLD:
            updatedata()
            MOTORL.run(40)
            MOTORR.run(-40)
        MOTORL.brake()
        MOTORR.brake()
        cnt = 0
    print(BOTTOM_LEFT, BOTTOM_MIDDLE, BOTTOM_RIGHT)
    print("P: ",(BOTTOM_LEFT-BOTTOM_RIGHT)*DEFAULTPROPORTION)
    print("I: ",DEFAULTI*ACCUMI)
    print("D: ",DEFAULTD*ACCUMD)
    # print(DEFAULTSPEED+DEFAULTPROPORTION*(BOTTOM_LEFT-BOTTOM_RIGHT)+DEFAULTI*ACCUMI+DEFAULTD*ACCUMD, DEFAULTSPEED+DEFAULTPROPORTION*(BOTTOM_RIGHT-BOTTOM_LEFT)-DEFAULTI*ACCUMI-DEFAULTD*ACCUMD)
    # MOTORL.run(DEFAULTSPEED+DEFAULTPROPORTION*(BOTTOM_LEFT-BOTTOM_RIGHT))
    # MOTORR.run(DEFAULTSPEED+DEFAULTPROPORTION*(BOTTOM_RIGHT-BOTTOM_LEFT))
    BEFLNUM = BOTTOM_LEFT
    BEFRNUM = BOTTOM_RIGHT