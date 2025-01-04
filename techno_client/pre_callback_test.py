import datetime
import time

import cv2
from picamera2 import MappedArray, Picamera2

TS_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


def log(msg):
    ts = datetime.datetime.now().strftime(TS_FORMAT)
    print(f"{ts} {msg}")


log("start")


def callback(request):
    log("callback start")
    timestamp = time.strftime("%Y-%m-%d %X")
    with MappedArray(request, "main") as m:
        cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)
    log("callback end")


picam2 = Picamera2()
colour = (0, 255, 0)
origin = (0, 30)
font = cv2.FONT_HERSHEY_SIMPLEX
scale = 1
thickness = 2


picam2.pre_callback = callback
log("camera start")
picam2.start()

log("start sleep")
time.sleep(5)
log("end sleep")

log("pooling start")
for x in range(10):
    time.sleep(1)
log("pooling end")

log("capture array start")
array = picam2.capture_array("main")
log("capture array end")

log("camera stop")
picam2.stop()

log("end")
