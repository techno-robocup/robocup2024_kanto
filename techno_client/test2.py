import socket

s = socket.socket()
addr = socket.getaddrinfo("roboberry.local", 8085, 0,
                                  socket.SOCK_STREAM)[-1][-1]
s.connect(addr)
s.send("l".encode("utf-8"))
r = s.recv(4096).decode("utf-8")
print(r)
print(r.split(","))