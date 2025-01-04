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

# while True:
#     pass

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
DEFAULTSPEED = 60
DEFAULTTURNSPEED = 50
DEFAULTTIMEWAIT = 0
DEFAULTPROPORTION = 0.12
DEFAULTI = 0.04
DEFAULTD = 0
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
WHITETHRESHOLD = 160
BLACKTHRESHOLD = 70
SATURATIONTHRESHOLD = 130
BEFLNUM = 0
BEFRNUM = 0

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


LINE_TRACE_SENSOR = LINE()
RESCUE_OBJECT_DETECTION_SENSOR = RESCUE_OBJ_DETECTION()


def updatedata():
    global BOTTOM_LEFT, BOTTOM_MIDDLE, BOTTOM_RIGHT, MIDDLE_LEFT, MIDDLE_MIDDLE, MIDDLE_RIGHT, TOP_LEFT, TOP_MIDDLE, TOP_RIGHT, ACCUMI, ACCUMD, BOTTOM_LEFT_OBJ, BOTTOM_RIGHT_OBJ, BOTTOM_MIDDLE_OBJ, MIDDLE_LEFT_OBJ, MIDDLE_MIDDLE_OBJ, MIDDLE_RIGHT_OBJ, TOP_LEFT_OBJ, TOP_MIDDLE_OBJ, TOP_RIGHT_OBJ, BEFLNUM, BEFRNUM
    now = LINE_TRACE_SENSOR.getdata().colors
    BOTTOM_LEFT = now[2].v
    BOTTOM_MIDDLE = now[5].v
    BOTTOM_RIGHT = now[8].v
    MIDDLE_LEFT = now[1].v
    MIDDLE_MIDDLE = now[4].v
    MIDDLE_RIGHT = now[7].v
    TOP_LEFT = now[0].v
    TOP_MIDDLE = now[3].v
    TOP_RIGHT = now[6].v
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


def isblack(h, s, v):
    return v < BLACKTHRESHOLD and s < SATURATIONTHRESHOLD


def iswhite(h, s, v):
    return v > WHITETHRESHOLD and s < SATURATIONTHRESHOLD


def isgreen(h, s, v):
    return BLACKTHRESHOLD < v < WHITETHRESHOLD and 50 < s < 90  # TODO need changes


def isred(h, s, v):
    return BLACKTHRESHOLD < v < WHITETHRESHOLD and (s < 10 or s > 170
                                                    )  # TODO need changes


# while True:
# print(LINE_TRACE_SENSOR.getdata())

MOTORARMBASE.run(-100)

# while True:
#     print(LINE_TRACE_SENSOR.getdata().colors[2].v)
while True:
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
    if isblack(BOTTOM_LEFT_OBJ.h,BOTTOM_LEFT_OBJ.s,BOTTOM_LEFT_OBJ.v):
        print("left")
        eliftempcnt = 0
        MOTORL.brake()
        MOTORR.brake()
        EV3.speaker.beep(frequency=440)
        while isblack(BOTTOM_LEFT_OBJ.h,BOTTOM_LEFT_OBJ.s,BOTTOM_LEFT_OBJ.v) and eliftempcnt<50:
            updatedata()
            eliftempcnt+=1
            print(eliftempcnt)
            MOTORL.run(DEFAULTTURNSPEED)
            MOTORR.run(DEFAULTTURNSPEED)
        while not isblack(BOTTOM_RIGHT_OBJ.h,BOTTOM_RIGHT_OBJ.s,BOTTOM_RIGHT_OBJ.v):
            updatedata()
            MOTORL.run(-DEFAULTTURNSPEED)
            MOTORR.run(DEFAULTTURNSPEED)
        while not isblack(BOTTOM_MIDDLE_OBJ.h,BOTTOM_MIDDLE_OBJ.s,BOTTOM_MIDDLE_OBJ.v):
            updatedata()
            MOTORL.run(DEFAULTTURNSPEED)
            MOTORR.run(-DEFAULTTURNSPEED)
    elif isblack(BOTTOM_RIGHT_OBJ.h,BOTTOM_RIGHT_OBJ.s,BOTTOM_RIGHT_OBJ.v):
        print("right")
        eliftempcnt=0
        MOTORL.brake()
        MOTORR.brake()
        EV3.speaker.beep(frequency=460)
        while isblack(BOTTOM_RIGHT_OBJ.h,BOTTOM_RIGHT_OBJ.s,BOTTOM_RIGHT_OBJ.v) and eliftempcnt<50:
            updatedata()
            eliftempcnt+=1
            print(eliftempcnt)
            MOTORL.run(DEFAULTTURNSPEED)
            MOTORR.run(DEFAULTTURNSPEED)
        while not isblack(BOTTOM_LEFT_OBJ.h,BOTTOM_LEFT_OBJ.s,BOTTOM_LEFT_OBJ.v):
            updatedata()
            print(BOTTOM_LEFT_OBJ.h,BOTTOM_LEFT_OBJ.s,BOTTOM_LEFT_OBJ.v)
            MOTORL.run(DEFAULTTURNSPEED)
            MOTORR.run(-DEFAULTTURNSPEED)
        while not isblack(BOTTOM_MIDDLE_OBJ.h,BOTTOM_MIDDLE_OBJ.s,BOTTOM_MIDDLE_OBJ.v):
            updatedata()
            MOTORL.run(-DEFAULTTURNSPEED)
            MOTORR.run(DEFAULTTURNSPEED)
    print(BOTTOM_LEFT_OBJ.h, BOTTOM_LEFT_OBJ.s, BOTTOM_LEFT_OBJ.v)
    print(BOTTOM_MIDDLE_OBJ.h, BOTTOM_MIDDLE_OBJ.s, BOTTOM_MIDDLE_OBJ.v)
    print(BOTTOM_RIGHT_OBJ.h, BOTTOM_RIGHT_OBJ.s, BOTTOM_RIGHT_OBJ.v)
    print()
    print("P: ", (BOTTOM_LEFT - BOTTOM_RIGHT) * DEFAULTPROPORTION)
    print("I: ", DEFAULTI * ACCUMI)
    print("D: ", DEFAULTD * ACCUMD)
    BEFLNUM = BOTTOM_LEFT
    BEFRNUM = BOTTOM_RIGHT
