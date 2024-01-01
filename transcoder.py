import cv2
import numpy as np
import os

def pixellength(size): #Basic bit flipping with 256 instead of 2
    counter2, counter1 = divmod(size, 256)
    counter3, counter2 = divmod(counter2, 256)
    counter4, counter3 = divmod(counter3, 256)
    counter5, counter4 = divmod(counter4, 256)
    if counter5 > 255:
            print("WTF") # 255^5 is a massive number who on earth.
            exit()
    return [counter5, counter4, counter3, counter2, counter1]

def valuetonumber(list): # Opposite of pixellength function.
    return list[0]*np.power(256,4)+list[1]*np.power(256,3)+list[2]*np.power(256,2)+list[3]*256+list[4]

def encode(data): #Encodes the data from an array.
    #Declaring Variables
    values = []
    out = []
    counter = 0
    last = 0
    #Creating shape using normal python lists
    for x in data:
        values.append(x)
        counter += 1
        if counter % 3 == 0:
            out.append(values)
            counter = 0
            values = []
    #Dealing with edge cases
    if len(values) == 1:
        out.append([values[0],0,0])
        last = 2
    elif len(values) == 2:
        out.append([values[0],values[1],0])
        last = 1
    length = len(out)
    return out, length, last

def decode(path): #Decodes data from a image file.
    array = np.reshape(cv2.imread(path),-1)
    #Seperating real data from information added at the begining.
    data = array[69:]
    pre = array[:69]
    
    #Special Inserted data required before real data.
    name = ''.join([chr(i) for i in np.trim_zeros(pre[:64])])
    zeros = valuetonumber(pre[64:])
    endofdata = len(data) - zeros
    #Bytes data type is used as it is dealing with binary data.
    data = data[:endofdata]
    text = bytearray(data)
    return text, name

def writeimage(path): #Uses encode function to create a image.
    with open(path,"rb") as f:
        data = np.fromfile(f, dtype=np.uint8)
    arr, length, last = encode(data)
    output = np.array(arr)
    #Limit File name Length
    filename = os.path.split(path)[-1]
    if len(filename) > 64:
        filename = filename[:30] + filename[-3:]
    name = np.fromstring(filename, dtype=np.uint8)
    name = np.append(name,np.zeros((64-len(name)),dtype=int))
    length = length + 23
    #Calculating a optimal image size for array length.
    x = int(np.ceil(4/3 * np.sqrt(length)))
    y = int(round((9*x)/16,0))
    size = x*y - length
    if size < 0:
        y = int(np.ceil((9*x)/16))
        size = x*y - length
    #Begining Data and Ending Zeros
    print(size*3+last)
    end = np.array(pixellength(size*3+last))
    pre = np.append(name,end)
    #Adding all the Arrays together.
    output = np.append(output, np.empty((size,3)))
    output = np.append(pre,output)
    image = np.array(output).reshape(y,x,3)
    #Writing the image array to a image.
    cv2.imwrite("data.png",image)

def dumb_decode(path): #dumb version of above decoder, only really for debugging.
    data = np.reshape(cv2.imread(path),-1)
    text = bytearray(data)
    return text

def decodeimage(path): #Writes the data from the encoded image into the original format.
    data, name = decode(path)
    with open(name,"wb") as outfile:
        outfile.write(data)
