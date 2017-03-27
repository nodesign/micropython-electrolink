import os

def getFileList(arg):
    path = arg[0]
    return os.listdir(path)

def writeFile(arg):
    name = arg[0]
    data = arg[1]
    try :
        f = open(name, "w")
        f.write(data)
        f.close()
        return "OK"
    except :
        raise Exception("File can't be written")

def getFile(arg):
    name = arg[0]
    f = open(name, "r")
    data = f.read()
    f.close()
    return data

def deleteFile(arg):
    name = arg[0]
    try :
        os.remove(name)
        return "OK"
    except :
        raise Exception("File don't exist or can't be removed")

spells = {
      "getFileList": getFileList, 
      "writeFile": writeFile, 
      "getFile": getFile,
      "deleteFile": deleteFile}