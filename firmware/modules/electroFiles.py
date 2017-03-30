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
    if (is_binary(name) is True):
        raise Exception("Oups! This is a binary file. Only text files are allowed!")
    else :
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

def is_binary(filename):
    """Return true if the given filename is binary.
    @raise EnvironmentError: if the file does not exist or cannot be accessed.
    @attention: found @ http://bytes.com/topic/python/answers/21222-determine-file-type-binary-text on 6/08/2010
    @author: Trent Mick <TrentM@ActiveState.com>
    @author: Jorge Orpinel <jorge@orpinel.com>"""
    fin = open(filename, 'rb')
    try:
        CHUNKSIZE = 1024
        while 1:
            chunk = fin.read(CHUNKSIZE)
            if '\0' in chunk: # found null byte
                return True
            if len(chunk) < CHUNKSIZE:
                break # done
    # A-wooo! Mira, python no necesita el "except:". Achis... Que listo es.
    finally:
        fin.close()

    return False

callbacks = {
      "getFileList": {"call": getFileList,  "parameters": "path",       "description": "Get file list in directory"},
      "writeFile":   {"call": writeFile,    "parameters": "path, data", "description": "Write data in file"}, 
      "getFile":     {"call": getFile,      "parameters": "path",       "description": "Get file data"},
      "deleteFile":  {"call": deleteFile,   "parameters": "path",       "description": "Delete specified file"}
      }
