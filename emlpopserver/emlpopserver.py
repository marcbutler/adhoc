# Minimal POP3 server for bring eml files into Outlook.
#
# Serves up a directory of eml files as if it where a POP server
# allowing easy import into Outlook.
#
# RFC1939 - Post Office Protocol - Version 3
#

import sys
import os
import SocketServer
import random

eml_files = []

class EmlFile:
    def __init__(self, dir, name):
        self.dir = dir
        self.name = name
        self.path = os.path.join(dir, name)
        self.id = rand_string()

    def get_size(self):
        (_, _, _, _, _, _, size, _, _, _) = os.stat(self.path)
        return size

    def send_msg(self, response):
        emlfile = file(self.path, 'rb')
        while 1:
            buf = emlfile.read(1024)
            if buf == '': break
            response.send(buf)
        emlfile.close()

def stat_response():
    totsize = 0
    for eml in eml_files:
        totsize += eml.get_size()
    return '%s %d' % (len(eml_files), totsize)

def rand_string():
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for x in xrange(20)])

class PopRequestHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        print self.client_address, 'connected'
        self.request.send('+OK POP3 localhost ready\r\n')

    def send_ok(self, text=''):
        self.request.send('+OK %s\r\n' % text)

    def send_dot(self):
        self.request.send('.\r\n')

    def handle(self):
        while 1:
            data = self.request.recv(1024)
            cmd = data.strip()
            if cmd == 'QUIT':
                return
            elif cmd == 'AUTH':
                self.request.send('+OK\r\n')
                self.request.send('PLAIN\r\n')
                self.request.send('.\r\n')
            elif cmd == 'STAT':
                self.request.send('+OK %s\r\n' % (stat_response()))
            elif cmd == 'UIDL':
                self.send_ok()
                num = 1
                for eml in eml_files:
                    self.request.send('%d %s\r\n' % (num, eml_files[num - 1].id))
                    num += 1
                self.request.send('.\r\n')
            elif cmd == 'LIST':
                self.send_ok()
                num = 1
                for eml in eml_files:
                    self.request.send('%d %d\r\n' % (num, eml_files[num - 1].get_size()))
                    num += 1
                self.send_dot()
            elif cmd[:4] == 'RETR':
                (_, id) = cmd.split(' ')
                id = int(id)
                eml = eml_files[id - 1]
                self.request.send('+OK %d octets\r\n' % eml.get_size())
                eml_files[id - 1].send_msg(self.request)
                self.send_dot()
                print 'Downloaded %s' % eml_files[id - 1].path
            else:
                self.send_ok()

    def finish(self):
        print self.client_address, 'disconnected'
        self.request.send('+OK BYE\r\n')

if len(sys.argv) <> 2:
    print 'Usage: %s eml-directory' % sys.argv[0]
    sys.exit(1)

files = [name for name in os.listdir(sys.argv[1]) if name[-4:] == '.eml']

for name in files:
    eml_files.append(EmlFile(sys.argv[1], name))

print 'Serving %d files.' % (len(eml_files))

server = SocketServer.ThreadingTCPServer(('', 1110), PopRequestHandler)
server.serve_forever()