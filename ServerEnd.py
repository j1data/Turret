import socket
import cv2
import time
import imutils
import numpy as np
import argparse
import math
s = socket.socket()
host = "192.168.1.129"
port = 57445

def detect(frame):
    bounding_box_cordinates, weights =  HOGCV.detectMultiScale(frame, winStride = (4, 4), padding = (8, 8), scale = 1.03)
    
    potPerson = 1
    person = 1
    for x,y,w,h in bounding_box_cordinates:
        if weights[potPerson-1] >= .4:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            cv2.putText(frame, f'person {person}', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
            print(weights[potPerson-1])
            center = [(x+w)/2,(y+h)/2]
            diff = [center[0] - 320/2, center[1] - 200/2]
            time.sleep(1)
            diff[0] = math.floor(diff[0])
            diff[1] = math.floor(diff[1])
            data = (str(diff[0]) + "," + str(diff[1]))
            c.send(data.encode())
            time.sleep(1)
            diff = []
            person += 1
        potPerson += 1
    
    
    #cv2.putText(frame, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    #cv2.putText(frame, f'Total Persons : {person-1}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    cv2.imshow('output', frame)

    return frame

def humanDetector(path):
        print('[INFO] Opening Web Cam.')
        detectByCamera(path)

def detectByCamera(path):   
    video = cv2.VideoCapture(path)
    print('Detecting people...')

    while True:
        check, frame = video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame, (320,200), interpolation = cv2.INTER_AREA)
        frame = detect(frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
                break

    video.release()
    cv2.destroyAllWindows()

s.bind((host, port))
s.listen(5)


while True:
    c, addr = s.accept()
    print('got a connection from addr', addr)
    HOGCV = cv2.HOGDescriptor()
    HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    humanDetector("http://192.168.1.102:8081/video")
    c.close()
   
