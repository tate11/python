import XmlContainer
import Settings

class XmlDecodeVisitor(XmlContainer.XmlNodeVisitor):

    def __init__(self):
        self.decodemap = []
        self.qrindex = 0
        # Invoke the super (XmlContainer.XmlNodeVisitor) class constructor:
        super(XmlDecodeVisitor, self).__init__([Settings.index_tag], [None, self.post_visitor_action], self.decodemap)

    
    def append(self, i):
        if self.qrindex >= len(self.decodemap):
            self.decodemap.append(i)
        else:
            if (i == 1) and (self.decodemap[self.qrindex] == 0):
                self.decodemap[self.qrindex] = 1
        self.qrindex += 1

    def post_visitor_action(self, xmldecodevisitor, node): 
        #print node.getTag()
        if node.getTag() == Settings.matrix_tag:
            pass
        elif node.getTag() == Settings.row_tag:
            pass
        elif node.getTag() == Settings.qr_tag:
            xmldecodevisitor.append(int(node.getVal()))
        else:
            xmldecodevisitor.qrindex = 0
    












