#!/usr/bin/python

import FilePathWrapper

testdirs = ["test/foo_dir1", "test/foo_dir1/", "test/foo_dir2/"]
testfiles = ["test/foo_file1.txt", "test/foo_file2", "test/foo_file3.txt.org"]
testdoesnotexist = ["test/invalid"]

for testdir in testdirs:
    wrapper = FilePathWrapper.FilePathWrapper(testdir)
    print "INPUT: " + wrapper.raw
    if wrapper.exists():
        print wrapper.getPath()
        print wrapper.getLeadingPath()
        print wrapper.getLeadingPathAsList()
        print wrapper.getBasename()        
        sortedDirContents = wrapper.getSortedDirContents()
        for member in sortedDirContents:
            print member.getPath()
    else:
        print "Error: could not find: %s"%(wrapper.raw)
    print "------------------"


for testfile in testfiles:
    wrapper = FilePathWrapper.FilePathWrapper(testfile)
    print "INPUT: " + wrapper.raw
    if wrapper.exists():
        print wrapper.getPath()
        print wrapper.getLeadingPath()
        print wrapper.getLeadingPathAsList()
        print wrapper.getBasename()
        print wrapper.hasExtension()
        print wrapper.getBasenameWoutExt()
        print wrapper.getBasenameWoutExt(1)
        print wrapper.getExtension()
        print wrapper.getExtension(False)
        print wrapper.getExtensions()
        print wrapper.getExtensions(False)
    else:
        print "Error: could not find: %s"%(wrapper.raw)
    print "------------------"

for testinvalid in testdoesnotexist:
    wrapper = FilePathWrapper.FilePathWrapper(testinvalid)
    print "INPUT: " + wrapper.raw
    if wrapper.exists():
        print "Error: found: %s"%(wrapper.raw)
    print "------------------"
