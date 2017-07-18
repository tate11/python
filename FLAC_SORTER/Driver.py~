#!/usr/bin/python

import os
import optparse
import FilePathWrapper
#
# In Ubuntu 14.04, python 2.7.6:
# apt-get install python-tagpy
import tagpy
#
# Pretty Print : used for dumping dictionaries
from pprint import pprint

#################################################################################################################

# Command line arg wrapper (performs sanitization of input args)

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-i", help="input directory (required)", dest="inputdir",  metavar="<inputdir>")
    parser.add_option("-o", help="output directory (optional)", dest="outputdir",  metavar="<outputdir>")
    parser.add_option("-v", help="verbose", action="store_true", dest="verbose",  default=False)
    (opts, args) = parser.parse_args()

inputdir = opts.inputdir
verbose = opts.verbose
outputdir = opts.outputdir

if opts.inputdir is None:
    print "Error: no input directory has been specified\n"
    parser.print_help()
    exit(-1)

outwrapper = None
if not opts.outputdir is None:
    outwrapper = FilePathWrapper.FilePathWrapper(opts.outputdir)
    if not outwrapper.isExistingDir:
        print "Error: output directory does not exist: %s\n"%(opts.outputdir)
        parser.print_help()
        exit(-1)


wrapper = FilePathWrapper.FilePathWrapper(opts.inputdir)
l = wrapper.searchFiles("flac")
albums = {}
artists = {}
for f in l:
    flac = tagpy.FileRef(f.getPath())
#    print flac.tag().artist
#    print flac.tag().album
#    print flac.tag().title
#    print flac.tag().track
#    print ""
    
    # This is our "valid .flac" test:
    album = flac.tag().album
    if len(album) > 0:       
        albums.setdefault(album, []).append(f)

    # This is our "valid .flac" test:
    artist = flac.tag().artist
    if len(artist) > 0:       
        artists.setdefault(artist, []).append(f)


print "-------------------------"
print "ALBUM"
print " <tracks>"
print ""
for album in albums:
    print album
    l = albums[album]
    for f in l:
        flac = tagpy.FileRef(f.getPath())
        print " " + flac.tag().title
    print ""

print "-------------------------"
print "ARTIST"
print " <albums>"
print ""
for artist in artists:
    print artist
    l = artists[artist]
    for f in l:
        flac = tagpy.FileRef(f.getPath())
        print " " + flac.tag().album
    print ""


    
#pprint(albums)

if not outwrapper is None: 
    print "do some stuff"

# for each album:
#    mkdir out/<artist>/<album name>  <--- artist may already exist! 
#    copy 
# for album in albums:
#    l = albums[album]
#    for f in l:
#        flac = tagpy.FileRef(f.getPath())
#        artist = flac.tag().artist
#        if not exist("out/" + artist):
#            mkdir("out/" + artist)
#        if not exist("out/" + artist + "/" + album):
#            mkdir("out/" + artist + "/" + album)
#        copy(f -> album)
#        rename(f -> track name)
