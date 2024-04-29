import queue
import threading

import cv2
import mediapipe as mp
import numpy as np
import pyautogui  # using directinput to allow more application access
import pydirectinput as pyautogui2
import configparser

from .draw_utiles import draw_landmarks_on_image


# def _print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
#     print('gesture recognition result: {}' + format(result))


def draw_progress_bar(img, value, max_value, text, pos, bar_color=(0, 255, 0), text_color=(255, 255, 255)):
    x, y, w, h = pos
    # draw the background
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), -1)
    # draw the progress bar
    bar_width = int((value / max_value) * w)
    cv2.rectangle(img, (x, y), (x + bar_width, y + h), bar_color, -1)
    # put the text
    cv2.putText(img, f'{text}: {value:.2f}', (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)


class GestureRecognition:
    def __init__(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands
        BaseOptions = mp.tasks.BaseOptions
        GestureRecognizer = mp.tasks.vision.GestureRecognizer
        GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
        VisionRunningMode = mp.tasks.vision.RunningMode

        # here data from config.ini should be accessed that will change button pressed based on saved hotkey
        self.gestures = [
            'volumeup',
            'volumedown',
            'w',
            's',
            'ctrl'
        ]

        model_path = 'officialVersion/own_trained_02.task'
        self.base_options = BaseOptions(model_asset_path=model_path)
        self.options = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.VIDEO
        )
        self.recognizer = GestureRecognizer.create_from_options(self.options)

        self.previous_position = None
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils

        self.gesture_queue = queue.Queue()

    # Create a gesture recognizer instance with the live stream mode:

    def _load_hotkey(self):  # load from config file
        try:
            config = configparser.ConfigParser()
            config.read('officialVersion/config.ini')
            self.gestures[0] = config.get('hotkey', 'value')
            self.gestures[1] = config.get('hotkey2', 'value')
            self.gestures[2] = config.get('hotkey3', 'value')
            self.gestures[3] = config.get('hotkey4', 'value')
            self.gestures[4] = config.get('hotkey5', 'value')
        except Exception as e:
            print('Error loading config, try saving settings first', f'fail {str(e)}')

    frames = None

    def start(self):
        last_key = None
        cap = cv2.VideoCapture(0)
        self._load_hotkey()
        while True:
            success, frame = cap.read()
            if not success:
                print("Start up failed")
                break

            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

            gesture_recognition_result = self.recognizer.recognize_for_video(mp_image,
                                                                             int(cap.get(cv2.CAP_PROP_POS_MSEC)))

            if gesture_recognition_result.gestures:
                # print(gesture_recognition_result.gestures[0][0].category_name)
                draw_progress_bar(frame, gesture_recognition_result.gestures[0][0].score, 1.0,
                                  gesture_recognition_result.gestures[0][0].category_name, (50, 50, 200, 20))
                frame = draw_landmarks_on_image(frame, gesture_recognition_result)
                # print('gesture recognition result: {}' + format(gesture_recognition_result))
                if gesture_recognition_result.gestures[0][0].category_name == 'Pointing_up':
                    pyautogui.keyDown(self.gestures[0])

                    # flags[gestures[0]] = True
                    cv2.putText(frame, self.gestures[0], (250, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (50, 200, 150), 3)
                elif gesture_recognition_result.gestures[0][0].category_name == 'pointing_down':
                    pyautogui.keyDown(self.gestures[1])

                    cv2.putText(frame, self.gestures[1], (250, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (50, 200, 150), 3)
                elif gesture_recognition_result.gestures[0][0].category_name == 'pinkyThumb':
                    pyautogui.keyDown(self.gestures[2])

                    cv2.putText(frame, self.gestures[2], (250, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (50, 200, 150), 3)
                elif gesture_recognition_result.gestures[0][0].category_name == 'three':
                    # if not flags[gestures[3]]:
                    pyautogui.keyDown(self.gestures[3])

                    # flags[gestures[3]] = True
                    cv2.putText(frame, self.gestures[3], (250, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (50, 200, 150), 3)
                elif gesture_recognition_result.gestures[0][0].category_name == 'four':
                    pyautogui.keyDown(self.gestures[4])

                    cv2.putText(frame, self.gestures[4], (250, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (50, 200, 150), 3)
                elif gesture_recognition_result.gestures[0][0].category_name == 'Yeah':
                    print("YEAHHHHHHH no gesture map......... yet")
                elif gesture_recognition_result.gestures[0][0].category_name == 'index_pinky':
                    print("no action my love")

                elif gesture_recognition_result.gestures[0][0].category_name == 'palm':
                    print("do nothing")
                    pyautogui.keyUp(self.gestures[0])
                    pyautogui.keyUp(self.gestures[1])
                    pyautogui.keyUp(self.gestures[2])
                    pyautogui.keyUp(self.gestures[3])
                    pyautogui.keyUp(self.gestures[4])

                else:
                    print("do nothing")

            cv2.imshow('Gesture Recognition', frame)
            if cv2.waitKey(1) & 0xFF == 27:  # Each frame lags for 20 milliseconds and then disappears, ESC key to exit
                break

        cap.release()
        cv2.destroyAllWindows()
