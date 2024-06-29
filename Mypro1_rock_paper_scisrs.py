import cv2
import random as rd
import mediapipe as mp

def mouseClick(event, xPos, yPos, flags, params):
    global evt, pnt
    if event in [cv2.EVENT_LBUTTONDOWN, cv2.EVENT_LBUTTONUP, cv2.EVENT_RBUTTONUP]:
        evt = event
        pnt = (xPos, yPos)

class mpHands:
    def __init__(self, maxHands=2, tol1=0.5, tol2=0.5):
        self.hands = mp.solutions.hands.Hands(False, maxHands, tol1, tol2)

    def Marks(self, frame):
        myHands, handsType = [], []
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frameRGB)
        if results.multi_hand_landmarks:
            for hand in results.multi_handedness:
                handsType.append(hand.classification[0].label)
            for handLandMarks in results.multi_hand_landmarks:
                myHand = [(int(lm.x * width), int(lm.y * height)) for lm in handLandMarks.landmark]
                myHands.append(myHand)
        return myHands, handsType

def is_rock(hand):
    return (
        hand[8][1] >= hand[6][1] and hand[12][1] >= hand[10][1] and
        hand[16][1] >= hand[14][1] and hand[20][1] >= hand[18][1]
    )

def is_paper(hand):
    return (
        hand[8][1] <= hand[6][1] and hand[12][1] <= hand[10][1] and
        hand[16][1] <= hand[14][1] and hand[20][1] <= hand[18][1]
    )

def is_scissors(hand):
    return (
        hand[8][1] <= hand[6][1] and hand[12][1] <= hand[10][1] and
        hand[16][1] >= hand[14][1] and hand[20][1] >= hand[18][1]
    )

def is_forbidden_finger(hand):
    return (
        hand[8][1] >= hand[6][1] and hand[12][1] <= hand[10][1] and
        hand[16][1] >= hand[14][1] and hand[20][1] >= hand[18][1]
    )

width, height = 1000, 500
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

findHands = mpHands(2)
evt, saveEvt, rnum = 0, 0, 4
font, fontColor, fontSize, fontThick = cv2.FONT_HERSHEY_SIMPLEX, (0, 0, 255), .2, 1

cv2.namedWindow("my WEBcam")
cv2.setMouseCallback("my WEBcam", mouseClick)

while True:
    ignore, frame = cam.read()
    handsLM, handsType = findHands.Marks(frame)

    cv2.rectangle(frame, (800, 50), (900, 90), (0, 255, 0), -1)
    cv2.putText(frame, "Play", (800, 80), font, 1, (255, 0, 0), 2)

    if evt == 1:
        saveEvt = evt
        if 800 < pnt[0] < 900 and 50 < pnt[1] < 90:
            cv2.rectangle(frame, (800, 50), (900, 90), (0, 0, 255), -1)
            cv2.putText(frame, "Play", (800, 80), font, 1, (255, 0, 0), 2)
            rnum = rd.randint(0, 2)
            state = "dont know"

    for numHands in range(len(handsLM)):
        hand = handsLM[numHands]
        for HandPoints in range(len(hand)):
            cv2.circle(frame, hand[HandPoints], 10, (0, 0, 255), 3)

        if is_forbidden_finger(hand):
            cv2.putText(frame, "forbidden finger!!", (50, 50), font, 2, fontColor, 2)
            cv2.rectangle(frame, (hand[3][0], hand[12][1]), (hand[17][0] , hand[0][1]), (0, 0, 0), -1)
            

        elif is_paper(hand):
            cv2.putText(frame, "paper", (50, 50), font, 2, fontColor, 2)
            if rnum == 0:
                cv2.putText(frame, "paper vs rock: You win", (50, 100), font, 2, fontColor, 2)
            elif rnum == 1:
                cv2.putText(frame, "paper vs paper: It's a tie", (50, 100), font, 2, fontColor, 2)
            elif rnum == 2:
                cv2.putText(frame, "paper vs scissors: You lost", (50, 100), font, 2, fontColor, 2)
        elif is_rock(hand):
            cv2.putText(frame, "rock", (50, 50), font, 2, fontColor, 2)
            if rnum == 0:
                cv2.putText(frame, "rock vs rock: It's a tie", (50, 100), font, 2, fontColor, 2)
            elif rnum == 1:
                cv2.putText(frame, "rock vs paper: You lost", (50, 100), font, 2, fontColor, 2)
            elif rnum == 2:
                cv2.putText(frame, "rock vs scissors: You win", (50, 100), font, 2, fontColor, 2)
        elif is_scissors(hand):
            cv2.putText(frame, "scissors", (50, 50), font, 2, fontColor, 2)
            if rnum == 0:
                cv2.putText(frame, "scissors vs rock: You lost", (50, 100), font, 2, fontColor, 2)
            elif rnum == 1:
                cv2.putText(frame, "scissors vs paper: You win", (50, 100), font, 2, fontColor, 2)
            elif rnum == 2:
                cv2.putText(frame, "scissors vs scissors: It's a tie", (50, 100), font, 2, fontColor, 2)

    cv2.imshow("my WEBcam", frame)
    cv2.moveWindow("my WEBcam", 0, 0)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
