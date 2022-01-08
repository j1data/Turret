import socket
import cv2
import time
import imutils
import numpy as np
import argparse
import math
s = socket.socket()
host = "192.168.1.106"
port = 57445
degh = 150
degv = 92



s.bind((host, port))
s.listen(5)


c, addr = s.accept()
print('got a connection from addr', addr)

data = (str(degv) + "," + str(degh))
c.send(data.encode())
time.sleep(1)

c.close()
   