import xml.etree.ElementTree


class SimpleXmlElement(xml.etree.ElementTree.Element):

    def __init__(self):
        super(SimpleXmlElement, self).__init__()
