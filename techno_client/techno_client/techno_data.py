
IDX_STATUS = 0
IDX_HEIGHT = 1
IDX_WIDTH = 2
IDX_TIMESTAMP = 3
IDX_DATA_COUNT = 4

STATUS_ERROR = 'error'
STATUS_OK = 'ok'


class HSVColor:
    def __init__(self, h, s, v):
        self.__h = h
        self.__s = s
        self.__v = v

    def __str__(self):
        return "HSVColor(%d,%d,%d)" % (self.__h, self.__s, self.__v)

    @property
    def h(self):
        return self.__h

    @h.setter
    def h(self, h):
        self.__h = h

    @property
    def s(self):
        return self.__s

    @s.setter
    def s(self, s):
        self.__s = s

    @property
    def v(self):
        return self.__v

    @v.setter
    def v(self, v):
        self.__v = v


class LineResult:
    def __init__(self, received_ar) -> None:
        if received_ar is None:
            self.status = STATUS_ERROR
            self.error_message = "received_ar is None"
            return

        ar_len = len(received_ar)
        if received_ar[IDX_STATUS] == STATUS_ERROR:
            if ar_len == 2:
                self.status = received_ar[IDX_STATUS]
                self.error_message = received_ar[1]
            else:
                self.error_message = "unknown error"
            return

        if ar_len < 5:
            self.status = STATUS_ERROR
            self.error_message = "invalid receive length. length="+str(ar_len)
            return

        box_count = int(received_ar[IDX_DATA_COUNT])
        if (ar_len != (5 + (box_count * 3))):
            self.status = STATUS_ERROR
            self.error_message = "invalid box_data len. length=" + \
                str(ar_len) + "box_count="+str(box_count)
            return

        self.status = received_ar[0]
        self.image_height = int(received_ar[IDX_HEIGHT])
        self.image_width = int(received_ar[IDX_WIDTH])
        self.timestamp = received_ar[IDX_TIMESTAMP]
        colors = []
        for i in range(box_count):
            colors.append(
                HSVColor(int(received_ar[IDX_DATA_COUNT + 1 + (i * 3)]),
                         int(received_ar[IDX_DATA_COUNT + 2 + (i * 3)]),
                         int(received_ar[IDX_DATA_COUNT + 3 + (i * 3)]),))

        self.colors = colors

    def __str__(self) -> str:
        res = "LineResult: "
        if self.status == STATUS_ERROR:
            res += "status("+str(self.status)+")" + \
                ", error_message("+str(self.error_message)+")"
        else:
            res += "status("+str(self.status)+")" + ", image_height("+str(self.image_height)+")" + ", image_width("+str(
                self.image_width)+")" + ", color.size("+str(len(self.colors))+")" + ", timestamp("+str(self.timestamp)+")"

            for c in self.colors:
                res += " "+str(c)

        return res

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, status: str) -> None:
        self.__status = status

    @property
    def error_message(self) -> str:
        return self.__error_message

    @error_message.setter
    def error_message(self, error: str) -> None:
        self.__error_message = error

    @property
    def image_height(self) -> int:
        return self.__image_height

    @image_height.setter
    def image_height(self, val: int) -> None:
        self.__image_height = val

    @property
    def image_width(self) -> int:
        return self.__image_width

    @image_width.setter
    def image_width(self, val: int) -> None:
        self.__image_width = val

    @property
    def colors(self) -> list[HSVColor]:
        return self.__colors

    @colors.setter
    def colors(self, val: list[HSVColor]) -> None:
        self.__colors = val

    @property
    def timestamp(self) -> str:
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, val: str) -> None:
        self.__timestamp = val


class RescueData:
    def __init__(self, name: str, probability: float,
                 left: int, top: int, right: int, bottom: int):
        self.name = name
        self.probability = probability
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def __str__(self):
        return "RescueData[(%s, %.3f)(%d,%d,%d,%d)]" % (
            self.name,
            self.probability,
            self.left, self.top,
            self.right, self.bottom)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, val: str):
        self.__name = val

    @property
    def probability(self) -> float:
        return self.__probability

    @probability.setter
    def probability(self, val: float):
        self.__probability = val

    @property
    def left(self) -> int:
        return self.__left

    @left.setter
    def left(self, val: int):
        self.__left = val

    @property
    def top(self) -> int:
        return self.__top

    @top.setter
    def top(self, val: int):
        self.__top = val

    @property
    def right(self) -> int:
        return self.__right

    @right.setter
    def right(self, val: int):
        self.__right = val

    @property
    def bottom(self) -> int:
        return self.__bottom

    @bottom.setter
    def bottom(self, val: int):
        self.__bottom = val


class RescueResult:
    def __init__(self, received_ar) -> None:
        if received_ar is None:
            self.status = STATUS_ERROR
            self.error_message = "received_ar is None"
            return

        ar_len = len(received_ar)
        if received_ar[IDX_STATUS] == STATUS_ERROR:
            if ar_len == 2:
                self.status = received_ar[IDX_STATUS]
                self.error_message = received_ar[1]
            else:
                self.error_message = "unknown error"
            return

        if ar_len < 4:
            self.status = STATUS_ERROR
            self.error_message = "invalid receive length. length="+str(ar_len)
            return

        data_count = int(received_ar[IDX_DATA_COUNT])
        if (ar_len != (5 + (data_count * 6))):
            self.status = STATUS_ERROR
            self.error_message = "invalid data_count len. length=" + \
                str(ar_len)+"box_count="+str(data_count)
            return

        self.status = received_ar[0]
        self.image_height = int(received_ar[IDX_HEIGHT])
        self.image_width = int(received_ar[IDX_WIDTH])
        self.timestamp = received_ar[IDX_TIMESTAMP]
        rescue_data = []
        for i in range(data_count):
            rescue_data.append(RescueData(
                received_ar[IDX_DATA_COUNT + 1 + (i * 6)],
                float(received_ar[IDX_DATA_COUNT + 2 + (i * 6)],),
                int(received_ar[IDX_DATA_COUNT + 3 + (i * 6)],),
                int(received_ar[IDX_DATA_COUNT + 4 + (i * 6)],),
                int(received_ar[IDX_DATA_COUNT + 5 + (i * 6)],),
                int(received_ar[IDX_DATA_COUNT + 6 + (i * 6)],),
            ))

        self.rescue_data = rescue_data

    def __str__(self):
        res = "RescueResult: "
        if self.status == STATUS_ERROR:
            res += "status("+str(self.status)+")" + \
                ", error_message("+str(self.error_message)+")"
        else:
            res += "status("+str(self.status)+")" + ", image_height("+str(self.image_height)+")" + ", image_width("+str(
                self.image_width)+")" + ", timestamp("+str(self.timestamp)+")" + ", rescue_data.size("+str(len(self.rescue_data))+")"

            for r in self.rescue_data:
                res += ", "+str(r)

        return res

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, status: str) -> None:
        self.__status = status

    @property
    def error_message(self) -> str:
        return self.__error_message

    @error_message.setter
    def error_message(self, error: str) -> None:
        self.__error_message = error

    @property
    def image_height(self) -> int:
        return self.__image_height

    @image_height.setter
    def image_height(self, val: int) -> None:
        self.__image_height = val

    @property
    def image_width(self) -> int:
        return self.__image_width

    @image_width.setter
    def image_width(self, val: int) -> None:
        self.__image_width = val

    @property
    def rescue_data(self) -> list[RescueData]:
        return self.__rescue_data

    @rescue_data.setter
    def rescue_data(self, val: list[RescueData]) -> None:
        self.__rescue_data = val

    @property
    def timestamp(self) -> str:
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, val: str) -> None:
        self.__timestamp = val
