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
EV3.light.off()


DEBUGPRINT = False
DEBUGMOTOR = False
DEBUGCOLORSENSOR = False
DEFAULTSPEED = 70
DEFAULTTURNSPEED = 70
DEFAULTTIMEWAIT = 0
DEFAULTPROPORTION = 0.24
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
WHITETHRESHOLD = 190
BLACKTHRESHOLD = 73
SATURATIONTHRESHOLD = 150
BEFLNUM = 0
BEFRNUM = 0
TIMESTAMP = ""
TIMESTAMPCNT = 0
BEFORETIMESTAMP = ""
CNT = 0
ISRESCUE = False

client = TechnoClient(host="roboberry.local", port=8085)
CLIENT_LEFT_TOP_X = 102
CLIENT_LEFT_TOP_Y = 0
CLIENT_RIGHT_BOTTOM_X = 1052
CLIENT_RIGHT_BOTTOM_Y = 648
HORIZONTAL_BOX = 3
VERTICAL_BOX = 3
HORIZONTAL_GAP = 125
VERTICAL_GAP = 25

BASEDEGREE = 0
ARMDEGREE = 0

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
        return client.rescue(debug=True)


def isgreenhue(hue: int):
    return 150 <= hue <= 210


LINE_TRACE_SENSOR = LINE()
RESCUE_OBJECT_DETECTION_SENSOR = RESCUE_OBJ_DETECTION()


def updatedata():
    global BOTTOM_LEFT, BOTTOM_MIDDLE, BOTTOM_RIGHT, MIDDLE_LEFT, MIDDLE_MIDDLE, MIDDLE_RIGHT, TOP_LEFT, TOP_MIDDLE, TOP_RIGHT, ACCUMI, ACCUMD, BOTTOM_LEFT_OBJ, BOTTOM_RIGHT_OBJ, BOTTOM_MIDDLE_OBJ, MIDDLE_LEFT_OBJ, MIDDLE_MIDDLE_OBJ, MIDDLE_RIGHT_OBJ, TOP_LEFT_OBJ, TOP_MIDDLE_OBJ, TOP_RIGHT_OBJ, BEFLNUM, BEFRNUM, TIMESTAMP
    now = LINE_TRACE_SENSOR.getdata()
    BOTTOM_LEFT = now.colors[2].v
    BOTTOM_MIDDLE = now.colors[5].v
    BOTTOM_RIGHT = now.colors[8].v
    MIDDLE_LEFT = now.colors[1].v
    MIDDLE_MIDDLE = now.colors[4].v
    MIDDLE_RIGHT = now.colors[7].v
    TOP_LEFT = now.colors[0].v
    TOP_MIDDLE = now.colors[3].v
    TOP_RIGHT = now.colors[6].v
    BOTTOM_LEFT_OBJ = now.colors[2]
    BOTTOM_MIDDLE_OBJ = now.colors[5]
    BOTTOM_RIGHT_OBJ = now.colors[8]
    MIDDLE_LEFT_OBJ = now.colors[1]
    MIDDLE_MIDDLE_OBJ = now.colors[4]
    MIDDLE_RIGHT_OBJ = now.colors[7]
    TOP_LEFT_OBJ = now.colors[0]
    TOP_MIDDLE_OBJ = now.colors[3]
    TOP_RIGHT_OBJ = now.colors[6]
    ACCUMI = BOTTOM_LEFT - BOTTOM_RIGHT
    ACCUMD = (BEFLNUM - BEFRNUM) - (BOTTOM_LEFT - BOTTOM_RIGHT)
    TIMESTAMP = str(now.timestamp)
    if BACKCOLOR.reflection()>98:
        ISRESCUE = True


def isblack(h, s, v):
    
    return v < BLACKTHRESHOLD and s < SATURATIONTHRESHOLD


def iswhite(h, s, v):
    return v > WHITETHRESHOLD and s < SATURATIONTHRESHOLD


def isgreen(h, s, v):
    return 50 < h < 85 and SATURATIONTHRESHOLD < s


def isred(h, s, v):
    return (h < 10 or h > 165) and s > SATURATIONTHRESHOLD # TODO need changes


# while True:
# print(LINE_TRACE_SENSOR.getdata())

MOTORARMBASE.run(-150)
MOTORARMHANDS.run(-300)


def uturn():
    global BOTTOM_LEFT_OBJ,BOTTOM_MIDDLE_OBJ,BOTTOM_RIGHT_OBJ,DEFAULTTURNSPEED,MOTORL,MOTORR
    print("uturn")
    while not iswhite(BOTTOM_LEFT_OBJ.h,BOTTOM_LEFT_OBJ.s,BOTTOM_LEFT_OBJ.v) and not iswhite(BOTTOM_RIGHT_OBJ.h,BOTTOM_RIGHT_OBJ.s,BOTTOM_RIGHT_OBJ.v):
        updatedata()
        MOTORL.run(-DEFAULTTURNSPEED)
        MOTORR.run(-DEFAULTTURNSPEED)
    while not iswhite(BOTTOM_MIDDLE_OBJ.h,BOTTOM_MIDDLE_OBJ.s,BOTTOM_MIDDLE_OBJ.v):
        updatedata()
        MOTORL.run(DEFAULTTURNSPEED)
        MOTORR.run(-DEFAULTTURNSPEED)
    while not isblack(BOTTOM_MIDDLE_OBJ.h,BOTTOM_MIDDLE_OBJ.s,BOTTOM_MIDDLE_OBJ.v):
        updatedata()
        MOTORL.run(DEFAULTTURNSPEED)
        MOTORR.run(-DEFAULTTURNSPEED)

# while True:
#     print(LINE_TRACE_SENSOR.getdata().colors[2].v)

time.sleep(2)
BASEDEGREE = MOTORARMBASE.angle()
ARMDEGREE = MOTORARMHANDS.angle()
MOTORARMBASE.track_target(BASEDEGREE)
MOTORARMHANDS.track_target(ARMDEGREE)

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
    UPDEGREE=MOTORARMBASE.angle()
    CNT+=1
    if BEFORETIMESTAMP == TIMESTAMP:
        TIMESTAMPCNT += 1
    else:
        BEFORETIMESTAMP = TIMESTAMP
        TIMESTAMPCNT = 0
    if TIMESTAMPCNT > 5:
        MOTORL.brake()
        MOTORR.brake()
        while TIMESTAMP == BEFORETIMESTAMP:
            print("stopping")
            updatedata()
        BEFORETIMESTAMP = TIMESTAMP
        TIMESTAMPCNT = 0
    MOTORL.run(DEFAULTSPEED + DEFAULTPROPORTION *
               (BOTTOM_LEFT - BOTTOM_RIGHT) + DEFAULTI * ACCUMI +
               DEFAULTD * ACCUMD)
    MOTORR.run(DEFAULTSPEED + DEFAULTPROPORTION *
               (BOTTOM_RIGHT - BOTTOM_LEFT) - DEFAULTI * ACCUMI -
               DEFAULTD * ACCUMD)
    print(BOTTOM_LEFT_OBJ.h, BOTTOM_LEFT_OBJ.s, BOTTOM_LEFT_OBJ.v)
    print(BOTTOM_MIDDLE_OBJ.h, BOTTOM_MIDDLE_OBJ.s, BOTTOM_MIDDLE_OBJ.v)
    print(BOTTOM_RIGHT_OBJ.h, BOTTOM_RIGHT_OBJ.s, BOTTOM_RIGHT_OBJ.v)
    print()
    print("P: ", (BOTTOM_LEFT - BOTTOM_RIGHT) * DEFAULTPROPORTION)
    print("I: ", DEFAULTI * ACCUMI)
    print("D: ", DEFAULTD * ACCUMD)
    if isblack(BOTTOM_LEFT_OBJ.h, BOTTOM_LEFT_OBJ.s, BOTTOM_LEFT_OBJ.v):
        print("left")
        eliftempcnt = 0
        MOTORL.brake()
        MOTORR.brake()
        EV3.speaker.beep(frequency=440)
        while not iswhite(BOTTOM_LEFT_OBJ.h, BOTTOM_LEFT_OBJ.s,
                      BOTTOM_LEFT_OBJ.v) and eliftempcnt < 30:
            updatedata()
            eliftempcnt += 1
            print(eliftempcnt)
            MOTORL.run(DEFAULTTURNSPEED)
            MOTORR.run(DEFAULTTURNSPEED)
            if ISRESCUE:
                break
        while not isblack(BOTTOM_MIDDLE_OBJ.h, BOTTOM_MIDDLE_OBJ.s,
                          BOTTOM_MIDDLE_OBJ.v) and not isblack(
                              BOTTOM_RIGHT_OBJ.h, BOTTOM_RIGHT_OBJ.s,
                              BOTTOM_RIGHT_OBJ.v):
            updatedata()
            MOTORL.run(-DEFAULTTURNSPEED)
            MOTORR.run(DEFAULTTURNSPEED)
            if ISRESCUE:
                break
    elif isblack(BOTTOM_RIGHT_OBJ.h, BOTTOM_RIGHT_OBJ.s, BOTTOM_RIGHT_OBJ.v):
        print("right")
        eliftempcnt = 0
        MOTORL.brake()
        MOTORR.brake()
        EV3.speaker.beep(frequency=460)
        while not iswhite(BOTTOM_RIGHT_OBJ.h, BOTTOM_RIGHT_OBJ.s,
                      BOTTOM_RIGHT_OBJ.v) and eliftempcnt < 30:
            updatedata()
            eliftempcnt += 1
            print(eliftempcnt)
            MOTORL.run(DEFAULTTURNSPEED)
            MOTORR.run(DEFAULTTURNSPEED)
            if ISRESCUE:
                break
        while not isblack(BOTTOM_MIDDLE_OBJ.h, BOTTOM_MIDDLE_OBJ.s,
                          BOTTOM_MIDDLE_OBJ.v) and not isblack(
                              BOTTOM_LEFT_OBJ.h, BOTTOM_LEFT_OBJ.s,
                              BOTTOM_LEFT_OBJ.v):
            updatedata()
            MOTORL.run(DEFAULTTURNSPEED)
            MOTORR.run(-DEFAULTTURNSPEED)
            if ISRESCUE:
                break
    elif isgreen(BOTTOM_LEFT_OBJ.h, BOTTOM_LEFT_OBJ.s, BOTTOM_LEFT_OBJ.v) and CNT >= 30:
        CNT = 0
        print("green left")
        MOTORL.brake()
        MOTORR.brake()
        EV3.speaker.beep(frequency=500)
        if isgreen(BOTTOM_RIGHT_OBJ.h,BOTTOM_RIGHT_OBJ.s,BOTTOM_RIGHT_OBJ.v):
            EV3.speaker.beep(frequency=1000)
            uturn()
            continue
        while not isblack(BOTTOM_LEFT_OBJ.h,BOTTOM_LEFT_OBJ.s,BOTTOM_LEFT_OBJ.v) and not iswhite(BOTTOM_LEFT_OBJ.h,BOTTOM_LEFT_OBJ.s,BOTTOM_LEFT_OBJ.v):
            updatedata()
            MOTORL.run(DEFAULTTURNSPEED)
            MOTORR.run(DEFAULTTURNSPEED)
        if isblack(BOTTOM_LEFT_OBJ.h,BOTTOM_LEFT_OBJ.s,BOTTOM_LEFT_OBJ.v):
            print("detect black")
            while not iswhite(BOTTOM_LEFT_OBJ.h,BOTTOM_LEFT_OBJ.s,BOTTOM_LEFT_OBJ.v):
                updatedata()
                MOTORL.run(DEFAULTTURNSPEED)
                MOTORR.run(DEFAULTTURNSPEED)
            while isblack(BOTTOM_MIDDLE_OBJ.h,BOTTOM_MIDDLE_OBJ.s,BOTTOM_MIDDLE_OBJ.v):
                updatedata()
                MOTORL.run(-DEFAULTTURNSPEED)
                MOTORR.run(DEFAULTTURNSPEED)
            while not isblack(BOTTOM_MIDDLE_OBJ.h,BOTTOM_MIDDLE_OBJ.s,BOTTOM_MIDDLE_OBJ.v):
                updatedata()
                MOTORL.run(-DEFAULTTURNSPEED)
                MOTORR.run(DEFAULTTURNSPEED)
        else:
            print("is white, skipping")
    elif isgreen(BOTTOM_RIGHT_OBJ.h, BOTTOM_RIGHT_OBJ.s, BOTTOM_RIGHT_OBJ.v) and CNT >= 30:
        CNT = 0
        print("green right")
        MOTORL.brake()
        MOTORR.brake()
        EV3.speaker.beep(frequency=600)
        if isgreen(BOTTOM_LEFT_OBJ.h,BOTTOM_LEFT_OBJ.s,BOTTOM_LEFT_OBJ.v):
            EV3.speaker.beep(frequency=1000)
            uturn()
            continue
        while not isblack(BOTTOM_RIGHT_OBJ.h,BOTTOM_RIGHT_OBJ.s,BOTTOM_RIGHT_OBJ.v) and not iswhite(BOTTOM_RIGHT_OBJ.h,BOTTOM_RIGHT_OBJ.s,BOTTOM_RIGHT_OBJ.v):
            updatedata()
            MOTORL.run(DEFAULTTURNSPEED)
            MOTORR.run(DEFAULTTURNSPEED)
        if isblack(BOTTOM_RIGHT_OBJ.h,BOTTOM_RIGHT_OBJ.s,BOTTOM_RIGHT_OBJ.v):
            print("detect black")
            while not iswhite(BOTTOM_RIGHT_OBJ.h,BOTTOM_RIGHT_OBJ.s,BOTTOM_RIGHT_OBJ.v):
                updatedata()
                MOTORL.run(DEFAULTTURNSPEED)
                MOTORR.run(DEFAULTTURNSPEED)
            while isblack(BOTTOM_MIDDLE_OBJ.h,BOTTOM_MIDDLE_OBJ.s,BOTTOM_MIDDLE_OBJ.v):
                updatedata()
                MOTORL.run(DEFAULTTURNSPEED)
                MOTORR.run(-DEFAULTTURNSPEED)
            while not isblack(BOTTOM_MIDDLE_OBJ.h,BOTTOM_MIDDLE_OBJ.s,BOTTOM_MIDDLE_OBJ.v):
                updatedata()
                MOTORL.run(DEFAULTTURNSPEED)
                MOTORR.run(-DEFAULTTURNSPEED)
        else:
            print("is white, skipping")
    elif isred(BOTTOM_RIGHT_OBJ.h,BOTTOM_RIGHT_OBJ.s,BOTTOM_RIGHT_OBJ.v) and isred(BOTTOM_MIDDLE_OBJ.h,BOTTOM_MIDDLE_OBJ.s,BOTTOM_MIDDLE_OBJ.v) and isred(BOTTOM_LEFT_OBJ.h,BOTTOM_LEFT_OBJ.s,BOTTOM_LEFT_OBJ.v):
        MOTORL.brake()
        MOTORR.brake()
        break
    elif TOUCHL.pressed() or TOUCHR.pressed():
        print("pressed")
        EV3.speaker.beep(frequency=700)
        MOTORL.brake()
        MOTORR.brake()
        WASLBLACK = False
        WASRBLACK = False
        MOTORL.run(-DEFAULTTURNSPEED)
        MOTORR.run(-DEFAULTTURNSPEED)
        time.sleep(2)
        MOTORL.run(-DEFAULTTURNSPEED)
        MOTORR.run(DEFAULTTURNSPEED)
        time.sleep(5)
        while True:
            updatedata()
            if TOUCHR.pressed():
                MOTORL.run(DEFAULTTURNSPEED-50)
                MOTORR.run(DEFAULTTURNSPEED)
                time.sleep(0.3)
            else:
                MOTORL.run(DEFAULTTURNSPEED)
                MOTORR.run(DEFAULTTURNSPEED-50)
            if isblack(BOTTOM_LEFT_OBJ.h,BOTTOM_LEFT_OBJ.s,BOTTOM_LEFT_OBJ.v):
                WASLBLACK = True
            if isblack(BOTTOM_RIGHT_OBJ.h,BOTTOM_RIGHT_OBJ.s,BOTTOM_RIGHT_OBJ.v):
                WASRBLACK = True
            if WASLBLACK and WASRBLACK:
                break
        while not isblack(BOTTOM_MIDDLE_OBJ.h,BOTTOM_MIDDLE_OBJ.s,BOTTOM_MIDDLE_OBJ.v):
            updatedata()
            MOTORL.run(-DEFAULTTURNSPEED)
            MOTORR.run(DEFAULTTURNSPEED)
    elif BACKCOLOR.reflection() > 98 or ISRESCUE:
        EV3.speaker.beep(frequency=1000)
        ISRESCUE = False
        MOTORL.brake()
        MOTORR.brake()
        # if not BACKCOLOR.reflection()>98:
        #     continue
        MOTORL.run(90)
        MOTORR.run(100)
        time.sleep(3)
        MOTORARMBASE.track_target(MOTORARMBASE.angle()+150)
        MIDDLE_X = 2304
        while True:
            MOTORL.brake()
            MOTORR.brake()
            rescue_now = RESCUE_OBJECT_DETECTION_SENSOR.getdata()
            print(rescue_now)
            if len(rescue_now.rescue_data)>0:
                MINDIFFCOOR = 100000000
                MINDIFFCOOR_DATA = RescueData("NULL",-1.0,-1,-1,-1,-1)
                GREEN_BOX_DATA = RescueData("NULL",-1.0,-1,-1,-1,-1)
                RED_BOX_DATA = RescueData("NULL",-1.0,-1,-1,-1,-1)
                for i in rescue_now.rescue_data:
                    if i.name == "green_box" and i.probability >= 0.6:
                        if GREEN_BOX_DATA.name == "NULL":
                            GREEN_BOX_DATA = i
                        elif GREEN_BOX_DATA.probability<i.probability:
                            GREEN_BOX_DATA = i
                    elif i.name == "red_box" and i.probability >= 0.6:
                        if RED_BOX_DATA.name == "NULL":
                            RED_BOX_DATA = i
                        elif RED_BOX_DATA.probability<i.probability:
                            RED_BOX_DATA = i
                defaultdivisor = 2
                for i in rescue_now.rescue_data:
                    if (i.name == "silver_ball" or i.name == "black_ball") and i.probability >= 0.6:
                        if abs(MIDDLE_X - (i.right+i.left)//2)<abs(MINDIFFCOOR - MIDDLE_X) and (GREEN_BOX_DATA.top+GREEN_BOX_DATA.bottom)//2 < (i.top+i.bottom)//2:
                            MINDIFFCOOR = (i.right+i.left)//2
                            MINDIFFCOOR_DATA = i
                if MINDIFFCOOR_DATA.name != "NULL" and MINDIFFCOOR_DATA.bottom > 1296 and abs(MIDDLE_X - (MINDIFFCOOR_DATA.right+MINDIFFCOOR_DATA.left)//2)<=400: # TODO need change
                    print(MINDIFFCOOR_DATA.name + " detected as near and middle")
                    MOTORARMHANDS.run(500)
                    time.sleep(2)
                    MOTORARMHANDS.hold()
                    MOTORL.run(250)
                    MOTORR.run(250)
                    time.sleep(2.5)
                    MOTORL.brake()
                    MOTORR.brake()
                    MOTORARMHANDS.run(-500)
                    time.sleep(2)
                    MOTORARMHANDS.hold()
                    while True:
                        rescue_now = RESCUE_OBJECT_DETECTION_SENSOR.getdata()
                        BOX_OBJ = []
                        if len(rescue_now.rescue_data)>0:
                            for i in rescue_now.rescue_data:
                                if MINDIFFCOOR_DATA.name == "silver_ball":
                                    if i.name == "green_box":
                                        BOX_OBJ = i
                                elif MINDIFFCOOR_DATA.name == "black_ball":
                                    if i.name == "red_box":
                                        BOX_OBJ = i
                        if BOX_OBJ != []:
                            if BOX_OBJ.bottom > 1296 and abs(MIDDLE_X - (BOX_OBJ.right+BOX_OBJ.left)//2)<=500:
                                MOTORARMBASE.track_target(MOTORARMBASE.angle()-150)
                                while not TOUCHL.pressed() and not TOUCHR.pressed():
                                    MOTORL.run(300)
                                    MOTORR.run(300)
                                MOTORL.run(300)
                                MOTORR.run(300)
                                time.sleep(2)
                                MOTORL.brake()
                                MOTORR.brake()
                                MOTORARMBASE.track_target(MOTORARMBASE.angle()+90)
                                MOTORARMHANDS.run(500)
                                time.sleep(2)
                                MOTORARMHANDS.hold()
                                MOTORARMBASE.track_target(MOTORARMBASE.angle()-90)
                                MOTORL.run(-300)
                                MOTORR.run(-300)
                                MOTORARMHANDS.run(-500)
                                MOTORARMHANDS.hold()
                                time.sleep(3)
                                MOTORARMBASE.track_target(MOTORARMBASE.angle()+150)
                                break
                            elif abs(MIDDLE_X - (BOX_OBJ.right+BOX_OBJ.left)//2)<=400 and BOX_OBJ.bottom>1296:
                                MOTORL.run(-100)
                                MOTORR.run(-100)
                                time.sleep(0.9)
                                MOTORL.brake()
                                MOTORR.brake()
                            elif abs(MIDDLE_X - (BOX_OBJ.right+BOX_OBJ.left)//2)<=400 and BOX_OBJ.bottom<=1296:
                                MOTORL.run(100)
                                MOTORR.run(100)
                                time.sleep(1.2)
                                MOTORL.brake()
                                MOTORR.brake()
                            elif MIDDLE_X < (BOX_OBJ.right+BOX_OBJ.left)//2:
                                MOTORL.run(100)
                                MOTORR.run(-100)
                                time.sleep(0.5)
                                MOTORL.brake()
                                MOTORR.brake()
                            elif MIDDLE_X > (BOX_OBJ.right+BOX_OBJ.left)//2:
                                MOTORL.run(-100)
                                MOTORR.run(100)
                                time.sleep(0.5)
                                MOTORL.brake()
                                MOTORR.brake()
                            else:
                                MOTORL.run(-100)
                                MOTORR.run(100)
                                time.sleep(1)
                                MOTORL.brake() # may change due to
                                MOTORR.brake() # the place
                        else:
                            MOTORL.run(-100)
                            MOTORR.run(100)
                            time.sleep(2)
                            MOTORL.brake()
                            MOTORR.brake()
                elif MINDIFFCOOR_DATA.name == "NULL":
                    MOTORL.run(-100) # may change due to
                    MOTORR.run(100)  # the place
                    time.sleep(1)
                    MOTORL.brake()
                    MOTORR.brake()
                elif abs(MIDDLE_X - MINDIFFCOOR) <= 400:
                    MOTORL.run(100)
                    MOTORR.run(100)
                    time.sleep(0.7)
                    MOTORL.brake()
                    MOTORR.brake()
                    if MINDIFFCOOR_DATA.bottom > 1296:
                        MOTORL.run(-100)
                        MOTORR.run(-100)
                        time.sleep(2)
                        MOTORL.brake()
                        MOTORR.brake()
                elif MIDDLE_X > MINDIFFCOOR:
                    MOTORL.run(-100)
                    MOTORR.run(100)
                    time.sleep(0.7)
                    MOTORL.brake()
                    MOTORR.brake()
                    if MINDIFFCOOR_DATA.bottom > 1296:
                        MOTORL.run(-100)
                        MOTORR.run(-100)
                        time.sleep(1)
                        MOTORL.brake()
                        MOTORR.brake()
                elif MIDDLE_X < MINDIFFCOOR:
                    MOTORL.run(100)
                    MOTORR.run(-100)
                    time.sleep(0.7)
                    MOTORL.brake()
                    MOTORR.brake()
                    if MINDIFFCOOR_DATA.bottom > 1296:
                        MOTORL.run(-100)
                        MOTORR.run(-100)
                        time.sleep(1)
                        MOTORL.brake()
                        MOTORR.brake()
                continue
            else:
                MOTORL.run(-100)
                MOTORR.run(100)
                time.sleep(1)
                MOTORL.brake()
                MOTORR.brake()
    BEFLNUM = BOTTOM_LEFT
    BEFRNUM = BOTTOM_RIGHT
