import socket
import time
import msgpack

ip = '2001:470:66:3f9::2'
port = 1525

data = ["powRGB1", 50]
data = ["setRGB1", (0,255,255)]

data = ["trSetup", [1, int(time.time())+10, "powRGB1", [0]]]
sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
sock.sendto(msgpack.packb(data),(ip, port))
data = ["trSetup", [2, int(time.time())+10, "powRGB2", [0]]]
sock.sendto(msgpack.packb(data),(ip, port))
data = ["powRGB1", 50]
sock.sendto(msgpack.packb(data),(ip, port))
