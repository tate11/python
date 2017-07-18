#!/usr/bin/env python

import os
import sys
import optparse

#   EXAMPLE USAGE:
#
#   $ cat animals.txt
#   lions
#   tigers
#   rats
#
#   $ python switchmaker.py -i animals.txt
#   case lions:
#       break;
#   case tigers:
#       break;
#   case rats:
#       break;
#   default:
#       break;

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-i", help="input file (required)", dest="inputfile",  metavar="<filename>")
    (opts, args) = parser.parse_args()

if opts.inputfile is None:
    print "Error: input file not provided\n"
    parser.print_help()
    exit(-1)

if not os.path.exists(opts.inputfile):
    print "Error: %s does not exist"%(opts.inputfile)
    exit(-1)


with open(opts.inputfile, 'r') as f:
    case_stmts = f.readlines()
    f.close()

    for case_stmt in case_stmts:
        print "case " + case_stmt.rstrip() + ":"
        print "    break;"
    print "default:"
    print "    break;"	
