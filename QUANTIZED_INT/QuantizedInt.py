
# An integer between 'minval' and 'maxval' (inclusive) with discrete possible values as determined
# by 'increment'.
class QuantizedInt(object):

    def __init__(self, minval, maxval, increment=1):
        if minval > maxval:
            raise AssertionError("'minval' (%d) cannot be > 'maxval' (%d)"%(minval, maxval))

        if minval == maxval:
            increment = 1

        if increment <= 0:
            raise AssertionError("specified 'increment' (%d) is invalid for range: [%d, %d]"%(increment, minval, maxval))

        if ((maxval - minval) % increment):
            raise AssertionError("specified 'increment' (%d) does not lead to equal discrete values in range: [%d, %d]"%(increment, minval, maxval))
        
        self.minval = minval
        self.maxval = maxval
        self.increment = increment

    def inRange(self, index):
        if (index >= 0) and (index < len(self)):
            return True
        return False


    def getVal(self, index):
        return self.getVals[index]  

    def getVals(self):
        l = []
        i = self.minval
        while i <= self.maxval:
            l.append(i)
            i += self.increment
        return l

    def __iter__(self):
        return iter(self.getVals())

    def __len__(self):
        return len(self.getVals())

    def __str__(self):
        return str(self.getVals())
    




