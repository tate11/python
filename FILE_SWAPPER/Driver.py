#!/usr/bin/python

import os
import optparse
import Settings
import FilePathWrapper
import FileSystemWrapper
import Producer
import Consumer
import Utils
#from sh import mount


# THIS WILL ONLY WORK WITH LINUX (TESTED ON UBUNTU)
# python Driver.py --i1=/home/alii2/poo/fs/test/test.pdf --i2=/home/alii2/poo/fs2/test/foop.pdf -s /tmp/sprott/

#################################################################################################################
# COMMAND LINE ARGUMENT CHECKS

minswapsize = Settings.minswapsize
maxswapsize = Settings.maxswapsize
minblocksize = 4096 # bytes

# Assert 'Settings.py' globals:
try:
    assert(minswapsize > 0)
    assert(maxswapsize > minswapsize)
    assert(Settings.gBS >= minblocksize)
except AssertionError:
    print "Error: revise your global values in: 'Settings.py'"
    exit(-1)

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("--i1", help="input file 1 (required)", dest="input1",  metavar="<infile1>")
    parser.add_option("--i2", help="input file 2 (required)", dest="input2",  metavar="<infile2>")
    parser.add_option("-s", help="swap directory (required)", dest="swapdir",  metavar="<swapdir>")
    parser.add_option("-n", help="maximum swap usage (in MB; default=%d)"%(minswapsize), dest="swapsize", metavar="<int>", default=minswapsize)
    parser.add_option("-v", help="verbose", action="store_true", dest="verbose",  default=False)
    (opts, args) = parser.parse_args()

#if os.geteuid() != 0:
#    print "Error: please run as root\n"
#    parser.print_help()
#    exit(-1)    

if opts.input1 is None:
    print "Error: input file 1 has not been specified\n"
    parser.print_help()
    exit(-1)

if opts.input2 is None:
    print "Error: input file 2 has not been specified\n"
    parser.print_help()
    exit(-1)

if opts.swapdir is None:
    print "Error: swap directory has not been specified\n"
    parser.print_help()
    exit(-1)

fw1 = FilePathWrapper.FilePathWrapper(opts.input1)
fw2 = FilePathWrapper.FilePathWrapper(opts.input2)
fw3 = FilePathWrapper.FilePathWrapper(opts.swapdir)

if not fw1.isExistingFile():
    print "Error: could not find input file 1: %s\n"%(opts.input1)
    parser.print_help()
    exit(-1)

if not fw2.isExistingFile():
    print "Error: could not find input file 2: %s\n"%(opts.input2)
    parser.print_help()
    exit(-1)

if fw1.getBasename() == fw2.getBasename():
    print "Error: input files cannot be identically names: %s\n"%(fw1.getBasename())
    parser.print_help()
    exit(-1)

if not fw3.isExistingDir():
    print "Error: swap directory does not exist: %s\n"%(opts.swapdir)
    parser.print_help()
    exit(-1)

try:
    swapsize = int(opts.swapsize)
except ValueError:
    print "Error: invalid max swap usage specified: %s\n"%(opts.swapsize)
    parser.print_help()
    exit(-1)    

if (swapsize < minswapsize) or (swapsize > maxswapsize):
    print "Error: invalid max swap usage specified (must be between %d and %d): %d\n"%(minswapsize, maxswapsize, swapsize)
    parser.print_help()
    exit(-1)

#################################################################################################################
# LOGICAL CHECKS

# Get filesystem wrappers:
fswrap1 = FileSystemWrapper.FileSystemWrapper(str(fw1))
fswrap2 = FileSystemWrapper.FileSystemWrapper(str(fw2))
fswrap3 = FileSystemWrapper.FileSystemWrapper(str(fw3))

# Get input file sizes (in bytes):
f1_size = fswrap1.myfilesize #os.path.getsize(str(fw1))
f2_size = fswrap2.myfilesize #os.path.getsize(str(fw2))

# Diagnostic:
#print(str(fswrap1))
#print(str(fswrap2))
#print(str(fswrap3))

# Assert that swap space filesystem actually has the available space:
if not fswrap3.hasFree(Utils.MBtoBytes(swapsize)):
    print "Error: swap space buffer too small: %s"%(str(fw3))
    parser.print_help()
    exit(-1)

# Assert that input files can fit onto their intended target filesystems.
# Eg. a 5GB file on a 120GB filesystem will NOT swap with a 1GB file on a
# 4GB filesystem.                                                             <---- TEST THIS
# Similarly, a 6GB file on a 120GB filesystem will NOT swap with a 4GB file
# on a 10GB filesystem with only 1GB free space.                              <---- TEST THIS
if (f2_size + fswrap2.fsfree) < f1_size: 
    print "Error: '%s' is too large to swap with: %s"%(str(fw1), str(fw2))
    parser.print_help()
    exit(-1)
if (f1_size + fswrap1.fsfree) < f2_size: 
    print "Error: '%s' is too large to swap with: %s"%(str(fw2), str(fw1))
    parser.print_help()
    exit(-1)

# Diagnostic:
#print(str(fswrap1))
#print("FS *new* free space (bytes): %d"%((fswrap1.fsfree + f1_size) - f2_size))
#print ""
#print(str(fswrap2))
#print("FS *new* free space (bytes): %d"%((fswrap2.fsfree + f2_size) - f1_size))

#################################################################################################################
# ATTEMPT TO CREATE OUR RAMFS MOUNT POINT (MIGRATE TO WRAPPER SHELL SCRIPT)

#mount("
#mount("ramfs", "/tmp/sprott", "-t ramfs", "-o size=20M")
#mount -t ramfs -o size=20m ramfs /mnt/ram

#################################################################################################################
# ALL TESTS HAVE PASSED NOW COMMENCE SWAP ALGORITHM

producer = Producer.ProducerManager([fw1, fw2], str(fw3), swapsize)
consumer = Consumer.ConsumerManager(producer.getConsumerArgs())

while producer.hasWork():
    try: 
        producer.run()    
        consumer.run()
    except:
        print "Fatal error! Terminating..."
        exit(-1)





















# Copying a chunk from the END of a binary file:
# $ dd if=test.pdf of=chunk.bin bs=1 skip=13750000
#
# Truncating a binary file to a new size:
# $ truncate -s 13750000 test.pdf            <--- will attempt to resize test.pdf to 13750000 (by growing or shrinking, whichever is appropriate)
#                                            <--- shrinks natively happen in place (ie no copying required), grows require a copy (even tho the end result
#                                                 appears to be an in-place modificatioN)
#                                            <--- works for ext4, other fs's not so sure
#
# Concatenation/join multiple binary files
# $ cat file1.bin file2.bin > newfile.bin
# The new file will look like:
# <contents of file1.bin>
# <contents of file2.bin>



# Some guiding notes:
# Suppose I have a file  that's 3253721 bytes:
# $ ls -la *.pdf
# ...
# -rw-rw-r-- 1 alii2 alii2 3253721 Feb 15 13:43 test.pdf
#
# Then you CAN do something like this: 
#$ dd if=test.pdf of=funk.bin skip=3250000 bs=1 count=4096
#3721+0 records in
#3721+0 records out
#3721 bytes (3.7 kB) copied, 0.00353906 s, 1.1 MB/s
#$ ls -latr funk.bin 
#-rw-rw-r-- 1 alii2 alii2 3721 Mar 21 11:05 funk.bin           <--- you wanted to copy 4096 bytes, but only 3721 bytes were available, 'dd' handled this!
#



#free = (st1.f_bavail * st1.f_frsize)
#total = (st1.f_blocks * st1.f_frsize)
#used = (st1.f_blocks - st1.f_bfree) * st1.f_frsize

#percent = usage_percent(used, total, _round=1)

