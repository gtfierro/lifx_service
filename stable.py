from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.internet import task
from binascii import hexlify
import msgpack
import socket
import lifx

stable = { 'id': 'LiFX'}

_lights = {}
for i, l in enumerate(lifx.get_lights()):
    _lights['setRGB{0}'.format(i+1)] = l
    _lights['powRGB{0}'.format(i+1)] = l
    stable['setRGB{0}'.format(i+1)] = {'s': 'setRGBLed'}
    stable['powRGB{0}'.format(i+1)] = {'s': 'setBool'}

stable['trSetup'] = {'s': ""}
stable['trAbort'] = {'s': ""}

print(_lights)

transactions = {}

class LiFXService(DatagramProtocol):
    def sendError(self, msg, addr):
        print(msg)
        self.transport.write(msgpack.packb({'error': msg}), addr)

    def datagramReceived(self, data, addr):
        # unpack msgpack packet
        try:
            cmd = msgpack.unpackb(data)
        except:
            self.sendError('invalid msgpack', addr)
            return
        # check the arguments
        if len(cmd) != 2:
            self.sendError('wrong number of arguments',addr)
            return
        cmd[0] = cmd[0].decode(encoding='utf-8')
        print("received {0} from {1}".format(cmd, addr))
        if cmd[0] not in list(stable.keys()):
            self.sendError('method {0} not advertised'.format(cmd[0]), addr)
            return
        success = False
        if cmd[0] == 'trSetup':
            success = self.trSetup(cmd, addr)
        elif cmd[0] == 'trAbort':
            success = self.trAbort(cmd)
        else:
            self.doCmd(cmd[0],cmd[1], addr)

    def doCmd(self, stablename, args, addr):
        if stablename.startswith('set'):
            success = self.set((stablename, args), addr)
        else:
            success = self.pow((stablename, args), addr)

        if success:
            self.transport.write(msgpack.packb({'error': False}), addr)

    def trSetup(self, cmd, addr):
        tx_id, time, fn, arglist = cmd[1]
        fn = fn.decode(encoding='utf-8')
        if tx_id in transactions:
            self.sendError('already has tx with ID {0}'.format(tx_id), addr)
            return
        
        transactions[tx_id] = reactor.callLater(time, lambda : self.doCmd(fn, arglist[0], addr))
        return True

    def trAbort(self, cmd):
        tx_id = cmd[1]
        if transactions[tx_id]:
                transactions[tx_id].cancel()
                del transactions[tx_id]
        return True

    def set(self, cmd, addr):
        if isinstance(cmd[1], list) and len(cmd[1]) == 3:
            colors = map(lambda x: x / 255., cmd[1])
            h,s,b = RGBtoHSB(*colors)
            l = _lights[cmd[0]]
            l.set_power(True)
            l.set_color(int((h / 360.) * 0xffff), int(s * 0xffff), int(b * 0xffff), 6500, 100)
        else:
            self.sendError('argument {0} to {1} was invalid. Expected length-3 array'.format(cmd[1],cmd[0]), addr)
            return False
        return True

    def pow(self, cmd, addr):
        if isinstance(cmd[1], int) and 0 <= cmd[1] and 100 >= cmd[1]:
            l = _lights[cmd[0]]
            l.set_power(cmd[1] > 0)
            l.set_color(l.hue,l.saturation, int((cmd[1] / 100.) * 0xffff), l.kelvin, 100)
        else:
            self.sendError('argument {0} to {1} was invalid. Expected int between0  and 10'.format(cmd[1],cmd[0]), addr)
            return False
        return True

def RGBtoHSB(r,g,b):
    min_col = min(r,g,b)
    max_col = max(r,g,b)
    brightness = max_col
    delta = max_col - min_col
    if max != 0:
        saturation = delta / float(max_col)
    else:
        saturation = 0
        hue = -1
        return hue, saturation, brightness
    
    if r == max_col:
        hue = (g - b) / float(delta)
    elif (g == max_col):
        hue = 2 + ( b - r) / float(delta)
    else:
        hue = 4 + (r - g) / float(delta)

    hue *= 60
    if hue < 0:
        hue += 360
    
    return map(int, (hue, saturation, brightness))
        
        
sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
print('ADVERTISING',stable)
def dobcast():
    try:
        sock.sendto(msgpack.packb(stable), ('ff02::1',1525))
    except Exception as e:
        print('error broadcasting',e)

l = LiFXService()

reactor.listenUDP(1525, l, interface='::')

bcast = task.LoopingCall(dobcast)
bcast.start(10)

reactor.run()
