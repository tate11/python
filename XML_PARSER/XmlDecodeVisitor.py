import XmlContainer
import Settings

class XmlRowColVisitor(XmlContainer.XmlNodeVisitor):

    def __init__(self, args):
        # Invoke the super (XmlContainer.XmlNodeVisitor) class constructor:
        super(XmlRowColVisitor, self).__init__() # ([Settings.row_tag, Settings.col_tag, Settings.qr_tag, Settings.result_tag], True)  
        self.qrCount = args[0]

    def previsit(self, node):
        if (node.getTag() == Settings.row_tag) or (node.getTag() == Settings.col_tag):
            self.map = []
        elif node.getTag() == Settings.qr_tag:
            index = int(node.getVal())
            while len(self.map) < index:
                self.map.append(0) 
        elif node.getTag() == Settings.result_tag:
            self.map.append(int(node.getVal()))

    def postvisit(self, node):
        if (node.getTag() == Settings.row_tag) or (node.getTag() == Settings.col_tag):
            while len(self.map) < self.qrCount:
                self.map.append(0)

    def getEmptyMap(self, count):
        return [0] * count
            


class XmlMatrixVisitor(XmlContainer.XmlNodeVisitor):

    # args : [rowcolCount, qrCount, qrFinalCount]
    def __init__(self, args):
        # Invoke the super (XmlContainer.XmlNodeVisitor) class constructor:
        super(XmlMatrixVisitor, self).__init__() #  ([Settings.matrix_tag, Settings.row_tag, Settings.col_tag], True)
        self.rowcolCount = args[0]
        self.qrCount = args[1]
        self.qrFinalCount = args[2]

    def previsit(self, node):        
        if node.getTag() == Settings.matrix_tag:
            self.map = []
        elif (node.getTag() == Settings.row_tag) or (node.getTag() == Settings.col_tag):
            index = int(node.getVal())
            while len(self.map) < index:
                self.map.append([0] * self.qrCount) 

            if index == (self.rowcolCount - 1):
                qrCount = self.qrFinalCount
            else:
                qrCount = self.qrCount

            self.xmlrowcolvisitor = XmlRowColVisitor([qrCount])
            self.xmlrowcolvisitor.visit(node)
              
            self.map.append(self.xmlrowcolvisitor.map)

    def postvisit(self, node):
        if node.getTag() == Settings.matrix_tag:

            while len(self.map) < self.rowcolCount:
                if len(self.map) == (self.rowcolCount - 1):
                    qrCount = self.qrFinalCount
                else:
                    qrCount = self.qrCount
                self.map.append([0] * qrCount)

            
    def getEmptyMap(self, qrCount, qrFinalCount):
        l = []
        i = 0
        while i < self.rowcolCount:
            if i == self.rowcolCount - 1:
                count = qrFinalCount
            else:
                count = qrCount
            l.append(self.xmlrowcolvisitor.getEmptyMap(count))
            i += 1
        return l

    #def isDecoded(self, node):
    #    myDecodeMap = self.DecodeMap()
    #    self.travel(node, myDecodeMap)
    #    self.lastdecodemap = myDecodeMap.decodemap
        #print self.lastdecodemap
   #     return myDecodeMap.isDecoded()

    #def getLastDecodeMap(self):
     #   return self.lastdecodemap
        

# This visitor can traverse the following nodes:
#
# <set>           <--- this one
#     <matrix/>
#     <matrix/>
#     ... etc.
# </set>
#
# <merged>        <--- or this one
#     <matrix/>
#     <matrix/>
#     ... etc.
# </merged>
#
class XmlSetVisitor(XmlContainer.XmlNodeVisitor):

    # args : [matrixCount, rowcolCount, qrCount, qrFinalCount]
    # qrFinalCount is the expected number of QR codes in the last row/col of the last matrix in the set
    def __init__(self, args):
        # Invoke the super (XmlContainer.XmlNodeVisitor) class constructor:
        super(XmlSetVisitor, self).__init__() #([Settings.set_tag, Settings.merged_tag, Settings.matrix_tag], True)  
        self.matrixCount = args[0]
        self.rowcolCount = args[1]
        self.qrCount = args[2]
        self.qrFinalCount = args[3]



    def previsit(self, node):
        if (node.getTag() == Settings.set_tag) or (node.getTag() == Settings.merged_tag):
            self.map = []
        elif node.getTag() == Settings.matrix_tag:
            index = int(node.getVal())
            while len(self.map) < index:
                self.map.append([[0] * self.qrCount] * self.rowcolCount) 

            if index == (self.matrixCount - 1):
                qrFinalCount = self.qrFinalCount
            else:
                qrFinalCount = self.qrCount

            self.xmlmatrixvisitor = XmlMatrixVisitor([self.rowcolCount, self.qrCount, qrFinalCount])
            self.xmlmatrixvisitor.visit(node)
            self.map.append(self.xmlmatrixvisitor.map)

    def postvisit(self, node):
        if (node.getTag() == Settings.set_tag) or (node.getTag() == Settings.merged_tag):
            while len(self.map) < self.matrixCount:    
                if len(self.map) == (self.matrixCount - 1):
                    qrFinalCount = self.qrFinalCount
                else:
                    qrFinalCount = self.qrCount
                self.map.append(self.xmlmatrixvisitor.getEmptyMap(self.qrCount, qrFinalCount)) 


    def getEmptyMap(self):
        l = []
        i = 0
        while i < self.matrixCount:
            if i == (self.matrixCount - 1):
                qrFinalCount = self.qrFinalCount
            else:
                qrFinalCount = self.qrCount

            l.append(self.xmlmatrixvisitor.getEmptyMap(self.qrCount, qrFinalCount))
            i += 1
        return l


    def flatten(self, x):
        """flatten(sequence) -> list

        Returns a single, flat list which contains all elements retrieved
        from the sequence and all recursively contained sub-sequences
        (iterables).

        Examples:
        >>> [1, 2, [3,4], (5,6)]
        [1, 2, [3, 4], (5, 6)]
        >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, MyVector(8,9,10)])
        [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]"""

        result = []
        for el in x:
            #if isinstance(el, (list, tuple)):
            if hasattr(el, "__iter__") and not isinstance(el, basestring):
                result.extend(self.flatten(el))
            else:
                result.append(el)
        return result

    #def decode(self, node):
    #    self.visit(node)
    #    l = self.flatten(self.map)
    #    print l

    def getMapIter(self, node):
        self.visit(node)
       # return iter(self.flatten(self.map))
        return iter(self.map)

