import transcoder
import numpy as np
import os 
import cv2
import streamlit as st

st.title("Transcoding Tool")
encoding, decoding = st.tabs(["Encoding","Decoding"])

with encoding:
    f = st.file_uploader("Choose any file", accept_multiple_files=False,key="encoding")
    if f is not None:
        path = f.name
        file = f.getbuffer()
        data = np.frombuffer(file, dtype=np.uint8)
        arr, length, last = transcoder.encode(data)
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
        end = np.array(transcoder.pixellength(size*3+last))
        pre = np.append(name,end)
        #Adding all the Arrays together.
        output = np.append(output, np.empty((size,3)))
        output = np.append(pre,output)
        image = np.array(output).reshape(y,x,3)
        #Writing the image array to a image.
        cv2.imwrite("data.png",image)
        st.image("data.png",output_format="PNG")
        with open("data.png", "rb") as f:
            st.download_button("Download Image",f,"data.png")

with decoding:
    f = st.file_uploader("Choose any file", accept_multiple_files=False,key="decoding")
    if f is not None:
        file = np.frombuffer(f.getbuffer(),dtype=np.uint8)
        array = np.reshape(cv2.imdecode(file, cv2.IMREAD_COLOR),-1)
        #Seperating real data from information added at the begining.
        data = array[69:]
        pre = array[:69]
        
        #Special Inserted data required before real data.
        name = ''.join([chr(i) for i in np.trim_zeros(pre[:64])])
        zeros = transcoder.valuetonumber(pre[64:])
        endofdata = len(data) - zeros
        #Bytes data type is used as it is dealing with binary data.
        data = data[:endofdata]
        text = bytearray(data)
        st.download_button("Download Here", bytes(text),file_name=name)