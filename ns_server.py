import json
import socket
import sys
from thread import *
from util import call_cmd


HOST = ''
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

s.listen(10)
print 'Listening command'


def clientthread(conn):
    conn.send('Welcome 200 OK.\n')  # send only takes string
    while True:
        data = conn.recv(1024)
        data = str(data).split(":")
        if data.__len__() == 2:
            cmd = data[0]
            reply = {}
            for item in str(data[1]).split(','):
                st, d = call_cmd(cmd, item)
                reply[item] = d
            reply = json.dumps({"ok": True, "data": reply})
            if not data:
                break
        else:
            reply = json.dumps({"ok": False, "message": "Command not found"})
        conn.sendall(reply)
        break
    conn.close()


while 1:
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    start_new_thread(clientthread, (conn,))

s.close()