import os

# Useful class wrapper over string filesystem paths (for Linux-based systems) to do things that 
# the standard modules wont let you do.
# SAFETY IS GUARANTEED SO LONG AS THE NAMES CONTAINED IN PATHS AREN'T TOO STUPID (ie. contain funky characters, strange whitespaces, etc.)
class FilePathWrapper(object):

    raw = ""

    # IN: path to file/dir (can be relative, absolute, etc.)
    def __init__(self, raw):
        self.raw = raw

    def __str__(self):
        return self.getPath() 

    # Does the file exist
    def isExistingFile(self):
        return os.path.isfile(self.raw)

    # Does the dir exist
    def isExistingDir(self):
        return os.path.isdir(self.raw)

    # Does the file/dir exist
    def exists(self):
        return ( self.isExistingFile() or self.isExistingDir() )

    ##############################################################################################
    # Common operations on dirs && files:

    # Returns the path
    #
    # Example:
    # IN: /some/where/overtherainbow.foo
    # OUT: /some/where/overtherainbow.foo
    #
    # IN: /some/where/overtherainbow/
    # OUT: /some/where/overtherainbow
    #
    def getPath(self):
        s = self.raw
        if s.endswith('/'):
            s = s[0:(len(s) - 1)]
        return s

    # Returns the leading path of dir or file
    #
    # Example:
    # IN: /some/where/overtherainbow.foo
    # OUT: /some/where
    #
    # Example:
    # IN: /some/where/overtherainbow/
    # OUT: /some/where
    #
    def getLeadingPath(self):
        s = self.getPath()
        s = (os.path.split(s))[0]
        return s

    # Returns the leading path of dir or file
    # as a FilePathWrapper object instance.
    #
    # Example:
    # IN: /some/where/overtherainbow.foo
    # OUT: /some/where          <--- return this new FilePathWrapper
    #
    # Example:
    # IN: /some/where/overtherainbow/
    # OUT: /some/where          <--- return this new FilePathWrapper
    #
    def getLeadingPathAsWrapper(self):
        return FilePathWrapper(self.getLeadingPath())

    # Returns the leading path as a list of elements
    #
    # Example:
    # IN: /some/where/overtherainbow.foo
    # OUT: ['/', 'some', 'where']
    #
    # Example:
    # IN: some/where/overtherainbow.foo
    # OUT: ['some', 'where']
    #
    def getLeadingPathAsList(self):
        s = self.getLeadingPath()
        l = s.split('/')
        l = filter(None, l)
        if s.startswith('/'):
            l.insert(0, '/')
        return l

    # Returns the basename (ie. the dir or file name without any leading path)
    #
    # Example:
    # IN: /some/where/overtherainbow.foo
    # OUT: overtherainbow.foo
    #
    # IN: /some/where/overtherainbow/
    # OUT: overtherainbow
    #
    def getBasename(self):     
        s = self.raw
        if s.endswith('/'):
            s = s[0:(len(s) - 1)]
        return (os.path.split(s))[1]

    # DEPRECATED! Use getExtended() instead
    #
    # Returns a FilePathWrapper object instance existing below the current.
    #
    # Example:
    # CURRENT: /some/where               <--- this FilePathWrapper
    # IN: /over/the/rainbow              <--- pass in this string
    # OUT: /some/where/over/the/rainbow  <--- return this new FilePathWrapper
    def getSubWrapper(self, subpath):
        print "FilePathWrapper.py:getSubWrapper() has been deprecated! Use getExtended() instead."
        return self.getExtended(subpath)
        #return FilePathWrapper(self.getPath() + subpath)


    # Extends THIS FilePathWrapper object instance.
    #
    # Example:
    # CURRENT: /some/where               <--- this FilePathWrapper
    # IN: /over/the/rainbow              <--- pass in this string
    # OUT: /some/where/over/the/rainbow  <--- return this new FilePathWrapper
    def getExtended(self, extension):
        s = extension
        if not s.startswith("/"):
            s = "/" + s
        return FilePathWrapper(self.getPath() + s)

    ##############################################################################################
    # Useful operations specifically for dirs:

    # Return a list of FilePathWrapper objects of the contents of an existing directory:
    def getSortedDirContents(self, excludeDirs=False):
        l = []
        if self.isExistingDir():
            sortedDirContents = sorted(os.listdir(self.raw))
            l = [FilePathWrapper(self.getPath() + '/' + member) for member in sortedDirContents]
            if excludeDirs:
                for fw in l:
                    if fw.isExistingDir():
                        l.remove(fw)
        return l

    # Make a directory if it does not exist (including all the parent directories leading down to it)
    # Returns:
    # True - if successful or directory already exists.
    # False - if unsuccessful.
    def createDir(self):
        if not self.isExistingDir():
            leadingPath = self.getLeadingPathAsWrapper() # FilePathWrapper(self.getLeadingPath())
            if (leadingPath.getPath() == '/') or (len(leadingPath.getPath()) == 0):
                try:
                    os.mkdir(self.getPath())    
                except OSError as e:
                    #print "Error: could not create directory: %s"%(self.getPath())
                    #print str(e)
                    return False
            elif not leadingPath.exists():
                if not leadingPath.createDir():
                    return False
            try:
                os.mkdir(self.getPath())   
            except OSError as e:
                #print "Error: could not create directory: %s"%(self.getPath())
                #print str(e)
                return False             
        return True
            

    # Return a list of FilePathWrapper objects over files with a target extension, and located
    # below an input, existing directory:
    def searchFiles(self, targetExtension):
        l = []
        if self.isExistingDir():
            sortedDirContents = sorted(os.listdir(self.raw))
            for member in sortedDirContents:
                wrapped_member = FilePathWrapper(self.getPath() + '/' + member)
                if wrapped_member.isExistingDir():
                    l = l + wrapped_member.searchFiles(targetExtension)
                elif wrapped_member.isExistingFile():
                    if wrapped_member.getExtension(False) == targetExtension:
                        l.append(wrapped_member)
        return l

    ##############################################################################################
    # Common operations specifically for files:

    # Has a file extension(s)?
    def hasExtension(self):
        if len(self.getExtension()) > 0:
             return True
        return False

    # Returns the basename (ie. the file name without any leading path) with NO extensions
    # Example:
    # IN: /some/where/overtherainbow.foo
    # OUT: overtherainbow
    #
    # Otherwise use 'n' to specify the number of extensions to omit.
    #
    def getBasenameWoutExt(self, n=None):
        basename = self.getBasename().split('.')[0]
        if n is None:        
            return basename
        elif n > 0:          
            exts = self.getExtensions()
            exts = exts[:-n or None]
            for ext in exts:
                basename = basename + ext
            return basename
        return self.getBasename()

    # Returns the file extension (if there are multiple, return the last only) 
    # Example:
    # IN: foobar.poo.wee.txt
    # OUT: .txt
    def getExtension(self, withDot=True):
        extension = os.path.splitext(self.raw)[1]
        if not withDot:
            extension = extension[1:]
        return extension

    # Returns a list of extensions (useful if filename has multiple extensions)
    # Example:
    # IN: foobar.poo.wee.txt
    # OUT: [.poo, .wee, .txt]
    def getExtensions(self, withDot=True):
        basename = self.getBasename()
        extensions = basename.split('.')[1:]
        if withDot:
            extensions = ['.' + x for x in extensions]
        return extensions


    # Creates empty file if it does not exist (ie. 'touch' command).
    # NOTE: the directory containing the empty file should already exist.
    # Returns:
    # True - if successful or file already exists.
    # False - if unsuccessful.
    def touch(self):
        if not self.isExistingFile():
            try:
                f = open(self.getPath(), 'a')
                f.close()
            except IOError:
                return False
        return True
    
