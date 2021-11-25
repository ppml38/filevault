class node:
    #Name of the file or directory
    name=None
    
    #'dir' or 'file'
    nodetype=None
    
    #List of all child nodes
    #Applicable only to folders NOT files
    children=None
    
    #List of all physical encrypted file names(Full path), that make up this file
    #Applicable only to files NOT folders
    hardfilelist=None
    
    #Parent node
    parent=None
    
    def __init__(self,name,nodetype,hardfiles=None): #Files will have None hardfiles, empty directory will have [] hardfiles
        self.name=name
        self.nodetype=nodetype
        self.parent=self
        if nodetype=='file':
            self.children=None
            self.hardfilelist=hardfiles
        else:
            self.children=[]
            self.hardfilelist=None
    def __str__(self):
        return str({"name":self.name,"nodetype":self.nodetype,"parent":self.parent.getrealname(),"children":[a.getrealname() for a in self.children] if self.children else str(self.children),"hardfiles":self.hardfilelist})
    def getname(self):
        return self.name
    def getrealname(self):
        if self.isfile():
            return self.name[:self.name.rfind("_")]
        return self.getname()
    def getllen(self):
        #Last block length
        return int(self.name.split("_")[-1])
    def getchildren(self):
        return self.children
    def gettype(self):
        return self.nodetype
    def isfile(self):
        return True if self.nodetype=='file' else False
    def isdir(self):
        return True if self.nodetype=='dir' else False
    def gethardfilelist(self):
        return self.hardfilelist
    def getparent(self):
        return self.parent
    def addchild(self,nd):
        if self.nodetype=='dir':
            nd.parent=self
            self.children.append(nd)
        else:
            return False
        return True
    def getchild(self,name,type=None):
        for i in self.children:
            if i.name==name:
                if type:
                    if i.nodetype==type:
                        return i
                else:
                    return i
        return False
    def contains(self,name,type=None):
        for i in self.children:
            if i.name==name:
                if type:
                    if i.nodetype==type:
                        return True
                else:
                    return True
        return False
                
    def delete(self,name=None):
        #Applicable only to folders
        if not self.isdir():
            return False
        ser=0
        for i in self.children:
            if i.getname()==name:
                break
            ser+=1
        else:
            return False
        del self.children[ser]
        return True
