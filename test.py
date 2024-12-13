import requests
class LINE:

    def __init__(self, vertical, horizontal):
        self.target_url = "http://roboberry.local:81/techno_cam/line_colors?latlx=1008&latly=0&labrx=3608&labry=2592&bc_h="+str(horizontal)+"&bc_v="+str(vertical)+"&bg_h=50&bg_v=50"

    def getdata(self):
        try:
            json_data = requests.get(self.target_url).json
        except:
            return None
        return json_data["colors"]


class RESCUE_OBJ_DETECTION:

    def __init__(self):
        self.target_url = "http://roboberry.local:81/techno_cam/rescue_objects"

    def getdata(self):
        try:
            json_data = requests.get(self.target_url).json
        except:
            return None
        return json_data["objects"]

LINE_TRACE_SENSOR = LINE(3, 3)
RESCUE_OBJECT_DETECTION_SENSOR = RESCUE_OBJ_DETECTION()

while True:
    print(requests.get("http://roboberry.local:81/techno_cam/line_colors?latlx=1008&latly=0&labrx=3608&labry=2592&bc_h="+str(3)+"&bc_v="+str(3)+"&bg_h=50&bg_v=50").json())
    # print(RESCUE_OBJECT_DETECTION_SENSOR.getdata())
