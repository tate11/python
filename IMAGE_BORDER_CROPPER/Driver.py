#!/usr/bin/python

import os
import sys
import optparse
import bordercrop
import pyPdf
import PythonMagick


def isRatioValid(r):
    if (r < 0.5) or (r >= 0): 
        return True
    return False

def printHelpAndExit():
    parser.print_help()
    exit(-1)

#################################################################################################################

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("--h1", help="horizontal cropping ratio 1 (from leftside) (default=0.1)", dest="h1",  metavar="<float>")
    parser.add_option("--h2", help="horizontal cropping ratio 2 (from rightside) (optional, defaults to 'h1')", dest="h2",  metavar="<float>")
    parser.add_option("--v1", help="vertical cropping ratio 1 (from top) (default=0.1)", dest="v1",  metavar="<float>")
    parser.add_option("--v2", help="vertical cropping ratio 2 (from bottom) (optional, defaults to 'v1')", dest="v2",  metavar="<float>")
    parser.add_option("-i", help="input .png file OR .pdf file (required)", dest="inputfile",  metavar="<filename>")
    parser.add_option("-o", help="output .png file (optional; shows a preview if not specified)", dest="outputfile",  metavar="<filename>")
    parser.add_option("-d", help=".pdf conversion density (default=300)", dest="pdfdensity",  metavar="<int>", default=300)
    parser.add_option("-v", help="verbose", action="store_true", dest="verbose",  default=False)
    parser.add_option("-x", help="don't ask (just do)", action="store_true", dest="dontask",  default=False)
    (opts, args) = parser.parse_args()

if (opts.inputfile is None):
    print "Error: please specify input file\n"
    printHelpAndExit()

if (not os.path.exists(opts.inputfile)):
    print "Error: input file does not exist: %s"%(opts.inputfile)
    printHelpAndExit()

if (opts.outputfile is not None):
    if (os.path.exists(opts.outputfile)):
        print "Error: output file already exists: %s"%(opts.outputfile)
        printHelpAndExit()

if (opts.h1 is not None):
    h1 = float(opts.h1)
    if (isRatioValid(h1) is False):
        print "Error: invalid --h1 value specified (should be between 0.0 and 0.5)\n"
        printHelpAndExit()
else:
    h1 = 0.1

if (opts.h2 is not None):
    h2 = float(opts.h2)
    if (isRatioValid(h2) is False):
        print "Error: invalid --h2 value specified (should be between 0.0 and 0.5)\n"
        printHelpAndExit()
else:
    h2 = h1

if (opts.v1 is not None):
    v1 = float(opts.v1)
    if (isRatioValid(v1) is False):
        print "Error: invalid --v1 value specified (should be between 0.0 and 0.5)\n"
        printHelpAndExit()
else:
    v1 = 0.1

if (opts.v2 is not None):
    v2 = float(opts.v2)
    if (isRatioValid(v2) is False):
        print "Error: invalid --v2 value specified (should be between 0.0 and 0.5)\n"
        printHelpAndExit()
else:
    v2 = v1

print ""
print "Input file: %s"%(opts.inputfile)
print "Output file: %s"%(opts.outputfile)
print "h1: %f"%(h1)
print "h2: %f"%(h2)
print "v1: %f"%(v1)
print "v2: %f"%(v2)

if (opts.dontask is False):   
    print ""
    response = raw_input("Is this correct? (y/n): ")
    if (not response.upper() == 'Y'):
        print ""
        print "Exiting!"
        exit(0)
    
print ""
print "Starting..."

if (opts.inputfile.endswith(".pdf")):
    myPdf = pyPdf.PdfFileReader(file(opts.inputfile, "rb"))
    num_pages = myPdf.getNumPages()
    for i in range(num_pages):
        im = PythonMagick.Image()
        im.density('%d'%(opts.pdfdensity))
        im.read(opts.inputfile + '[' + str(i) +']')  
        outfile = 'file_out-' + str(i)+ '.png'
        im.write(outfile)
        bordercrop.DoWork(outfile, None, h1, h2, v1, v2, opts.verbose)
    exit(0)
    # shell comamnd: $ convert -density 600 -depth 1 -quality 100 test.pdf test.png

bordercrop.DoWork(opts.inputfile, opts.outputfile, h1, h2, v1, v2, opts.verbose)
