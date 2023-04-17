#!/usr/bin/env python3

import re
import sys
if __name__ == '__main__':
    for line in sys.stdin.readlines():
        line = line.strip()
        if re.match('^\s*$', line):
            next
        elif m := re.match(r'^#(\d+)\s.*\s(\S+)\s\(.*\).*/data/src/wiredtiger/(.*)$', line):
            frm, fnc, src = m.group(1), m.group(2), m.group(3)
            print('{0:>2}  {1:30}  {2}'.format(frm, fnc, src))
        elif m := re.match(r'.* \(.*\(LWP (\d+)\)\)', line):
            print('\nThread', m.group(1))
