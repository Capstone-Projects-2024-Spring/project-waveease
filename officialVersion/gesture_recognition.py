import cv2
import mediapipe as mp
import numpy as np
#import pyautogui #using directinput to allow more application access
import pydirectinput as pyautogui
import configparser

from .draw_utiles import draw_landmarks_on_image

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

#here data from config.ini should be accessed that will change button pressed based on saved hotkey
gestures = [
    'volumeup',
    'volumedown',
    'w',
    's',
    'ctrl'
]


# Create a gesture recognizer instance with the live stream mode:
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    print('gesture recognition result: {}' + format(result))


model_path = 'officialVersion/own_trained_02.task'
base_options = BaseOptions(model_asset_path=model_path)
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO
)
recognizer = GestureRecognizer.create_from_options(options)

cap = cv2.VideoCapture(0)
previous_position = None
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils


def draw_progress_bar(img, value, max_value, text, pos, bar_color=(0, 255, 0), text_color=(255, 255, 255)):
    x, y, w, h = pos
    # draw the background
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), -1)
    # draw the progress bar
    bar_width = int((value / max_value) * w)
    cv2.rectangle(img, (x, y), (x + bar_width, y + h), bar_color, -1)
    # put the text
    cv2.putText(img, f'{text}: {value:.2f}', (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)

def load_hotkey(): #load from config file
    try:
        config = configparser.ConfigParser()
        config.read('officialVersion/config.ini')
        gestures[0] = config.get('hotkey', 'value')
        gestures[1] = config.get('hotkey2', 'value')
        gestures[2] = config.get('hotkey3', 'value')
        gestures[3] = config.get('hotkey4', 'value')
        gestures[4] = config.get('hotkey5', 'value')
    except Exception as e:
        print('Error loading config, try saving settings first', f'fail {str(e)}')

def start():
    load_hotkey()
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        gesture_recognition_result = recognizer.recognize_for_video(mp_image, int(cap.get(cv2.CAP_PROP_POS_MSEC)))

        if gesture_recognition_result.gestures:
            print(gesture_recognition_result.gestures[0][0].category_name)
            draw_progress_bar(frame, gesture_recognition_result.gestures[0][0].score, 1.0,
                              gesture_recognition_result.gestures[0][0].category_name, (50, 50, 200, 20))
            frame = draw_landmarks_on_image(frame, gesture_recognition_result)
            print('gesture recognition result: {}' + format(gesture_recognition_result))
            if gesture_recognition_result.gestures[0][0].category_name == 'Pointing_up':
                pyautogui.press(gestures[0])
                cv2.putText(frame, gestures[0], (250, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (50, 200, 150), 3)
            elif gesture_recognition_result.gestures[0][0].category_name == 'pointing_down':
                pyautogui.press(gestures[1])
                cv2.putText(frame, gestures[1], (250, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (50, 200, 150), 3)
            
            elif gesture_recognition_result.gestures[0][0].category_name == 'pinkyThumb':
                pyautogui.keyDown(gestures[2])
                cv2.putText(frame, gestures[2], (250, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (50, 200, 150), 3)
            elif gesture_recognition_result.gestures[0][0].category_name == 'three':
                pyautogui.keyDown(gestures[3])
                cv2.putText(frame, gestures[3], (250, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (50, 200, 150), 3)
            elif gesture_recognition_result.gestures[0][0].category_name == 'four':
                pyautogui.keyDown(gestures[4])
                cv2.putText(frame, gestures[4], (250, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (50, 200, 150), 3)
            elif gesture_recognition_result.gestures[0][0].category_name == 'Yeah':
                print("YEAHHHHHHH no gesture map......... yet")
            elif gesture_recognition_result.gestures[0][0].category_name == 'index_pinky':
                print("no action my love")
            
            elif gesture_recognition_result.gestures[0][0].category_name == 'palm':
                pyautogui.keyUp(gestures[0])
                pyautogui.keyUp(gestures[1])
                pyautogui.keyUp(gestures[2])
                pyautogui.keyUp(gestures[3])
                pyautogui.keyUp(gestures[4])
            
            else :
                pyautogui.keyUp(gestures[0])
                pyautogui.keyUp(gestures[1])
                pyautogui.keyUp(gestures[2])
                pyautogui.keyUp(gestures[3])
                pyautogui.keyUp(gestures[4])
                

        cv2.imshow('Camera Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    start()
