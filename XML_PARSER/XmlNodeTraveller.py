import XmlContainer
import Settings

class XmlNodeTraveller(object):
    def __init__(self, xml):
        self.xml = xml

    def getIndex(self):
        return int(self.xml.getNodeVal(Settings.index_tag))

    def travel(self):
        if self.xml.getTag() == Settings.qr_tag:
            
            return int(self.xml.getVal())
        else:
            l = [] 
            # recursive magic
            for node in self.xml:
                if node.getTag() != Settings.index_tag:
                    l.append(XmlNodeTraveller(node).travel())

        return l
                #if node.getTag != Settings.index_tag:


    def supertravel(self, non_parent_tags, child_tag, child_val_type):
        if self.xml.getTag() == child_tag:
            
            return child_val_type(self.xml.getVal())
        else:
            l = [] 
            # recursive magic
            for node in self.xml:
                if node.getTag() not in non_parent_tags:
                    l.append(XmlNodeTraveller(node).supertravel(non_parent_tags, child_tag, child_val_type))

        return l
                #if node.getTag != Settings.index_tag:
                    



    def isDecoded(self):
        return bool(self.xml.getNode(Settings.decoded_tag).getVal())























