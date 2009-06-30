import getopt
import sys
import socket
import struct
import time

port = 12345

def tcpingd():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    s.bind(('', port))
    s.listen(5)

    try:
        while True:
            conn, addr = s.accept()
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                #echo = struct.unpack('d', data)
                #resp = struct.pack('dd', echo[0], time.time())
                conn.sendall(data)

    except socket.error, e:
        print('Error: %s' % e)

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:")
    except getopt.GetoptError:
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-p':
            port = int(arg)

    tcpingd()
