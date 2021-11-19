import os
import math
import string
import random
class crypto:
    def encrypt(plain,password=''):
        """
        Encrypts data in plain text, by converting into bytes.
        """
        if password=='': #If password is empty data handled in plain. no encryption or decryption
            return plain
        cipher=[]
        for i in range(len(plain)):
            cipher.append(int.from_bytes(plain[i].encode('utf-8'),byteorder='big')^int.from_bytes(password[i%len(password)].encode('utf-8'),byteorder='big'))
        return bytes(cipher).decode('utf-8')
    def decrypt(cipher,password=''):
        #Since XOR is two-way compatible, we reuse encrypt function to decrypt
        return crypto.encrypt(cipher,password)

    def encrypt_bytes(data,password=''):
        if password=='': #If password is empty data handled in plain. no encryption or decryption
            return data
        password=bytes(password,'utf-8')
        key=password*math.ceil(len(data)/len(password))
        return [i^j for i,j in zip(data,key)]
    def decrypt_bytes(cipher,password=''):
        return crypto.encrypt_bytes(cipher,password)
        
    def new_random_name(length):
        letters = string.ascii_lowercase+string.ascii_uppercase
        return ''.join(random.choice(letters) for i in range(int(length)))
        
    def encrypt_filename(filename,password,length):
        length=int(length)
        #Given file name is in the format of path\to\filename_0:1, path\to\filename_21:3 etc.
        if password=='': #If password is empty data handled in plain. no encryption or decryption
            return filename
            
        #Count given filenamelength and prepend like 18_path\to\filename_1
        count=len(filename)
        filename=str(count)+"_"+filename
        
        #if it is less than required length add junk in the end, like if length=30, then 18_path\to\filename_1hdncjfiej
        if len(filename)<length:
            filename+=crypto.new_random_name(length-len(filename))
        print(filename)
        #Get ready for encryption
        password=bytes(password,'utf-8')
        filename=bytes(filename,'utf-8')
        #Encrypt it with password like jfheydhcnfhgptdhsncjfieodfdscd
        key=password*math.ceil(len(filename)/len(password))
        cip=[i^j for i,j in zip(filename,key)]
        #Shuffle it with password
        offsets=[int(a)%length for a in password]
        offsets=offsets*math.ceil(length/len(offsets))
        for i in range(0,length):
            cip[i],cip[offsets[i]]=cip[offsets[i]],cip[i]
        
        #return
        return '_'.join([str(a) for a in cip])


    def decrypt_filename(cipher,password,length):
        length=int(length)
        #Get bytes out of string
        cip=[int(a) for a in cipher.split('_')]
        password=bytes(password,'utf-8')
        
        #Un-shuffle cipher bytes
        offsets=[int(a)%length for a in password]
        offsets=offsets*math.ceil(length/len(offsets))
        for i in range(length-1,-1,-1):
            cip[i],cip[offsets[i]]=cip[offsets[i]],cip[i]
        
        #Decrypt it with password
        key=password*math.ceil(len(cip)/len(password))
        filename=[i^j for i,j in zip(cip,key)]
        
        #Decode it to readable string
        filename=bytes(filename).decode()
        
        #Extract filename from decoded string
        fn=filename.split('_',1)
        return fn[1][:int(fn[0])]

    def generate_junk(length):
        junk_bytes=bytes([i for i in range(256)])
        return [random.choice(junk_bytes) for i in range(length)]
    def decrypt_file(filelist,llen,key,vaultpath,out_path):
        #Vault path should be a directory
        #out_path should be a file that is to be written
        llen=int(llen)
        with open(out_path,'wb') as o:
            for f in filelist[:-1]:
                with open(vaultpath+os.sep+f,'rb') as f1:
                    o.write(bytes(crypto.decrypt_bytes(f1.read(),key)))
            with open(vaultpath+os.sep+filelist[-1],'rb') as g:
                if llen!=0:
                    o.write(bytes(crypto.decrypt_bytes(g.read(llen),key)))
                else:
                    o.write(bytes(crypto.decrypt_bytes(g.read(),key)))
        return True
    def encrypt_file(in_path,out_path,fs_path,key=None,encrypted_filename_length=10,block_length=10240):
        """
        This function gets full path of physical filenames
        seperate it into blockfiles, encrypt it, and save it in filevault and returns list of encrypted file names
        
        Note: This accepts only filenames, incase a directory supllied in in_path, it will return empty list.
        """
        block_length=int(block_length)
        encrypted_filename_length=int(encrypted_filename_length)
        if os.path.isdir(in_path) or (not os.path.isfile(in_path)):
            return []
        encrypted_filenames=[]
        llen="0"
        with open(in_path,'rb') as inf:
            count=1
            while data:=inf.read(block_length):
                #Adding byte length in filename and junk in content, if data is less than block length
                #Filename should be suffixed with "_len:count", where len will be 0 all except last block which has less data than block length.
                data=list(data)
                fname=''
                if len(data)<block_length:
                    fname=fs_path+("_"+str(len(data)))
                    llen=str(len(data))
                    data+=crypto.generate_junk(block_length-len(data))
                else:
                    fname=fs_path+("_0")
                
                #Check if new filename already exists and create new for 3 times and and raise exception if not.
                for i in range(3):
                    #Adding count with path and encrypt it.
                    encrypted_file_name=crypto.encrypt_filename(fname+":"+str(count),key,encrypted_filename_length)
                    if not os.path.exists(in_path+os.sep+encrypted_file_name):
                        break
                else:
                    raise Exception("File name exhausted")

                cipher=crypto.encrypt_bytes(data,key)
                #Write the file only after all performed without erro
                with open(out_path+os.sep+encrypted_file_name,'wb') as output:
                    output.write(bytes(cipher))
                encrypted_filenames.append(encrypted_file_name)
                count+=1
        return (encrypted_filenames,llen)
