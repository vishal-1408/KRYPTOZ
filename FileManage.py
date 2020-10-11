import os, random

homedir=os.path.expanduser('~') + '/AppData/Roaming/ChatApp/' 

def Return_App_Path(filename): #This returns app directory 
    global homedir
    if os.path.isdir(homedir):
        return homedir + filename
    else:
        os.makedirs(homedir)
        return homedir + filename
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

def hex_gen():
    hexdigits = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    red = hexdigits[random.randint(0,15)] + hexdigits[random.randint(0,15)]
    blue = hexdigits[random.randint(0,15)] + hexdigits[random.randint(0,15)]
    green = hexdigits[random.randint(0,15)] + hexdigits[random.randint(0,15)]
    return '#'+red+green+blue
print(hex_gen())