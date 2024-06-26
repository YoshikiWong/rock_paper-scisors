import cv2
import random as rd
import time as tm
import mediapipe as mp

print (cv2.__version__)
evt =0
font=cv2.FONT_HERSHEY_SIMPLEX
fontColor=(0,0,255)
fontSize=.2
fontThick=1
rnum =4

def mouseClick(event,xPos,yPos,flags,params):
    global evt
    global pnt
    if (event == cv2.EVENT_LBUTTONDOWN):
        #print("Mouse event was:",event)
        #print("at Position: ",xPos,yPos)
        evt =event
        pnt = (xPos,yPos)
    if (event == cv2.EVENT_LBUTTONUP):
        #print("Mouse event was:",event)
        #print("at Position: ",xPos,yPos)
        evt = event
        pnt = (xPos,yPos)
    if event ==cv2.EVENT_RBUTTONUP:
        #print("Right button up:  ",event)
        pnt = (xPos,yPos)
        evt = event

class mpHands:
    import mediapipe as mp
    def __init__(self,maxHands=2,tol1=.5,tol2=.5):
        self.hands=self.mp.solutions.hands.Hands(False,maxHands,tol1,tol2)
    def Marks(self,frame):
        myHands=[]
        handsType=[]
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            #print(results.multi_handedness)
            for hand in results.multi_handedness:
                #print(hand)
                #print(hand.classification)
                #print(hand.classification[0])
                handType=hand.classification[0].label
                handsType.append(handType)
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width),int(landMark.y*height)))
                myHands.append(myHand)
        return myHands,handsType
        
    

width =1000
height=500

cam =cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*"MJPG"))

findHands=mpHands(2)
SaveEvt =0

cv2.namedWindow("my WEBcam")
cv2.setMouseCallback("my WEBcam",mouseClick)
while True:
    ignore, frame = cam.read()
    handsLM,handsType=findHands.Marks(frame)
    
    cv2.rectangle(frame,(800,50),(900,90),(0,255,0),-1)
    cv2.putText(frame,"Play",(800,80),font,1,(255,0,0),2)
    
    if evt == 1:
        saveEvt = evt
        print(evt)
        if(pnt[0]>800 and pnt[0]<900 and pnt[1]>50 and pnt[1>90]):
            cv2.rectangle(frame,(800,50),(900,90),(0,0,255),-1)
            cv2.putText(frame,"Play",(800,80),font,1,(255,0,0),2)
            rnum = rd.randint(0, 2)
            print(rnum)
            state ="dont know"

            #rock =0 paper =1 scissors =2

                


    for numHands in range(0,len(handsLM),1):
        for HandPoints in range(0,len(handsLM[numHands]),1):
            cv2.circle(frame,handsLM[numHands][HandPoints],10,(0,0,255),3)
        if(handsLM[numHands][8][1] >= handsLM[numHands][5][1] and handsLM[numHands][16][1] >= handsLM[numHands][13][1] and handsLM[numHands][20][1] >= handsLM[numHands][17][1]and handsLM[numHands][12][1] <= handsLM[numHands][9][1] and handsLM[numHands][4][0] <= handsLM[numHands][3][0]):
            cv2.putText(frame,"forbidden finger!!",(0,50),font,2,fontColor,2)


            cv2.rectangle(frame,(handsLM[numHands][3][0],handsLM[numHands][12][1]),(handsLM[numHands][17][0],handsLM[numHands][0][1]),(0,0,0),-1)

            
        if(handsLM[numHands][4][1] <= handsLM[numHands][1][1] and handsLM[numHands][8][1] <= handsLM[numHands][5][1] and handsLM[numHands][12][1] <= handsLM[numHands][9][1] and handsLM[numHands][16][1] <= handsLM[numHands][13][1] and handsLM[numHands][20][1] <= handsLM[numHands][17][1]):
            cv2.putText(frame,"paper",(0,50),font,2,fontColor,2)
            if rnum ==0:
                cv2.putText(frame,"paper vs rock: You win ",(0,50),font,2,fontColor,2)
                state = "paper vs rock: You win"
            if rnum ==1:
                cv2.putText(frame,"paper vs paper: Its a tie ",(0,50),font,2,fontColor,2)
            if rnum ==2:
                cv2.putText(frame,"paper vs scissors: You lost ",(0,50),font,2,fontColor,2)

        if(handsLM[numHands][4][0] <= handsLM[numHands][3][0] and handsLM[numHands][8][1] >= handsLM[numHands][5][1] and handsLM[numHands][12][1] >= handsLM[numHands][9][1] and handsLM[numHands][16][1] >= handsLM[numHands][13][1] and handsLM[numHands][20][1] >= handsLM[numHands][17][1]):
            cv2.putText(frame,"rock",(0,50),font,2,fontColor,2)
            if rnum ==0:
                cv2.putText(frame,"rock vs rock: Its a tie ",(0,50),font,2,fontColor,2)
            if rnum ==1:
                cv2.putText(frame,"rock vs paper: You lost ",(0,50),font,2,fontColor,2)
            if rnum ==2:
                cv2.putText(frame,"rock vs scissors: You win ",(0,50),font,2,fontColor,2)

        if(handsLM[numHands][4][0] <= handsLM[numHands][3][0] and handsLM[numHands][8][1] <= handsLM[numHands][5][1] and handsLM[numHands][12][1] <= handsLM[numHands][9][1] and handsLM[numHands][16][1] >= handsLM[numHands][13][1] and handsLM[numHands][20][1] >= handsLM[numHands][17][1]):
            cv2.putText(frame,"scissors",(0,50),font,2,fontColor,2)
            if rnum ==0:
                cv2.putText(frame,"scissors vs rock: You lost ",(0,50),font,2,fontColor,2)
            if rnum ==1:
                cv2.putText(frame,"scissors vs paper: You win ",(0,50),font,2,fontColor,2)
            if rnum ==2:
                cv2.putText(frame,"scissors vs scissors: Its a tie ",(0,50),font,2,fontColor,2)
    
    cv2.imshow("my WEBcam", frame)
    cv2.moveWindow("my WEBcam",0,0)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cam.release()