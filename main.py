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
DEFAULTTURNSPEED = 60
DEFAULTCNTTHRESHOLD = 10
DEFAULTTIMEWAIT = 0.5
DEFAULTPROPORTION = 0.3
DEFAULTI = 0.5
DEFAULTD = 0.05
ACCUMI = 0
ACCUMD = 0
BOTTOM_LEFT = 0
BOTTOM_MIDDLE = 0
BOTTOM_RIGHT = 0
MIDDLE_LEFT = 0
MIDDLE_MIDDLE = 0
MIDDLE_RIGHT = 0
TOP_LEFT = 0
TOP_MIDDLE = 0
TOP_RIGHT = 0
BOTTOM_LEFT_OBJ = []
BOTTOM_RIGHT_OBJ = []
BOTTOM_MIDDLE_OBJ = []
MIDDLE_LEFT_OBJ = []
MIDDLE_MIDDLE_OBJ = []
MIDDLE_RIGHT_OBJ = []
TOP_LEFT_OBJ = []
TOP_MIDDLE_OBJ = []
TOP_RIGHT_OBJ = []
WHITETHRESHOLD = 100
BLACKTHRESHOLD = 60
SATURATIONTHRESHOLD = 100
BEFLNUM = 0
BEFRNUM = 0
cnt = 0

MOTORARMBASE.run(-100)


class LINE:

    def __init__(self, vertical, horizontal):
        self.target_url = "http://roboberry.local:81/techno_cam/line_colors?latlx=408&latly=0&labrx=4208&labry=2592&bc_h=3&bc_v=3&bg_h=1200&bg_v=500&debug=true"

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
    global BOTTOM_LEFT, BOTTOM_MIDDLE, BOTTOM_RIGHT, MIDDLE_LEFT, MIDDLE_MIDDLE, MIDDLE_RIGHT, TOP_LEFT, TOP_MIDDLE, TOP_RIGHT, ACCUMI, ACCUMD, BOTTOM_LEFT_OBJ, BOTTOM_RIGHT_OBJ, BOTTOM_MIDDLE_OBJ, MIDDLE_LEFT_OBJ, MIDDLE_MIDDLE_OBJ, MIDDLE_RIGHT_OBJ, TOP_LEFT_OBJ, TOP_MIDDLE_OBJ, TOP_RIGHT_OBJ, BEFLNUM, BEFRNUM
    now = LINE_TRACE_SENSOR.getdata()
    BOTTOM_LEFT = now[2][2]
    BOTTOM_MIDDLE = now[5][2]
    BOTTOM_RIGHT = now[8][2]
    MIDDLE_LEFT = now[1][2]
    MIDDLE_MIDDLE = now[4][2]
    MIDDLE_RIGHT = now[7][2]
    TOP_LEFT = now[0][2]
    TOP_MIDDLE = now[3][2]
    TOP_RIGHT = now[6][2]
    BOTTOM_LEFT_OBJ = now[2]
    BOTTOM_MIDDLE_OBJ = now[5]
    BOTTOM_RIGHT_OBJ = now[8]
    MIDDLE_LEFT_OBJ = now[1]
    MIDDLE_MIDDLE_OBJ = now[4]
    MIDDLE_RIGHT_OBJ = now[7]
    TOP_LEFT_OBJ = now[0]
    TOP_MIDDLE_OBJ = now[3]
    TOP_RIGHT_OBJ = now[6]
    ACCUMI = BOTTOM_LEFT - BOTTOM_RIGHT
    ACCUMD = (BEFLNUM - BEFRNUM) - (BOTTOM_LEFT - BOTTOM_RIGHT)

def isblack(h,s,v):
    return v<BLACKTHRESHOLD and s < SATURATIONTHRESHOLD

def iswhite(h,s,v):
    return v>WHITETHRESHOLD and s < SATURATIONTHRESHOLD

def isgreen(h,s,v):
    return BLACKTHRESHOLD < v < WHITETHRESHOLD and 50 < s < 90 # TODO need changes

def isred(h,s,v):
    return BLACKTHRESHOLD < v < WHITETHRESHOLD and (s < 10 or s > 170) # TODO need changes

# while True:
    # print(LINE_TRACE_SENSOR.getdata())

while True:
    cnt += 1
    if Button.CENTER in EV3.buttons.pressed():
        MOTORL.brake()
        MOTORR.brake()
        ACCUMI = 0
        ACCUMD = 0
        EV3.speaker.beep()
        time.sleep(0.5)
        while True:
            if Button.CENTER in EV3.buttons.pressed():
                EV3.speaker.beep()
                time.sleep(0.5)
                break
    updatedata()
    MOTORL.run(DEFAULTSPEED + DEFAULTPROPORTION *
               (BOTTOM_LEFT - BOTTOM_RIGHT) + DEFAULTI * ACCUMI +
               DEFAULTD * ACCUMD)
    MOTORR.run(DEFAULTSPEED + DEFAULTPROPORTION *
               (BOTTOM_RIGHT - BOTTOM_LEFT) - DEFAULTI * ACCUMI -
               DEFAULTD * ACCUMD)
    if isblack(BOTTOM_LEFT_OBJ[0], BOTTOM_LEFT_OBJ[1], BOTTOM_LEFT_OBJ[2]) and not isblack(BOTTOM_RIGHT_OBJ[0], BOTTOM_RIGHT_OBJ[1], BOTTOM_RIGHT_OBJ[2]) and cnt > 10:
        MOTORL.brake()
        MOTORR.brake()
        EV3.speaker.beep()
        time.sleep(0.5)
        print(MIDDLE_MIDDLE_OBJ)
        if isblack(MIDDLE_MIDDLE_OBJ[0], MIDDLE_MIDDLE_OBJ[1], MIDDLE_MIDDLE_OBJ[2]):
            EV3.speaker.beep()
            while isblack(BOTTOM_LEFT_OBJ[0], BOTTOM_LEFT_OBJ[1], BOTTOM_LEFT_OBJ[2]):
                updatedata()
                MOTORL.run(DEFAULTSPEED)
                MOTORR.run(DEFAULTSPEED)
            cnt = 0
        else:
            while isblack(BOTTOM_LEFT_OBJ[0], BOTTOM_LEFT_OBJ[1], BOTTOM_LEFT_OBJ[2]):
                updatedata()
                MOTORL.run(DEFAULTSPEED)
                MOTORR.run(DEFAULTSPEED)
                print(BOTTOM_LEFT_OBJ[0], BOTTOM_LEFT_OBJ[1], BOTTOM_LEFT_OBJ[2])
            MOTORL.run(DEFAULTSPEED)
            MOTORR.run(DEFAULTSPEED)
            time.sleep(DEFAULTTIMEWAIT)
            while not isblack(BOTTOM_MIDDLE_OBJ[0], BOTTOM_MIDDLE_OBJ[1], BOTTOM_MIDDLE_OBJ[2]):
                updatedata()
                MOTORL.run(-DEFAULTSPEED)
                MOTORR.run(DEFAULTSPEED)
                print(BOTTOM_MIDDLE_OBJ[0], BOTTOM_MIDDLE_OBJ[1], BOTTOM_MIDDLE_OBJ[2])
    # print(*BOTTOM_LEFT_OBJ)
    # print(*BOTTOM_MIDDLE_OBJ)
    # print(*BOTTOM_RIGHT_OBJ)
    # print(*MIDDLE_LEFT_OBJ)
    # print(*MIDDLE_MIDDLE_OBJ)
    # print(*MIDDLE_RIGHT_OBJ)
    # print(*TOP_LEFT_OBJ)
    # print(*TOP_MIDDLE_OBJ)
    # print(*TOP_RIGHT_OBJ)
    print()
    # print("P: ", (BOTTOM_LEFT - BOTTOM_RIGHT) * DEFAULTPROPORTION)
    # print("I: ", DEFAULTI * ACCUMI)
    # print("D: ", DEFAULTD * ACCUMD)
    BEFLNUM = BOTTOM_LEFT
    BEFRNUM = BOTTOM_RIGHT
