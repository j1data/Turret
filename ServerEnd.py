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
degh = 100
degv = 100
deghNEW = 100
degvNEW = 100

def detect(frame,degh,degv,deghNEW,degvNEW):
    bounding_box_cordinates, weights =  HOGCV.detectMultiScale(frame, winStride = (4, 4), padding = (8, 8), scale = 1.03)
    
    potPerson = 1
    person = 1
    for x,y,w,h in bounding_box_cordinates:
        if weights[potPerson-1] >= .4:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            cv2.putText(frame, f'person {person}', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
            print(weights[potPerson-1])
            print(str(x) + "," + str(y) + "," + str(w) + "," + str(h))
            center = [(x+(w/2)),(y+(h/2))]
            print(center)
            diff = [math.floor(center[0]) - 320/2, math.floor(center[1]) - 200/2]
            cv2.circle(frame, (math.floor(center[0]),math.floor(center[1])),10,(255,0,0),2)
            cv2.circle(frame, (160,100),10,(0,0,255),2)
            time.sleep(0.5)
            print(diff)
            if math.floor(diff[0]) < -30 :
                deghNEW = degh - 5
            elif math.floor(diff[0]) > 30 :
                deghNEW = degh + 5

            if math.floor(diff[1]) < -10 :
                degvNEW = degv + 1
            elif math.floor(diff[1]) > 10 :
                degvNEW = degv - 1
            
            if deghNEW < 40 :
                deghNEW = 40
            elif deghNEW > 170 :
                deghNEW = 170
            if degvNEW < 70 :
                degvNEW = 70
            elif degvNEW > 170 :
                degvNEW = 170
            
            if deghNEW != degh:
                degh = deghNEW
                degv = degvNEW
                data = (str(degv) + "," + str(degh))
                c.send(data.encode())
                time.sleep(1)
                
            diff = []
            person += 1
        potPerson += 1
    #cv2.putText(frame, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    #cv2.putText(frame, f'Total Persons : {person-1}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    cv2.imshow('output', frame)

    return frame,degh,degv,deghNEW,degvNEW

def humanDetector(path,degh,degv,deghNEW,degvNEW):
        print('[INFO] Opening Web Cam.')
        degh,degv,deghNEW,degvNEW = detectByCamera(path,degh,degv,deghNEW,degvNEW)
        return degh,degv,deghNEW,degvNEW

def detectByCamera(path,degh,degv,deghNEW,degvNEW):   
    video = cv2.VideoCapture(path)
    print('Detecting people...')
    

    while True:
        check, frame = video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame, (320,200), interpolation = cv2.INTER_AREA)
        frame,degh,degv,deghNEW,degvNEW = detect(frame,degh,degv,deghNEW,degvNEW)

        key = cv2.waitKey(1)
        if key == ord('q'):
                break

    video.release()
    cv2.destroyAllWindows()

    return degh,degv,deghNEW,degvNEW

s.bind((host, port))
s.listen(5)


while True:
    c, addr = s.accept()
    print('got a connection from addr', addr)
    HOGCV = cv2.HOGDescriptor()
    HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    degh,degv,deghNEW,degvNEW = humanDetector("http://192.168.1.102:8081/video",degh,degv,deghNEW,degvNEW)
    c.close()
   
