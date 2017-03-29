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

callbacks = {
      "getFileList": {"call": getFileList,  "parameters": "path",       "description": "Get file list in directory"},
      "writeFile":   {"call": writeFile,    "parameters": "path, data", "description": "Write data in file"}, 
      "getFile":     {"call": getFile,      "parameters": "path",       "description": "Get file data"},
      "deleteFile":  {"call": deleteFile,   "parameters": "path",       "description": "Delete specified file"}
      }
