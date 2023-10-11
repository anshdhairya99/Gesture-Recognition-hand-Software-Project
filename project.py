import cv2
import mediapipe as mp
import pyautogui
import time

def count_fingers(lst):
     
    count = 0
    thresh = (lst.landmark[0].y*100-lst.landmark[9].y*100)/2 

    if lst.landmark[5].y*100-lst.landmark[8].y*100 > thresh:
          count += 1
    if lst.landmark[9].y*100-lst.landmark[12].y*100 > thresh:
          count += 1
    if lst.landmark[13].y*100-lst.landmark[16].y*100 > thresh:
          count += 1
    if lst.landmark[17].y*100-lst.landmark[20].y*100 > thresh:
          count += 1
    if lst.landmark[5].x*100-lst.landmark[4].x*100 > 6:
          count += 1
    return count

cap = cv2.VideoCapture(0)

drawing = mp.solutions.drawing_utils
hands = mp.solutions.hands
hand_obj = hands.Hands(max_num_hands = 1)
FONT = cv2.FONT_HERSHEY_SIMPLEX

start_init = False

prev  = -1

while True:
    end_time = time.time()
    _, frm = cap.read()
    frm = cv2.flip(frm, 1) 
    frm = cv2.putText(frm, "Hand Gesture Recognition",(100, 40),
                      cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
    frm = cv2.putText(frm, "Frd:1, Rev:2, Vol Up:3, Vol Down:4, Play/Pause:5",(10, 450),
                      cv2.FONT_HERSHEY_COMPLEX, 0.75, (255,255,255), 2)

    res = hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

    if res.multi_hand_landmarks:
         
        hand_keyPoints = res.multi_hand_landmarks[0]

        count = count_fingers(hand_keyPoints)

        if not (prev == count):
            if not (start_init):
                start_time = time.time()
                start_init = True

            elif (end_time-start_time) > 0.2:

                if (count == 1):
                    cv2.putText(frm, "Forward..",(5, 50), FONT, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
                    pyautogui.press("right")

                elif (count == 2):
                    cv2.putText(frm, "Reverse..",(5, 50), FONT, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
                    pyautogui.press("left")

                elif (count == 3):
                    cv2.putText(frm, "Volume Up..",(5, 50), FONT, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
                    pyautogui.press("up")

                elif (count == 4):
                    cv2.putText(frm, "Volume Down..",(5, 50), FONT, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
                    pyautogui.press("down")

                elif (count == 5):
                    cv2.putText(frm, "Play/Pause..",(5, 50), FONT, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
                    pyautogui.press("space")

                prev = count
                start_init = False
        
        drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS)

    cv2.imshow("window", frm)   
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break