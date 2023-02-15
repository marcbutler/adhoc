#!/usr/bin/env python
# Copyright (c) 2006 Marc Butler

# Merged hextostr.py and strtohex.py into a single tool for converting strings
# to and from hex and improved slightly.

import sys

def str_to_hex(str):
    return ''.join(['%02X' % (ord(c)) for c in str])

def hex_to_str(hexstr):
    str = ''
    while len(hexstr) >= 2:
        v = int(hexstr[:2], 16)
        str += '%c' % v
        hexstr = hexstr[2:]
    return str

if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[1] not in ["to", "from"]:
        print '''Usage: hexstr.py to|from <string>
to = convert hex to a string
from = convert from hex to a string        
'''
        sys.exit(1)
    else:
        if sys.argv[1] == "to":
            print hex_to_str(sys.argv[2])
        else:
            print str_to_hex(sys.argv[2])
        sys.exit(0)
