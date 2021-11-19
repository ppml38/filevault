from userio import userio
from node import node
from crypto import crypto
import os
class filestruct:
    """
    All file manipulation operation will be handled here
    This will handle physical manipulation of files and maintain a Tree data structure.
    """
    root=None
    pwd=None
    key='' #to include cryptography functionality with file manipulation, fill this field with key
    filename_length=None
    block_length=None
    vaultpath=None
    def __init__(self,path,key='',filename_length=10,block_length=10240):
        self.key=key
        self.filename_length=filename_length
        self.block_length=block_length
        self.vaultpath=path
        self.root=node('','dir')
        self.pwd=self.root
        if len(os.listdir(path))==0:
            #Empty vault
            pass
        else:
            vfiles=os.listdir(self.vaultpath) #Vault files as is
            files={} #Actual files
            for i in vfiles:
                dc=crypto.decrypt_filename(i,self.key,self.filename_length)
                pos=int(dc.split("_")[-1].split(':')[-1])-1
                llen=dc.split("_")[-1].split(':')[0] #Last block length
                #key will have _llen as a suffix to show what is the length of last block
                key=dc[:dc.rfind("_")]+"_"+llen
                if key in files:
                    if pos<len(files[key]):
                        pass
                    else:
                        files[key]+=[None]*(pos+1-len(files[key]))
                else:
                    files[key]=[None]*(pos+1)
                files[key][pos]=i
            #print(files)
            #combine files of _0 and _llen into one.
            cfiles={}
            ds=[]
            for f in files:
                if f.split("_")[-1]!="0":
                    count=0
                    if f.split("_")[0]+"_0" in files:
                        for i in files[f.split("_")[0]+"_0"]: #copy from _0 to _llen and delete _0
                            files[f][count]=i
                            count+=1
                        ds.append(f)
            for i in ds:
                del files[i[:i.rfind("_")]+"_0"]
            #print(files)
            #input()
            for f in files:
                self.recursively_addfile(f,files[f],self.root)
    def getpwd(self):
        return self.pwd.getrealname()
    def getfullpath(self,n=None):
        if not n:
            n=self.pwd
        if n==self.root:
            return os.sep
        if n.isdir():
            return self.getfullpath(n.getparent())+n.getrealname()+os.sep
        else:
            return self.getfullpath(n.getparent())+n.getrealname()
    def ls(self):
        #Adds '/' at the end of directory list
        d=[]
        f=[]
        for i in self.pwd.children:
            if i.nodetype=='dir':
                d.append(i.getrealname()+os.sep)
            else:
                f.append(i.getrealname())
        d.sort()
        f.sort()
        return ["."+os.sep,".."+os.sep]+d+f
    def getnode(self,path,nodetype=None,current_node=None):
        """
        Searches for the path provided and returns the nodes that match
        Note: There can be more than one match for a given path ex. A file and a folder named same.
        Hence we need to return the array of matches
        
        This searches through the tree recursively.
        Current node: The node we are in now
        Path: Path we have to search for
        Nodetype: Type of node we are looking, list of matches if None
        
        Returns [] if there is no such node
        else returns the node(s)
        """
        #Return nothing if nothing provided in path
        if not path:
            return None

        #Split the path into list of folders, for traversal
        if isinstance(path,str):
            path=path.strip().split(os.sep)
        
        #If there is no current node provided start searching from present working directory
        if not current_node:
            current_node=self.pwd
        
        if len(path)==1: #We have reached the end of given path
            #Return the required node
            
            #If the path ended with \ or /, the last of list will be empty string, hence return current_node
            if not path[0]:
                return [current_node]

            #Parent directory
            if path[0]=='..':
                return [current_node.parent]
            
            #Present directory
            if path[0]=='.':
                return [current_node]
                
            #If the path provided is among children return them
            nlist=[]
            for n in current_node.getchildren():
                if n.getrealname()==path[0]:
                    if nodetype:
                        if n.gettype()==nodetype:
                            nlist.append(n)
                    else:
                        nlist.append(n)
            return nlist
        else:
            #Traverse to the upper node and start sub-recursion, to the remaining path

            #If the path started with \ or /, the first of list will be empty string. that means the path starts from root.
            if not path[0]:
                current_node=self.root
                return self.getnode(path[1:], nodetype, current_node)

            #Parent directory
            if path[0]=='..':
                current_node=current_node.parent
                return self.getnode(path[1:], nodetype, current_node)
            
            #Present directory
            if path[0]=='.':
                return self.getnode(path[1:], nodetype, current_node)
            
            #Get all the children that match, then sub-recurse to each
            nlist=[]
            for n in current_node.getchildren():
                if n.getrealname()==path[0]:
                    nlist.append(n)
            #start the recursion for further traversal
            nodes=[]
            for n in nlist:
                ns=self.getnode(path[1:], nodetype, n)
                if ns:
                    for i in ns:
                        nodes.append(i)
            return nodes
    def cd(self,newpath):
        n=self.getnode(newpath)
        if n:
            self.pwd=n[0]
            return True
        else:
            return False
    def getfile(self,nd,externalpath=None):
        if not externalpath:
            externalpath=os.getcwd()
        #Removing \ or / from the given path as we are adding our os.sep
        if externalpath[-1] in ['/','\\']:
            externalpath=externalpath[:-1]
        if isinstance(nd,str):
            nd=self.getnode(nd)
            if nd:
                nd=nd[0]
            else:
                return False
            if nd.isfile(): #If it is a file no need for recursion just save the file and return
                if not os.path.exists(externalpath):
                    os.makedirs(externalpath)
                crypto.decrypt_file(nd.gethardfilelist(),nd.getllen(),self.key,self.vaultpath,externalpath+os.sep+nd.getrealname())
                userio.success("Done : "+externalpath+os.sep+nd.getrealname())
                return True
        #for dirs and files under dirs recursion is required
        if nd.isfile():
            if not os.path.exists(externalpath):
                os.makedirs(externalpath)
            crypto.decrypt_file(nd.gethardfilelist(),nd.getllen(),self.key,self.vaultpath,externalpath+os.sep+nd.getrealname())
            userio.success("Done : "+externalpath+os.sep+nd.getrealname())
        else:
            for i in nd.getchildren():
                self.getfile(i,externalpath+os.sep+nd.getname())
        return True
    def mkdir(self,dirname):
        self.pwd.addchild(node(dirname,'dir',[]))
        return True
    def delete(self,filename):
        n=self.getnode(filename)
        if not n:
            return False
        #By this we are taking first instance, which means, if there are 2 instance of same name, first will be deleted.
        #Physically delete the files from vault.
        self.recursively_delete(n[0])
        
        #Logically Delete from fs
        n[0].getparent().delete(n[0].getname())
        return True
    def recursively_delete(self,n):
        """
        This will recursively go through the files and physically delete the file from vault path
        """
        if n.isfile():
            for i in n.gethardfilelist():
                os.remove(self.vaultpath+os.sep+i)
        else:#Its a directory, we have to recurse though all the files and delete.
            iter_backup=n.getchildren()  #as we are deleting on the fly, we need a seperate backup for smooth iteration.
            for i in iter_backup:
                self.recursively_delete(i)
            
    def recursively_addfile(self,path,hardlist,pwd=None):
        #NOTE: pwd is different from self.pwd
        if not pwd: #If there is no pwd given, that means we need to add in current 'present working directory in file system'
            pwd=self.pwd
            
        folders=[a for a in path.split(os.sep) if a]
        
        if len(folders)==1: #Its just a file name no path prepended
            pwd.addchild(node(folders[-1],'file',hardlist))
        elif len(folders)>1: #There are more paths that we have to travers
            dir=folders[0] #Get first upper directory in the path
            if not pwd.contains(dir,'dir'):
                #Create a directory and initiate sub-recursion
                pwd.addchild(node(dir,'dir',[]))
            self.recursively_addfile(os.sep.join(folders[1:]),hardlist,pwd.getchild(dir,'dir')) #Remove upper dir from the path and initiate sub-recursion with upper dir node as pwd
        else:
            False
        
    def addfile(self,externalpath):
        start=externalpath.rfind(os.path.basename(externalpath))
        if os.path.isfile(externalpath): #File
            (filelist,llen)=crypto.encrypt_file(externalpath,self.vaultpath,self.getfullpath()+externalpath[start:],self.key,self.filename_length,self.block_length)
            if filelist:
                self.pwd.addchild(node(os.path.basename(externalpath)+"_"+llen,'file',filelist))
                userio.success("Done  "+externalpath+"\t"+externalpath[start:])
            else:
                userio.error("Empty file: "+externalpath)
                return False
        elif os.path.isdir(externalpath): #Non-empty directory
            for root,dir,files in os.walk(externalpath):
                if files:
                    for file in files:
                        full_filename=root+os.sep+file
                        (filelist,llen)=crypto.encrypt_file(full_filename,self.vaultpath,os.sep+full_filename[start:],self.key,self.filename_length,self.block_length)
                        if filelist:
                            #adding last block length in the end of full file name
                            full_filename+="_"+llen
                            self.recursively_addfile(full_filename[start:],filelist,self.pwd)
                            userio.success("Done  "+root+os.sep+file)
                        else: #Empty file
                            userio.error("Empty "+root+os.sep+file)
                else: #Empty directory
                    #Empty directories will be thrown away
                    userio.error("Empty "+root)
        else:
            return False
        return True
