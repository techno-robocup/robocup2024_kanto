#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import urequests

EV3 = EV3Brick()
MOTORL = Motor(Port.C)
MOTORR = Motor(Port.D)
MOTORARMBASE = Motor(Port.B)
MOTORARMHANDS = Motor(Port.A)
TOUCHL = TouchSensor(Port.S4)
TOUCHR = TouchSensor(Port.S3)

DEBUGPRINT = False
DEBUGMOTOR = False
DEBUGCOLORSENSOR = False
DEFAULTSPEED = 140
DEFAULTPROPORTION = 1.1
DEFAULTI = 0.00055
DEFAULTD = 15
ACCUMI = 0
ACCUMD = 0
WHITETHRESHOLD = 100
BLACKTHRESHOLD = 50
BEFLNUM = 0
BEFRNUM = 0
cnt = 0

class LINE:
  def __init__(self, vertical, horizontal):
    self.target_url = f"http://roboberry.local:81/techno_cam/line_colors?latlx=1008&latly=0&labrx=3608&labry=2592&bc_h={str(horizontal)}&bc_v={str(vertical)}&bg_h=50&bg_v=50"
  def getdata(self):
    try:
      json_data = urequests.get(self.target_url).json
    except:
      return None
    return json_data["colors"]

class RESCUE_OBJ_DETECTION:
  def __init__(self):
    self.target_url = "http://roboberry.local:81/techno_cam/rescue_objects"
  def getdata(self):
    try:
      json_data = urequests.get(self.target_url).json
    except:
      return None
    return json_data["objects"]

def isgreenhue(hue: int):
  return 150<=hue<=210

LINE_TRACE_SENSOR = LINE(3,3)
RESCUE_OBJECT_DETECTION_SENSOR = RESCUE_OBJ_DETECTION()
while True:
  cnt+=1
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
  if now := LINE_TRACE_SENSOR.getdata() is None:
    continue
  else:
    ISUM=now[1][0]-now[7][0]
    DSUM=(BEFLNUM-BEFRNUM)-(now[1][0]-now[7][0])
    MOTORL.run(DEFAULTSPEED + DEFAULTPROPORTION * (now[1][0]-now[7][0])+DEFAULTI*ACCUMI+DEFAULTD*ACCUMD)
    MOTORR.run(DEFAULTSPEED + DEFAULTPROPORTION * (now[7][0]-now[1][0])-DEFAULTI*ACCUMI-DEFAULTD*ACCUMD)
    BEFLNUM=now[1][0]
    BEFRNUM=now[7][0]
  if cnt>=20 and BLACKTHRESHOLD>=now[1][0] and not BLACKTHRESHOLD>=now[7][0]:
    EV3.speaker.beep()
    while BLACKTHRESHOLD>=now[1][0]:
      now=LINE_TRACE_SENSOR.getdata()
      MOTORL.run(200)
      MOTORR.run(200)
    while not BLACKTHRESHOLD>=now[7][0]:
      now=LINE_TRACE_SENSOR.getdata()
      MOTORL.run(-200)
      MOTORR.run(200)
    MOTORL.run(200)
    MOTORR.run(-200)
    time.sleep(0.3)
    cnt = 0
  if cnt>=20 and BLACKTHRESHOLD>=now[7][0] and not BLACKTHRESHOLD>=[1][0]:
    EV3.speaker.beep()
    while BLACKTHRESHOLD>=[7][0]:
      now=LINE_TRACE_SENSOR.getdata()
      MOTORL.run(200)
      MOTORR.run(200)
    while not BLACKTHRESHOLD>=now[1][0]:
      now=LINE_TRACE_SENSOR.getdata()
      MOTORL.run(200)
      MOTORR.run(-200)
    MOTORL.run(-200)
    MOTORR.run(200)
    time.sleep(0.3)
    cnt=0
