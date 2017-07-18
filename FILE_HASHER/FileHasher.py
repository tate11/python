import hashlib

# http://pythoncentral.io/hashing-files-with-python/

class FileHasher(object):

    def __init__(self, algorithm, blocksize=65536):
        func = getattr(hashlib, algorithm)  # Gets hashlib.algorithm
        self.hasher = func()
        self.blocksize = blocksize

    def addFile(self, l): 
        for next in l:
            with open(next, 'rb') as f:
                buf = f.read(self.blocksize)
                while len(buf) > 0:
                    self.hasher.update(buf)
                    buf = f.read(self.blocksize)           

    def addStr(self, s):
        self.hasher.update(s) 

    def getHash(self):
        return self.hasher.hexdigest()






