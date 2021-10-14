import numpy as np
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

def read_tiq(path):

    f = open(path,'rb')

    #メタデータの読み込み
    str_lines=''

    while True:
        line = f.readline()
        line_str = line.decode('utf-8')

        str_lines += line_str
        if ("</Setup>" in line_str):
            str_lines += "</DataFile>"
            f.seek(13, 1)
            break

    root = ET.fromstring(str_lines)


    for i in root.iter(tag='Scaling'):
       scale=float(i.text)
    print(i.tag,"=",scale)


    #バイナリデータの読み込み
    bytes_data = f.read()
    f.close()

    #バイナリデータのデコード
    #I(0),Q(0),I(1),Q(1)のようにint16型のデータが並んでいる.
    dtype = np.dtype([('I', np.int16), ('Q', np.int16)])
    dtype=dtype.newbyteorder('<')
    int_data = np.frombuffer(bytes_data, dtype=dtype)


    I=int_data["I"]*scale
    Q=int_data["Q"]*scale


    return (I,Q)


import time


I,Q=read_tiq(r"C:\Users\ttten\Documents\data\1-2020.07.21.17.15.01.648.tiq")


p2=(I**2)+(Q**2)
p2log=10*np.log10(10*p2)

print(p2[:20])

"""
plt.plot(p2log[:100000])
plt.show()
"""
