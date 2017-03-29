# Simple function, no returning values
def printValue(arg):
    # Use variable here to name inocming elements from array
    someParameter = arg[0]
    print(someParameter)

# Function with returning value and error checking
def summing(arg):
    a = arg[0]
    b = arg[1]
    c = None
    try :
        c = a+b
        return c
    except :
        # This message will be sent in error topic
        raise Exception("Parameters must be numbers!")

# Declare callbacks here for two functions and describe them
callbacks = {
      "printValue":  {"call": printValue,  "parameters": "value",          "description": "Print value in micropython console"},
      "summing":     {"call": summing,     "parameters": "valueA, valueB", "description": "Make sum of valueA + valueB"}
      }
