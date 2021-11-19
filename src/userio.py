import re
import os
import re
class userio:
    """
    Class that defines all the methods to interact with users like getting unput from user
    and showing different kind of messages and warnings to them.
    """
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    def fprint(msg):
        msg=re.sub("@blue@",userio.bcolors.OKBLUE,msg)
        msg=re.sub("@green@",userio.bcolors.OKGREEN,msg)
        msg=re.sub("@cyan@",userio.bcolors.OKCYAN,msg)
        msg=re.sub("@yellow@",userio.bcolors.WARNING,msg)
        msg=re.sub("@red@",userio.bcolors.FAIL,msg)
        msg=re.sub("@purple@",userio.bcolors.HEADER,msg)
        msg=re.sub("@#[a-z]+?@",userio.bcolors.ENDC,msg)
        print(msg)
    def cprint(msg,color):
        if color=='blue':
            print(userio.bcolors.OKBLUE+msg+userio.bcolors.ENDC)
        elif color=='green':
            print(userio.bcolors.OKGREEN+msg+userio.bcolors.ENDC)
        elif color=='cyan':
            print(userio.bcolors.OKCYAN+msg+userio.bcolors.ENDC)
        elif color=='yellow':
            print(userio.bcolors.WARNING+msg+userio.bcolors.ENDC)
        elif color=='red':
            print(userio.bcolors.FAIL+msg+userio.bcolors.ENDC)
        elif color=='purple':
            print(userio.bcolors.HEADER+msg+userio.bcolors.ENDC)
        else:
            print(msg)
    def success(msg,pause=False):
        print(userio.bcolors.OKGREEN+msg+userio.bcolors.ENDC)
        #Pause will wait for user input to continue
        if pause:
            input()
    def error(msg,pause=False):
        print(userio.bcolors.FAIL+msg+userio.bcolors.ENDC)
        #Pause will wait for user input to continue
        if pause:
            input()
    def warning(msg,pause=False):
        print(userio.bcolors.WARNING+msg+userio.bcolors.ENDC)
        #Pause will wait for user input to continue
        if pause:
            input()
    def showmenu(options=[],header=None):
        if header:
            print(userio.bcolors.HEADER+header+userio.bcolors.ENDC)
        count=1
        for i in options:
            print(userio.bcolors.OKBLUE+str(count)+"."+userio.bcolors.ENDC+str(i))
            count+=1
        while True:
            ch=getdata(regex="\d+\Z")
            if int(ch)>=1 and int(ch)<=len(options):
                return ch
            error("Option not found")
    def getdata(prompt=">>",regex=None,default=None,message="Invalids",password=False):
        #If there is a value in regex, by default it means, this funtion expects a valid value from user.
        #Hence it will infinitely ask user to enter valid data. user cannot escape just by pressing enter.
        #If there is no regex given, All kind of input is acceptable including blank. hence user can just "press any key to continue" using this
        #if user should be allowed to enter valid value and also escape by pressing empty enter. Adjust regex accordingly.
        errcount=0
        while(True):
            data=None
            if password:
                data=getpass.getpass(userio.bcolors.OKBLUE+prompt+userio.bcolors.ENDC)
            else:
                data=input(userio.bcolors.OKBLUE+prompt+userio.bcolors.ENDC)
            if not data:
                if default:
                    return default
            if regex:
                if re.match(regex,data):
                    return data
                else:
                    if default and errcount==2:
                        error("Invalid again. Default "+str(default)+" assumed")
                        return default
                    error(message)
                    errcount+=1
                    continue
            return data
    def confirm(prompt="(y/n):"):
        while True:
            choice=input(userio.bcolors.OKCYAN+prompt+userio.bcolors.ENDC)
            if choice in ['y','Y','Yes','YES','yes','yeah','Yeah','YEAH','ya','Ya','YA','yep','Yep','YEP']:
                return True
            elif choice in ['n','N','no','No','NO','Nope','nope','NOPE']:
                return False
            else:
                error("Invalid option")
