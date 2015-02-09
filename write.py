import socket
import time
import msgpack

ip = '2001:470:66:3f9::2'
port = 1525

data = ["powRGB1", 100]
data = ["setRGB1", (254,255,255)]

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
i = 1
while 1:
    print('sending',i)
    sock.sendto(msgpack.packb(data),(ip, port))
    i += 1
    time.sleep(5)
