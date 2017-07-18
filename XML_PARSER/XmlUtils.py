import xml.etree.ElementTree as ElementTree
import Settings

def getAttribFindStr(attrib):
    s = ""
    for a in attrib:
        s += "[@%s='%s']"%(a, attrib[a])
    return s

# class xml.etree.ElementTree.Element(tag, attrib={}, **extra)  
# NOTE: we don't support "**extra""
# WARNING: ensure your 'attrib' dictionary contains STRING to STRING key-val pairs only!
def getOrAddChild(e, tag, attrib=None):
    if attrib is None:
        attrib = {} 
    c = e.find("%s%s"%(tag, getAttribFindStr(attrib)))
    if c is None:
        c = ElementTree.Element(tag, attrib)
        e.append(c)
    return c



def getIndentStr(indentwidth, indentcount):
    s1 = ""
    s2 = ""
    i = 0     
    while i < indentwidth:
        s1 += " "
        i += 1
    i = 0 
    while i < indentcount:
        s2 += s1
        i += 1
    return s2


def strformat1(e, indentwidth=2, indentcount=0):
    s = ""
    s += getIndentStr(indentwidth, indentcount) + "<%s"%(e.tag)
    for attr in e.items():
        s += " %s='%s'"%(attr[0], attr[1])
    if len(e) > 0:
        s += ">\n"
        for c in e:
            s += strformat1(c, indentwidth, (indentcount + 1))
        s += getIndentStr(indentwidth, indentcount) + "</%s>\n"%(e.tag)    

    else:

        if (e.text is not None) and (len(e.text.strip()) > 0):
       # if e.text is not None:
       # if len(e.text) > 0: 
            s += ">%s</%s>\n"%(e.text, e.tag)
        else:
            s += " />\n"
 
    return s


# Dumps valid .xml
def dump(e, indentwidth=2):
    return strformat1(e, indentwidth, 0)



# IN: <merged_session>, <session>, <set>, <matrix>, <row>, <col>, <QR>
# Inspects below the elements listed above to see if its <QR> leaves
# all have the attribute 'result' set to '1'.
def isDecoded(e):
    if len(e) == 0:
        return False
    it = e.iter()
    while True:
        try:
            next_e = it.next()
            if next_e.tag == Settings.qr_tag:
                if next_e.get(Settings.result_attrib) is None:
                    return False
                if not int(next_e.get(Settings.result_attrib)):
                    return False
                
        except StopIteration:
            break
    return True
