#!/usr/bin/python

import QuantizedInt

i1 = 1
i2 = 11


# Failure example:
inc = 3
try:
    quantizedint = QuantizedInt.QuantizedInt(i1, i2, inc)
except AssertionError as e:
    print "Could not quantize over: [1, 11, 3]"

# Success example:
inc = 2
try:
    quantizedint = QuantizedInt.QuantizedInt(i1, i2, inc)
except AssertionError as e:
    print str(e)
    exit(-1)

print "Quantized int set: %s"%(quantizedint)
print "Number of discrete values in set: %d"%(len(quantizedint))
for i in quantizedint:
    print str(i)

#print "@ Index -2: %s (%d)"%(quantizedint.inRange(-2), quantizedint.getVal(-2))
#print "@ Index 0: %s (%d)"%(quantizedint.inRange(0), quantizedint.getVal(0))
#print "@ Index 3: %s (%d)"%(quantizedint.inRange(3), quantizedint.getVal(3))
#print "@ Index 5: %s (%d)"%(quantizedint.inRange(5), quantizedint.getVal(5))
#print "@ Index 20: %s (%d)"%(quantizedint.inRange(20), quantizedint.getVal(20))
