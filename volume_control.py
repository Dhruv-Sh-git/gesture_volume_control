import cv2 as cv
import time
import numpy as np
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
cap=cv.VideoCapture(0)
#to set height and width of the cam
cap.set(3,480)
cap.set(4,480)
mpHands=mp.solutions.handspip 
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils
########################github
#from ctypes import cast, POINTER
#from comtypes import CLSTX_ALL
#from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#initialisations
devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))
#can be used sometimes
volume.GetMute()
volume.GetMasterVolumeLevel()
#volume range
volume.GetVolumeRange()
volRange=volume.GetVolumeRange()
#print(volume.GetVolumeRange())
#(-65.25, 0.0, 0.03125)found in print i.e volume level is from -65.25 to 0
#volume.SetMasterVolumeLevel(-20.0,None)
# use master volume after finalising
###############################
Vmin=volRange[0]
Vmax=volRange[1]
while True:
    success,img =cap.read()
    imgRGB=cv.cvtColor(img,cv.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                h,w,c =img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                
                # print(id,cx,cy)
                if id==4:
                    x1,y1=cx,cy
                    #print(id,x1,y1)
                    cv.circle(img,(x1,y1),12,(0,0,255),cv.FILLED)
                if id==8:
                    x2,y2=cx,cy
                    #print(id,x2,y2)
                    cv.circle(img,(x2,y2),12,(0,0,255),cv.FILLED)

                    cv.line(img,(x1,y1),(x2,y2),(0,0,250),3)
                    #midpoint
                    c1,c2=(x1+x2)//2,(y1+y2)//2
                    cv.circle(img,(c1,c2),12,(0,0,255),cv.FILLED)
                    length=math.hypot(x2-x1,y2-y1)
                    #print(length)#max=200,min=20 at approx 50cm hand range
                    vol=np.interp(length,[20,200],[Vmin,Vmax])
                    print(vol)
                    volume.SetMasterVolumeLevel(vol,None)


            mpDraw.draw_landmarks(img,handLms, mpHands.HAND_CONNECTIONS)
    cv.imshow("img",img)
    if cv.waitKey(20) & 0xff==ord('d'):
        break

cap.release()
cv.destroyAllWindows()