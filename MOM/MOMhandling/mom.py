from MOMParser import IterParser
import re, argparse, os, difflib 
from define import * 
from collections import OrderedDict

class ParsingMom(IterParser):
    def __init__(self, name):
        IterParser.__init__(self, name)
        self.root = root
        self.line = "*" * 132
        self.sortMO = sorted(self.mos.keys())
    
    def showMom(self, mo = None, attr = None):
        show_info = ''
        show_info += '%s\nname:%s version:%s release:%s author:%s revision:%s\n' %(self.line, self.mim['name'], self.mim['version'], self.mim['release'], self.mim['author'], self.mim['revision'])
        if mo is None and attr is None:
            show_info += '%s\n%s\n%s\n' %(self.line, "MO".ljust(30), self.line)
            for mo in self.sortMO:
                show_info += '%s\n' % mo
            show_info += '%s\n%s\n%s\n' %(self.line, "ENUM".ljust(30), self.line) 
#             for enum in sorted(self.enums):
#                 show_info += '%s\n' % enum
            for moc in self.sortMO:
                getMo = self.mos[moc]
                show_info += '%s\n' % getMo.showMoInfo()
                show_info += '%s\n%s%s%s%s%s%s\n%s\n' % (self.line, "MOC".ljust(30), 'Attribute'.ljust(30), 'defaultValue'.ljust(20), 'Flags'.ljust(40), 'Length'.ljust(20), 'Range'.ljust(20), self.line)
                attr_list = getMo.getAttrs()
                for attr_name in sorted(attr_list):
                    getAttr = attr_list[attr_name]
                    show_info += '%s%s%s%s%s%s\n' % (getAttr.getMoName().ljust(30), getAttr.getName().ljust(30), getAttr.getDefault().ljust(20), getAttr.getFlags().ljust(40), getAttr.getLength().ljust(20), getAttr.getRange())
                    
        if mo is not None and attr is None:
            p = re.compile(mo, re.IGNORECASE)
            for moc in self.sortMO:
                check = p.search(moc)
                if check:   
                    getMo = self.mos[moc]
                    show_info += '%s\n' % getMo.showMoInfo()
                
        if mo is None and attr is not None:
            show_info += '%s\n%s%s%s%s%s%s\n%s\n' % (self.line, "MOC".ljust(30), 'Attribute'.ljust(30), 'defaultValue'.ljust(20), 'Flags'.ljust(40), 'Length'.ljust(20), 'Range'.ljust(20), self.line)
            p = re.compile(attr, re.IGNORECASE)
            for attr_name in sorted(self.attrs):
                check = p.search(attr_name)
                if check:
                    getAttr = self.attrs[attr_name]
                    show_info += '%s%s%s%s%s%s\n' % (getAttr.getMoName().ljust(30), getAttr.getName().ljust(30), getAttr.getDefault().ljust(20), getAttr.getFlags().ljust(40), getAttr.getLength().ljust(20), getAttr.getRange())
                
        if mo is not None and attr is not None:
            p = re.compile(mo, re.IGNORECASE)
            for moc in self.sortMO:
                check = p.search(moc)
                if check:   
                    getMo = self.mos[moc]
                    show_info += '%s\n%s%s%s%s%s%s\n%s\n' % (self.line, "MOC".ljust(30), 'Attribute'.ljust(30), 'defaultValue'.ljust(20), 'Flags'.ljust(40), 'Length'.ljust(20), 'Range'.ljust(20), self.line)
                    m = re.compile(attr, re.IGNORECASE)
                    attr_list = getMo.getAttrs()
                    for attr_name in sorted(attr_list):
                        check1 = m.search(attr_name)
                        if check1:
                            getAttr = attr_list[attr_name]
                            show_info += '%s%s%s%s%s%s\n' % (getAttr.getMoName().ljust(30), getAttr.getName().ljust(30), getAttr.getDefault().ljust(20), getAttr.getFlags().ljust(40), getAttr.getLength().ljust(20), getAttr.getRange())
        return show_info
        
    def showDesc(self, mo = None, attr = None):
        show_info = ''
        show_info += '%s\nname:%s version:%s release:%s author:%s revision:%s\n' %(self.line, self.mim['name'], self.mim['version'], self.mim['release'], self.mim['author'], self.mim['revision'])
        if mo is None and attr is None:
            for moc in self.sortMO:
                getMo = self.mos[moc]
                show_info += '%s\n%s%s\n' %(self.line,"MO = ", getMo.getName())
                show_info += '%s%s\n'%("description = ".ljust(10), getMo.getDesc())
            
        if mo is not None and attr is None:
            p = re.compile(mo, re.IGNORECASE)
            for moc in self.sortMO:
                check = p.search(moc)
                if check:   
                    getMo = self.mos[moc]
                    show_info += '%s\n%s%s\n' %(self.line,"MO = ", getMo.getName())
                    show_info += '%s%s\n'%("description = ".ljust(10), getMo.getDesc())
                    attr_list = getMo.getAttrs()
                    for attr_name in sorted(attr_list):
                        getAttr = attr_list[attr_name]
                        show_info += '%s\n%s\t%s\n' %(self.line, getAttr.getName(), getAttr.getDesc())
                        
        if mo is None and attr is not None:
            p = re.compile(attr, re.IGNORECASE)
            for attr_name in sorted(self.attrs):
                check = p.search(attr_name)
                if check:
                    getAttr = self.attrs[attr_name]
                    show_info += '%s\n%s%s\t%s%s\n' %(self.line,"MO = ", getAttr.getMoName(),"ATTR = ", getAttr.getName())
                    show_info += '%s%s\n'%("description = ".ljust(10), getAttr.getDesc())
                        
        if mo is not None and attr is not None:
            p = re.compile(mo, re.IGNORECASE)
            for moc in self.sortMO:
                check = p.search(moc)
                if check:   
                    getMo = self.mos[moc]
                    m = re.compile(attr, re.IGNORECASE)
                    attr_list = getMo.getAttrs()
                    for attr_name in sorted(attr_list):
                        check1 = m.search(attr_name)
                        if check1:
                            getAttr = attr_list[attr_name]
                            show_info += '%s\n%s%s\t%s%s\n' %(self.line,"MO = ", getAttr.getMoName(),"ATTR = ", getAttr.getName())
                            show_info += '%s%s\n'%("description = ".ljust(10), getAttr.getDesc())
        return show_info
    
    def findParent(self, child, tree_list):
        for key, value in self.relations.items():
            if key[-10:] == ref_to_By: pass
            elif child == value.getChildName():
                parent = value.getParentName()
                cardi = value.getCaldi()
                child_cardi = child + cardi
                tree_list.insert(0, child_cardi)
                if parent == root: 
                    tree_list.insert(0, root + '[1]')
                    return tree_list
                else: return self.findParent(parent, tree_list)
            else: pass
        
    def findChild(self, parent):
        child_dic = {}
        for key, value in self.relations.items():
            if key[-10:] == ref_to_By: pass
            elif parent == value.getParentName():
                child = value.getChildName()
                cardi = value.getCaldi()
                child_cardi = child + cardi
                child_dic.update({child:child_cardi})
            else: pass
        return child_dic
    
    def checkSys(self, tree_list):
        if tree_list[-1][-3:] == '[1]':
            return '(systemCreated)'
        else: return ''
    
    def treeStruct(self, tree_list, show_info, mo):
        child_list = self.findChild(mo)
        if child_list != {}:
            for child in child_list:
                tree_list.append(child_list[child])
                show_info += '%s%s\n' % (tree_list, self.checkSys(tree_list))
                check_child = self.findChild(child)
                if check_child != {}:
                    for gchild in check_child:
                        tree_list.append(check_child[gchild])
                        show_info += '%s%s\n' % (tree_list, self.checkSys(tree_list))
                        check2_child = self.findChild(gchild)
                        if check2_child != {}:
                            for ggchild in check2_child:
                                tree_list.append(check2_child[ggchild])
                                show_info += '%s%s\n' % (tree_list, self.checkSys(tree_list))
                                check3_child = self.findChild(ggchild)
                                if check3_child != {}:
                                    for gggchild in check3_child:
                                        tree_list.append(check3_child[gggchild])
                                        show_info += '%s%s\n' % (tree_list, self.checkSys(tree_list))
                                        tree_list.pop()
                                tree_list.pop()
                        tree_list.pop()
                tree_list.pop()
        tree_list.pop()
        return show_info
    
    def relation(self, mo = None):
        show_info = ''
        if mo == None:
            tree_list = []
            tree_list.append(root + '[1]')
            show_info += '%s\n' % self.treeStruct(tree_list, show_info, root)
        else:
            p = re.compile(mo, re.IGNORECASE)
            for key, value in self.relations.items():
                if key[-10:] == ref_to_By: pass
                else:
                    parent_mo = value.getParentName() 
                    child_mo = value.getChildName()
                    cardi = value.getCaldi()
                    child_cardi = child_mo + cardi
                    check = p.search(child_mo)
                    if check:
                        tree_list = []
                        tree_list.append(child_cardi)
                        tree_list = self.findParent(parent_mo, tree_list)
                        show_info += '%s%s\n' % (tree_list, self.checkSys(tree_list))
                        show_info += '%s\n' % self.treeStruct(tree_list, show_info, child_mo)
        return show_info
    
def diff(prev, cur):
    diff = difflib.ndiff(prev.splitlines(), cur.splitlines())
    diffstr = ''
    for line in list(diff):
        if line.split(' ')[0] == prev:
            diffstr += red % line
        elif line.split(' ')[0] == modified:
            diffstr += yellow % line
        elif line.split(' ')[0] == new:
            diffstr += green % line
        else:
            pass
            # if you want to add previous mom, please turn on this sentence
            #diffstr += '%s\n' % line
    return diffstr

#add argparse operation
def argParse():
    if args.version == Gen1:
        if args.file:
            cur_mom = open('mom', 'wb')
            cur_mom.write(args.file.read())
            cur_mom.close()
            
        elif args.currentMOM:
            filename = os.popen(Gen1_MOM)
            cur_mom = open('mom', 'wb')
            cur_mom.write(filename.read())
            cur_mom.close()
            
        elif args.diff:
            cur_mom = open('mom','rb')
            commit = os.popen(Gen1_commit)
            prev_commit = commit.readlines()[1]
            prev_commit = prev_commit.split(' ')[0]
            read_prev_mom = os.popen(Gen1_prevMOM % prev_commit)
            
            prev_mom = open('prevmom','wb')
            prev_mom.write(read_prev_mom.read())
            prev_mom.close()
            prev_mom = open('prevmom','rb')
            
            if args.mom:
                parser1 = ParsingMom(prev_mom)
                parser2 = ParsingMom(cur_mom)        
                prev_str = parser1.showMom(args.mo, args.attr)
                cur_str = parser2.showMom(args.mo, args.attr)
                diff_file =  diff(prev_str, cur_str)
                print diff_file
                
            elif args.description:
                parser1 = ParsingMom(prev_mom)
                parser2 = ParsingMom(cur_mom)        
                prev_str = parser1.showDesc(args.mo, args.attr)
                cur_str = parser2.showDesc(args.mo, args.attr)
                diff_file =  diff(prev_str, cur_str)
                print diff_file
        else:
            if args.mom:
                try: 
                    cur_mom = open('mom','rb')
                    parser = ParsingMom(cur_mom)
                    print parser.showMom(args.mo, args.attr)
                except Exception as ex: print ex 
            
            elif args.description:
                try: 
                    cur_mom = open('mom','rb')
                    parser = ParsingMom(cur_mom)
                    print parser.showDesc(args.mo, args.attr) 
                except Exception as ex: print ex     
            elif args.tree:
                try:
                    cur_mom = open('mom', 'rb')
                    parser = ParsingMom(cur_mom)
                    print parser.relation(args.mo)
                except Exception as ex: print ex     
                
    elif args.version == Gen2:
        if args.file:
            cur_mom = open('mom2', 'wb')
            cur_mom.write(args.file.read())
            cur_mom.close()
            
        elif args.currentMOM:
            filename = os.popen(Gen2_MOM)
            cur_mom = open('mom2', 'wb')
            cur_mom.write(filename.read())
            cur_mom.close()
            
        elif args.diff:
            cur_mom = open('mom2','rb')
            commit = os.popen(Gen2_commit)
            prev_commit = commit.readlines()[1]
            prev_commit = prev_commit.split(' ')[0]
            read_prev_mom = os.popen(Gen2_prevMOM % prev_commit)
            
            prev_mom = open('prevmom','wb')
            prev_mom.write(read_prev_mom.read())
            prev_mom.close()
            prev_mom = open('prevmom','rb')
            
            if args.mom:
                parser1 = ParsingMom(prev_mom)
                parser2 = ParsingMom(cur_mom)        
                prev_str = parser1.showMom(args.mo, args.attr)
                cur_str = parser2.showMom(args.mo, args.attr)
                diff_file =  diff(prev_str, cur_str)
                print diff_file
                
            elif args.description:
                parser1 = ParsingMom(prev_mom)
                parser2 = ParsingMom(cur_mom)        
                prev_str = parser1.showDesc(args.mo, args.attr)
                cur_str = parser2.showDesc(args.mo, args.attr)
                diff_file =  diff(prev_str, cur_str)
                print diff_file
        else:
            if args.mom:
                try: 
                    cur_mom = open('mom2','rb')
                    parser = ParsingMom(cur_mom)
                    print parser.showMom(args.mo, args.attr)
                except Exception as ex: print ex 
            
            elif args.description:
                try: 
                    cur_mom = open('mom2','rb')
                    parser = ParsingMom(cur_mom)
                    print parser.showDesc(args.mo, args.attr) 
                except Exception as ex: print ex     

# add argparse command line option
parser = argparse.ArgumentParser(description = 'Test MOM handling')
parser.add_argument('-i', dest ='file', action = 'store', type = argparse.FileType('r'), help = 'If you want to show specific MOM version, input filename by using -i option')
# parser.add_argument('version', action = 'store', type = int, help = 'Choose G1 or G2 by num(G1=1, G2=2)')
parser.add_argument('-p', dest ='currentMOM', action = 'store_true', help = 'Load current MOM by using -p option')
parser.add_argument('-mo', dest = 'mo', action = 'store', help = 'Search specific mo using -mo option')
parser.add_argument('-attr', dest = 'attr', action = 'store', help = 'Search specific attr using -attr option')
parser.add_argument('-d', dest ='description', action = 'store_true', help = 'Show only description about specific mo')
parser.add_argument('-diff', dest ='diff', action = 'store_true', help = 'Show difference between current MOM xml and prev MOM xml')
parser.add_argument('-a', dest ='mom', action = 'store_true', help = 'Show all information in MOM')
parser.add_argument('-t', dest ='tree', action = 'store_true', help = 'Show relationship between MOs') 
args = parser.parse_args()  
# argParse()

def testcase():
    name = "LteRbsNodeComplete_Itr27_R10D03.xml"
    parser = ParsingMom(name)
    a = parser.relation()
#     a = parser.relation(mo='celltdd')
#     a = parser.relation(mo='uemeascontrol')
    print a
#     print parser.showMom()
#     print parser.showMom(mo='nbiot', attr='cell')
#     print parser.showMom(mo='vzsdfwe')
#     print parser.showMom(mo='nbiot')
#     print parser.showMom(attr='id$')
#     print parser.showDesc(mo='nbiot')
#     print parser.showDesc(attr='id$')
#     print parser.showDesc(mo='nbiot', attr='cell')
if __name__ == '__main__':
    testcase()

