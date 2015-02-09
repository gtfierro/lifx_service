import socket
import time
import msgpack

ip = '2001:470:4956:1:6203:8ff:fe9e:d1d0'
port = 1525

data = ["powRGB1", 50]
data = ["setRGB1", (0,255,255)]

data = ["trSetup", [1, 4, "powRGB1", [0]]]
sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
sock.sendto(msgpack.packb(data),(ip, port))
