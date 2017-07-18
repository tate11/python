import sys
import SimpleXmlTree
import XmlDecodeVisitor
import Settings
import numpy as np
import xml.etree.ElementTree
import lxml.etree as etree
#import SimpleXmlElement.SimpleXmlElement as SimpleXmlElement
import XmlUtils


# Performs deep (nested) replacement of elements, eg. replacing -1 with 0:            
    # 
    # IN:  [[1,0,0,1], [0,0,0,-1], [1,1,0,0]]
    # OUT: [[1,0,0,1], [0,0,0,0], [1,1,0,0]]
    #
def deepReplace(l, i1, i2):
    index = 0
    for e in l:
        if type(e) is list:
            deepReplace(e, i1, i2)
        elif type(e) is int:
            if e == i1:
                l[index] = i2  
        index += 1
    return l


def getDepth(g, count=0):
   #return lambda L: isinstance(L, list) and max(map(depth, L))+1
    return count if not isinstance(g,list) else max([getDepth(x,count+1) for x in g])

def flatten(x):
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
            result.extend(flatten(el))
        else:
            result.append(el)
    return result



#def visitor_action(xmlnodetk, node):
#    if xmlnodetk.isChild(node):
#        xmlnodetk.visitor_obj.append(int(node.getVal()))
        #print xmlnodetk.visitor_obj
   

#x = []
#xmlnodetk = XmlContainer.XmlNodeVisitor([Settings.index_tag], visitor_action, x)

class MyXmlTreeVisitor(SimpleXmlTree.XmlTreeVisitor):
    def __init__(self, visitortype, ignore_tags=None, inverse=False):
        # Invoke the super (SimpleXmlTree.XmlTreeVisitor) class constructor:
        super(MyXmlTreeVisitor, self).__init__(visitortype)#, ignore_tags=None, inverse=False)

    def previsit_breadthfirst(self, node):
        s = "PRE: %s"%(str(node))
        print s

    def previsit_depthfirst(self, node):
        s = "PRE: %s"%(str(node))
        print s

    def postvisit_depthfirst(self, node):
        s = "POST: %s"%(str(node))
        print s

   # def postvisit_singlevisitor(self, node):
   #     s = "POST: %s"%(str(node))
    #    print s


et = xml.etree.ElementTree.parse(sys.argv[1]) 
root = et.getroot()

print XmlUtils.dump(root, 4)

exit(0)

# Same output (valid .xml)
#xml.etree.ElementTree.dump(et)
#xml.etree.ElementTree.dump(root)

# This works (prints all the sets>
#for x in root.findall('project/src/set'):
#    print "XXXXXXXXXX"
#    xml.etree.ElementTree.dump(x)

# This works (dumps all the children)
#for n in root:
#    xml.etree.ElementTree.dump(n)



hashval = "fe7007dfa06a5e70931e03b8fbd437b3"

# This works
#for n in root.findall("project[@hash='%s']"%(hashval)):
#    print "Found project: %s"%(n.get('name'))

# This works
#n = root.find("project")
#if n is not None:
#    print "Found project: %s"%(n.get('name'))



project = root.find("project[@name='%s']"%(hashval))
if project is not None:
    print "Found project: %s"%(project.get('name'))


# Get a random QR (works)
randomqr = project.find("decode/session[@index='0']/set[@index='1']/matrix[@index='0']/row[@index='0']/QR[@index='2']")
if randomqr is not None:
    print "Random QR: %s"%(randomqr.get('result'))
else:
    print "didn't find"



# GET PARENT:
#parent = randomqr.find(".//row/..")
parent_map = {c:p for p in et.iter() for c in p}
parent = parent_map[randomqr]
#parent = randomqr.find(".//..")
# works but assumes we already know
#parent = project.find(".//decode/session[@index='0']/set[@index='1']/matrix[@index='0']/row[@index='0']/QR[@index='2']...")
print "Random QR's parent: %s %s"%(parent.tag, parent.get('index'))


# DFS of result of all QR codes under merged (works)
merged = project.find("decode/merged_session")
if merged is not None:
    #print "Found merged"
    it = merged.iter()
    while True:
        try:
            node = it.next()
            if node.tag == "QR":
                print "%s: %s"%(node.tag, node.get('result'))
        except StopIteration:
            break



# Pretty print attempt
#xx = etree.parse(et)
#print etree.tostring(x, pretty_print = True)




exit(0)









xml = SimpleXmlTree.SimpleXmlTree(sys.argv[1])

root = xml.getRoot()
#print root.dump()

myxmltreevisitor = MyXmlTreeVisitor(SimpleXmlTree.XmlTreeVisitorType.depthfirst)
myxmltreevisitor.visit(root)


#jonny = attempts.getGrandChild("matrix", 2)
#print jonny.getParent().getParent()
exit(-1)

for attempt in attempts:
    visitor = XmlDecodeVisitor.XmlSetVisitor([3, 2, 3, 2])
    visitor.visit(attempt)
    iterator = visitor.getMapIter(attempt)
    print visitor.map
    print iterator.next()
    #print visitor.map
   # print visitor.getEmptyMap()
    

   # for matrix in attempt:
        #print matrix.dump()
    #    visitor = XmlDecodeVisitor.XmlMatrixVisitor([3, 2, 3])
     #   visitor.visit(matrix)
      #  print visitor.matrixMap

exit(-1)

print visitor.isDecoded(xmlnode)


exit(-1)


targets = xmlnode.getNodes(Settings.attempt_tag)
rendered_targets = []

for target in targets:
    rendered_targets.append(target.travel(xmlnodetk))


l = []
for rendered_target in rendered_targets:
    print rendered_target
    #print(getDepth(rendered_target))
    l.append(np.array(flatten(rendered_target)))

start = True
for boo in l:
    if start:
        y = boo
        start = False
    else:
        y = y | boo
print y

xmlnodetk.child_action = child_action
xmlnodetk.child_action_args = y.tolist()


targets[0].travel(xmlnodetk)



xml.update()
