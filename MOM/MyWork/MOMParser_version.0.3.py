import xml.etree.ElementTree as ET
  
class MomParser(object):
    def __init__(self, name):
        self.name = name
        self.ns = {}
        self.root = None
        for event, elem in ET.iterparse(name, events=('start','end')):
            #print elem.tag
            if event == 'start' and self.root == None:              
                self.root = elem.tag                                                
                #print self.root
            elif event == 'start':
                #print event, elem
                if elem.tag == 'class':
                    #print elem.attrib.values()[0]
                    moName = elem.attrib.values()[0]
                    mo = MO(moName)     
                elif elem.tag == 'enum': pass
                elif elem.tag == 'struct': pass
                elif elem.tag == 'exception': pass
                else: pass
            elif event == 'end':
                if elem.tag == 'class':
                    for mo_child in elem:
                        if mo_child.tag == 'description': mo.description = mo_child.text
                        elif mo_child.tag == 'attribute':
                            #print child.attrib.values()[0]
                            attrName = mo_child.attrib.values()[0]
                            attr = ATTR(attrName)
                            for attr_child in mo_child:
                                '''
                                if len(attr_child.text) == 0:
                                    print 'text x', attr_child.text
                                else:
                                    print 'text o', attr_child.text
                                '''
                                if attr_child.tag == 'description': attr.description = attr_child.text
                                elif attr_child.tag == 'dataType': pass
                                else: 
                                    temp = attr_child.tag 
                                    attr.temp = attr_child.text
                            attr.mo = moName
                            mo.attribute.append(attr)
                            print attr.__dict__
                        else:
                            if len(mo_child._children) == 0:
                                mo.info = mo_child.tag
                            else:
                                print mo_child.tag
                    print mo.__dict__
                else: pass         
            else: pass#print event, elem
    
class MO(object):
    def __init__(self, name):
        self.name = name
        self.attribute = []
        self.description = None
        self.parents = None
        self.child = None
        
    def __getattribute__(self, attr):
        #print "get attr %s" % attr
        return object.__getattribute__(self, attr)
    def __setattr__(self, attr, val):
        #print "set attr %s to %r" % (attr, val)
        return object.__setattr__(self, attr, val)
    '''
    def __len__(self):
        return len(self.name)
    def __getitem__(self, k):
        return self.name[k]
    def __setitem__(self, k, v):
        self.name[k] = v
    '''
    
class ATTR(object):
    def __init__(self, name):
        self.name = name
        self.description = None
        self.mo = None
    def __getattribute__(self, attr):
        #print "get attr %s" % attr
        return object.__getattribute__(self, attr)
    def __setattr__(self, attr, val):
        #print "set attr %s to %r" % (attr, val)
        return object.__setattr__(self, attr, val)
    
if __name__ == '__main__':
    #name = "LteRbsNodeComplete_Itr27_R10D03.xml"
    name = "sample.xml"
    parser = MomParser(name)
    #print parser.ns    
