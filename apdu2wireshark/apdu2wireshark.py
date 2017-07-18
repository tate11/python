#!/usr/bin/env python

import os
import sys
import optparse
import socket
import binascii

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-i", help="input file (required)", dest="inputfile", metavar="<filename>")
    (opts, args) = parser.parse_args()

if opts.inputfile is None:
    print "Error: input file not provided\n"
    parser.print_help()
    exit(-1)

lines = []

try:
    with open(opts.inputfile, 'r') as f:
        lines = map(str.rstrip, f.readlines())
        f.close()
except:
    print "Error opening file: %s"%(opts.inputfile)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 4729)

for line in lines:
    header = "02040400000000000000000000000000"
    try:
        blob = binascii.unhexlify(header + line)
    except:
        print "Error binary conversion of: %s"%(line)

    try:
        sent = sock.sendto(blob, server_address)
    except:
        print "Error: network"
        break

sock.close()


