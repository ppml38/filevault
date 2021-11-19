"""
filevaule: App that can securely store the confidential files.
Author: Prakash
Project started date: 31-10-2021
Project finished date: 19-11-2021
"""
import getpass
import os

from filestruct import filestruct
from userio import userio
from config import config

if __name__=='__main__':
    MASTERPASSWORD=None
    VAULTPATH='vaultpath'
    VAULT_FILENAME_LENGTH='vault_filename_length'
    BLOCK_LENGTH='block_length'
    CONF_FILE="filevault.conf"
    #Run starts
    conf=config(CONF_FILE)
    os.system('cls')
    MASTERPASSWORD=getpass.getpass("Master password:")
        
    #Read through the filevault and generate file structure tree
    fs=filestruct(conf.get(VAULTPATH),MASTERPASSWORD,conf.get(VAULT_FILENAME_LENGTH),conf.get(BLOCK_LENGTH))
    while True:
        os.system('cls')
        userio.cprint("--------------------------------------------",'cyan')
        userio.fprint("@green@FILEVAULT:@#green@ @cyan@"+fs.getfullpath()+"@#cyan@")
        userio.cprint("--------------------------------------------",'cyan')
        #Show first level directory list
        clist=fs.ls()
        if clist:
            for i in clist:
                if i[-1]==os.sep:
                    userio.cprint(i,'blue')
                else:
                    print(i)
        else:
            print("empty")
        #Show option to add, get, delete and update
        userio.cprint("\n\n--------------------------------------------",'cyan')
        cmd_str=input("Commands: add, get, delete, mkdir, cd, exit\n>>")
        
        command=[]
        temp=''
        quote=None
        for i in cmd_str.strip():
            if quote:
                if i==quote:
                    if temp:
                        command.append(temp)
                    temp=''
                    quote=None
                else:
                    temp+=i
            else:
                if i in ['"',"'"]:
                    quote=i
                elif i==' ':
                    if temp:
                        command.append(temp)
                    temp=''
                    quote=None
                else:
                    temp+=i
        if quote:
            userio.error("quote mismatch",True)
            continue
        if temp:
            command.append(temp)
        if not command:
            continue
        #command=cmd_str.strip().split(' ')
        args=[a for a in command[1:] if a.strip()]
        command=command[0].lower()
        #Act as per option
        if command=='exit':
            break
        elif command=='cd':
            if len(args)==1:
                if not fs.cd(args[0]):
                    userio.error("Error changing directory",True)
            else:
                userio.error("Usage: cd [newpath|/|..]",True)
        elif command=='add':
            print("Adding...")
            if len(args)==1:
                if not fs.addfile(args[0]):
                    userio.error("Error adding file",True)
                else:
                    userio.success("Completed",True)
            else:
                userio.error("Usage: add filename",True)
        elif command=='get':
            print("Getting...")
            if len(args) in [1,2]:
                if fs.getfile(args[0],args[1] if len(args)==2 else None):
                    userio.success("Done",True)
                else:
                    userio.error("Error getting file",True)
            else:
                userio.error("Usage: get filename downloadpath",True)
        elif command=='delete':
            if len(args)==1:
                if fs.delete(args[0]):
                    userio.success("Done",True)
                else:
                    userio.error("Error deleting file",True)
            else:
                userio.error("Usage: delete filename",True)
        elif command=='mkdir':
            if len(args)==1:
                if fs.mkdir(args[0]):
                    userio.success("Done",True)
                else:
                    userio.error("Error creating directory",True)
            else:
                userio.error("Usage: mkdir foldername",True)
        else:
            userio.error("No such command",True)
        