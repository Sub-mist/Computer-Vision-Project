import cv2
import mediapipe as mp
import pyautogui
import random
import screen_brightness_control as sbc
import util
from pynput.mouse import Button, Controller

mouse = Controller()
screen_width, screen_height = pyautogui.size()

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)


def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]  # Assuming only one hand is detected
        index_finger_tip = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
        return index_finger_tip
    return None, None


def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y / 2 * screen_height)
        pyautogui.moveTo(x, y)


def left_click(landmark_list, thumb_index_dist):
    result = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and thumb_index_dist > 50
    return result


def right_click(landmark_list, thumb_index_dist):
    result = util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90  and thumb_index_dist > 50
    return result
    
  

def double_click(landmark_list, thumb_index_dist):    
    result = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and thumb_index_dist > 50
    return result

def control_volume(landmark_list):
    repeat = util.get_distance([landmark_list[7], landmark_list[11]]) < 50
    result = "Up" if (util.get_distance([landmark_list[4], landmark_list[16]]) > 100 and util.get_distance([landmark_list[4], landmark_list[16]]) < 130 and repeat ) else "Down" if (util.get_distance([landmark_list[4], landmark_list[16]]) < 50 and repeat ) else False
    return result

def control_brightness(landmark_list):
    repeat = util.get_distance([landmark_list[7], landmark_list[11]]) < 50
    result = util.get_distance([landmark_list[4], landmark_list[20]])  
    brightness = sbc.get_brightness(display=0)[0]
    return (
        "Up" if (result > 100 and result <140 and repeat and brightness < 100) else "Down" if (result < 40 and brightness > 10 and repeat) else False
    )
    

def screenshot(landmark_list, thumb_index_dist):
    result = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and thumb_index_dist < 50
    return result


def detect_gesture(frame, landmark_list, processed):
    if len(landmark_list) >= 21:

        index_finger_tip = find_finger_tip(processed)
        thumb_index_dist = util.get_distance([landmark_list[4], landmark_list[5]])
        brightness = sbc.get_brightness(display=0)[0]

        if util.get_distance([landmark_list[4], landmark_list[5]]) < 50  and util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90:
            move_mouse(index_finger_tip)
        elif left_click(landmark_list,  thumb_index_dist):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif right_click(landmark_list, thumb_index_dist):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif double_click(landmark_list, thumb_index_dist):
            pyautogui.doubleClick()
            cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        elif screenshot(landmark_list,thumb_index_dist ):
            im1 = pyautogui.screenshot()
            label = random.randint(1, 1000)
            im1.save(f'my_screenshot_{label}.png')
            cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        elif control_volume(landmark_list) == "Up":
            pyautogui.press("volumeup") 
            cv2.putText(frame, "Volume Up", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif control_volume(landmark_list) =="Down":
            pyautogui.press("volumedown")
            cv2.putText(frame, "Volume Down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif control_brightness(landmark_list) == "Up":
            sbc.set_brightness(brightness + 10)
            cv2.putText(frame, "Brightness Inc...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif control_brightness(landmark_list) == "Down":
            sbc.set_brightness(brightness - 10)
            cv2.putText(frame, "Brightness Dec...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


def main():
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)             # contains detection results, including hand landmarks

            landmark_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]  # Assuming only one hand is detected
                # draw.draw_landmarks() to draw dots on each landmark and lines connecting them
                # mpHands.HAND_CONNECTIONS provides predefined landmark connections.
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)                
                for lm in hand_landmarks.landmark:
                    landmark_list.append((lm.x, lm.y))

            detect_gesture(frame, landmark_list, processed)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()




