import getopt
import math
import socket
import struct
import sys
import time

port = 12345

def mean_sd(vals):
    m = 0.0
    s = 0.0
    i = 0
    
    for v in vals:
        i += 1
        v -= m
        m += v / i
        s += (i - 1) * v * v / i
    s = math.sqrt(s / len(vals))
    return m, s

def tcping(host=''):
    try:
        local = socket.gethostbyname(socket.gethostname())
        peer = socket.gethostbyname(host)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.settimeout(10)

        try:
            rtts = []
            s.connect((host, port))
            for i in range(10):
                echo = struct.pack('d', time.time())
                s.sendall(echo)
                data = s.recv(1024)
                if not data:
                    break
                now = time.time()
                resp = struct.unpack('d', data)
                rtt = (now - resp[0]) * 1000.0
                rtts.append(rtt)
                print('%d: %s <-> %s %f ms' % (i, local, peer, rtt))
                #print('  %f %f' % (resp[1] - resp[0], now - resp[1]))
                time.sleep(1)
        finally:
            s.close()
    except IOError, e:
        print('Error: %s' % e)

    print("avg/stddev = %f/%f ms" % mean_sd(rtts))

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:")
    except getopt.GetoptError:
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-p':
            port = int(arg)

    tcping(args[0])
