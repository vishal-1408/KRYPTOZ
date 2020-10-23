import os, random

homedir=os.path.expanduser('~') + '/AppData/Roaming/Kryptoz/' 

def Return_App_Path(filename): #This returns app directory 
    global homedir
    if os.path.isdir(homedir):
        return homedir + filename
    else:
        os.makedirs(homedir)
        return homedir + filename

def User_Code_Directory(filename):
    global homedir
    code_dir = homedir + '/UserCodes/'
    if os.path.isdir(code_dir):
        return code_dir+filename
    else:
        os.makedirs(code_dir)
        return code_dir + filename

def ECC_key_dir(filename):
    global homedir
    keys_dir = homedir + '/ECCkeys/'
    if os.path.isdir(keys_dir):
        return keys_dir+filename
    else:
        os.makedirs(keys_dir)
        return keys_dir + filename
    
def return_credentials():
    file = open(Return_App_Path("UserCredentials.txt"), 'r')
    Credential_List = ReadFile(file)
    file.close()
    return Credential_List
    
def User_Check(username_hash, password_hash):
    Credential_List=return_credentials()
    i = 1
    for entry in Credential_List:
        if i%2==1:
            if username_hash==entry:
                return True
        i+=1
    return False

def ReadFileLine(file): #This reads one line from file
	data = file.readline().replace('\n', '')
	return data

def ReadFile(file): #This reads whole file line by line and returns it as list
	data = file.read().split('\n')
	return data

def WriteSeperator(file, info, sep): #This writes each element of list inot a file where the elements are sperated by sep
	infoStr= ''
	for char in info:
		infoStr = infoStr + char + sep
	file.write(infoStr+'\n')

def ReadSeperator(file, sep): #Reads file and seperates string using sep, returns list
	data = ReadFileLine(file)
	data.split(sep)
	return data

def WriteLine(file, info): #Writes line with \n included
	file.writelines(info + '\n')

def code_export_file(username):
    username_and_code=addRandom(username)
    file = open(User_Code_Directory(username+'code.txt'), 'w')
    file.writelines(username_and_code)

def read_code_from_file(username):
    try:
        file = open(User_Code_Directory(username+'code.txt'), 'r')
    except:
        code_export_file(username)
        read_code_from_file(username)
    else:
        username_and_code = ReadFileLine(file)
        return username_and_code
def addRandom(text):
    randlist=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R',
    'S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','0']
    for i in range(4):
       index=random.randint(0,len(randlist)-1)
       text+=randlist[index]
    return text
    
def hex_gen():
    file = open('color.txt', 'r')
    color_list=ReadFile(file)
    return color_list[random.randint(0,len(color_list)-1)]
#print(hex_gen())

def addRandom(text):
    randlist=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R',
    'S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','0']
    for i in range(4):
       index=random.randint(0,len(randlist)-1)
       text+=randlist[index]
    return text