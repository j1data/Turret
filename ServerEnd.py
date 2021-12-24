import socket
import cv2
import time
s = socket.socket()
host = "192.168.1.129"
port = 57445
#face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
#cap = cv2.VideoCapture('http://192.168.1.136:8081/%27)
#cap = cv2.VideoCapture(0)
s.bind((host, port))
s.listen(5)
#data = "0,180"

while True:
    #ret, frame = cap.read()
        #frame = cv2.resize(frame, (640,480), interpolation = cv2.INTER_AREA)
        #frame = cv2.flip(frame,1)
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('img',frame)
    #time.sleep(5)
    #faces = face_cascade.detectMultiScale(gray,1.3,5)
    #for x,y,w,h in faces:
        #string = 'X{0:d}Y{1:d}'.format((x+w//2),(y+h//2))
        #print(string)
        #cv2.circle(frame,(x+w//2,y+h//2),2,(0,255,0),2)
        #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
    #cv2.rectangle(frame,(640//2-30,480//2-30),(640//2+30,480//2+30),(255,255,255),3)
    #cv2.imshow('img',frame)

    data = input("input '#,#'")

    if data == "no":
        break

    c, addr = s.accept()
    print('got a connection from addr', addr)
    c.send(data.encode())
    c.close()

    #if cv2.waitKey(10)&0xFF == ord('q'):
        #break
#cap.release()
#cv2.destroyAllWindows()