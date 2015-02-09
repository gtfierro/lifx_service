import socket
import time
import msgpack
import random

ip = '2001:470:66:3f9::2'
port = 1525

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

data = ["powRGB1", 100]
sock.sendto(msgpack.packb(data),(ip, port))

data = ["powRGB2", 100]
sock.sendto(msgpack.packb(data),(ip, port))

while 1:
        x = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
        print(x)
        data = ["setRGB1", x]
        sock.sendto(msgpack.packb(data),(ip, port))

        print(x)
        x = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
        data = ["setRGB2", x]
        sock.sendto(msgpack.packb(data),(ip, port))

        time.sleep(2)

