import socket
import time

from .techno_data import LineResult, RescueResult

RETRY_MAX = 3


class TechnoClient:

    def __init__(self,
                 host: str = "roboberry.local",
                 port: int = 8085,
                 timeout: int = 60,
                 buffer_size: int = 4096) -> None:
        self.__host = host
        self.__port = port
        self.__timeout = timeout
        self.__buffer_size = buffer_size
        self.__socket = None

    def __del__(self):
        self.close()

    def connect(self) -> None:
        if self.__socket is not None:
            return

        self.__socket = socket.socket()
        # self.__socket.settimeout(self.__timeout) # timeout is not supported on ev3
        addr = socket.getaddrinfo(self.__host, self.__port, 0,
                                  socket.SOCK_STREAM)[-1][-1]
        self.__socket.connect(addr)

    def close(self) -> None:
        if self.__socket is None:
            return

        try:
            self.__socket.shutdown(socket.SHUT_RDWR)
        except Exception as ex:
            pass
            self.__log("socket shutdown exception:" + str(type(ex)) + ":" + str(ex))

        try:
            self.__socket.close()
        except Exception as ex:
            pass
            self.__log("socket close exception:" + str(type(ex)) + ":" + str(ex))

        self.__socket = None

    def line(self,
             debug: bool = False) -> str:
        send_msg = "l"
        if debug:
            send_msg += " -d"

        return LineResult(self.__request_server(send_msg))

    def line_info(self,
                  left: int = 420, top: int = 0,
                  right: int = 1500, bottom: int = 1080,
                  box_count_h: int = 3, box_count_v: int = 3,
                  box_gap_h: int = 100, box_gap_v: int = 100) -> str:
        send_msg = "li"
        send_msg += " -l " + str(left)
        send_msg += " -t " + str(top)
        send_msg += " -r " + str(right)
        send_msg += " -b " + str(bottom)
        send_msg += " --ch " + str(box_count_h)
        send_msg += " --cv " + str(box_count_v)
        send_msg += " --gh " + str(box_gap_h)
        send_msg += " --gv " + str(box_gap_v)
        return self.__request_server(send_msg)

    def rescue(self, debug: bool = False) -> str:
        send_msg = "r"
        if debug:
            send_msg += " -d"

        return RescueResult(self.__request_server(send_msg))

    def clear_debug_image(self) -> str:
        return self.__request_server("ci")

    def __ts(self) -> str:
        lt = time.localtime()
        return '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(
            lt[0], lt[1], lt[2], lt[3], lt[4], lt[5])

    def __log(self, msg) -> None:
        print(self.__ts() + msg)
        pass

    def __request_server(self, message: str, retry_count: int = 0):
        try:
            self.connect()
            self.__socket.send(message.encode("utf-8"))
            received = self.__socket.recv(self.__buffer_size).decode("utf-8")

            received_ar = received.split(",")

            if len(received_ar) == 0:
                if retry_count < RETRY_MAX:
                    self.close()
                    return self.__request_server(message, (retry_count + 1))
                else:
                    return None

            return received_ar

        except Exception as ex:
            self.__log("__request_server exception:" + str(type(ex)) + ":" + str(ex))
            self.close()
            if retry_count < RETRY_MAX:
                return self.__request_server(message, (retry_count + 1))

        return None
