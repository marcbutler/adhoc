# Copyright (c) 2007 Marc Butler.
# All Rights Reserved. Absolutely no warranty.
# License: Public Domain.
#
# Takes one or more strings one the command line and creates C code suitable 
# for insertion into a 1394 configuration rom.

import sys, re

def stripquotes (s):
    # if the string is quoted remove the quotation marks.
    if (s[0] == '\'' or s[0] == '\"') and s[0] == s[-1]:
        return s[1:-1]

def pad_to_quad (bytelen):
    # determine that need to be added to the string to pad it out to the 
    # nearest number of quads.

    if bytelen % 4 == 0:
        return 0
    return 4 - bytelen % 4

def str_to_quads (s):
    # break the byte string into array of quadlets.

    bytelen = len(s)
    padlen = pad_to_quad(len(s))
    quadlen = (bytelen + padlen) / 4

    quads = []
    i = 0
    for j in range(0, quadlen):
        q = 0
        for k in range(0, 4):
            if i >= bytelen:
                break
            q = q << 8
            q |= ord(s[i])
            i += 1
        quads.append(q)

    # the string is stored "big endian" so if the last quadlet is
    # "ragged" (has paddin): this ensures the printable characters
    # are in the most significant bytes and NULs are in the least significant
    # bytes.
    if padlen > 0:
        quads[-1] = quads[-1] << (8 * padlen)
        
    return quads

def crc16_byte (byte, crc):
    for i in range(0, 8):
        j = (byte ^ crc) & 1 
        crc = crc >> 1
        if j:
            crc = crc ^ 0xA001;
        crc = crc & 0xFFFF
    return crc

def crc16_quads (quads):
    j = 0
    crc = 0
    for q in quads:
        crc = crc16_byte(q >> 24 & 0xFF, crc)
        crc = crc16_byte(q >> 16 & 0xFF, crc)
        crc = crc16_byte(q >> 8 & 0xFF, crc)
        crc = crc16_byte(q & 0xFF, crc)
    return crc
        
def textleaf (s):
    # needed as win32 passes quotation marks along with the command line
    # arguments.
    s = stripquotes(s)

    quads = str_to_quads(s)

    # insert minimal ascii encoding headers
    quads.insert(0, 0)
    quads.insert(0, 0)

    crc16 = crc16_quads(quads)
    #print 'CRC16=%X' % (crc16)

    print ''
    print '/* text leaf for string: "%s" */' % (s)
    print '0x%04X%04X,' % (len(quads), crc16)
    for q in quads:
        print '0x%08X,' % (q)
    print ''

if __name__ == '__main__':
    argcount = len(sys.argv)
    if argcount < 2:
        print 'Requires one or more strings as arguments.'
        sys.exit(1)

    for arg in sys.argv[1:]:
        if len(arg) > 0:
            textleaf(arg)

    def crc16 (s):
        crc = 0
        for b in range(0, len(s)):
            print '%X' % (ord(s[b]))
            crc = (crc ^ ord(s[b])) << 8
            for i in range(0, 7):
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc = crc << 1
                crc = crc & 0xFFFF
            print '%X' % (crc)
        return crc
    print 'CRC=%X' % (crc16("abcd"))

    sys.exit(0)

