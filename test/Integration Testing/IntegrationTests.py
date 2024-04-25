import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import cv2
import numpy as np
#import pyautogui
import mediapipe as mp

current_dir = os.path.dirname(os.path.realpath(__file__))
official_version_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'officialVersion'))
sys.path.append(official_version_dir)
from gesture_recognition import start

class TestWaveEaseIntegration(unittest.TestCase):

    @patch('gesture_recognition.configparser.ConfigParser')
    @patch('gesture_recognition.cap')
    @patch('gesture_recognition.pyautogui')
    @patch('gesture_recognition.GestureRecognizer.create_from_options')
    
    #Use Case 1: Integration Testing for MS Paint
    def test_integration_for_MS_Paint(self, mock_create_from_options, mock_pyautogui, mock_cap, mock_capture):
        # Mocking necessary objects for gesture recognition
        mock_cap.return_value.isOpened.return_value = True
        mock_capture = MagicMock()
        mock_capture.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))  # Mock an image frame
        mock_cap.return_value = mock_capture
        mock_create_from_options.return_value.recognize_for_video.return_value.gestures = [(MagicMock(),)]
        mock_pyautogui.press.return_value = None

        # Set up mock for hands landmarks
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands()
        mock_landmark1 = MagicMock()
        mock_landmark1.landmark = [MagicMock() for _ in range(21)]  # Mock hand landmarks
        mock_landmark2 = MagicMock()
        mock_landmark2.landmark = [MagicMock() for _ in range(21)]  # Mock hand landmarks
        mock_results = MagicMock()
        mock_results.multi_hand_landmarks = [mock_landmark1, mock_landmark2]
        hands.process.return_value = mock_results

        # Call the start method
        start()

        # Assert that the expected methods are called
        mock_cap.assert_called()
        mock_capture.read.assert_called()
        mock_create_from_options.return_value.recognize_for_video.assert_called()
        mock_pyautogui.press.assert_called()

    #Use Case 2: Integration Testing for Geography Activity
    def test_integration_for_geography_activity(self):
        # Mocking necessary objects for gesture recognition
        with patch('gesture_recognition.configparser.ConfigParser'), \
             patch('gesture_recognition.cap') as mock_cap, \
             patch('gesture_recognition.pyautogui') as mock_pyautogui, \
             patch('gesture_recognition.GestureRecognizer.create_from_options') as mock_create_from_options:
            
            # Set up mock for capturing image
            mock_cap.return_value.isOpened.return_value = True
            mock_capture = MagicMock()
            mock_capture.read.return_value = (True, cv2.imread('hand_test.jpg'))
            mock_cap.return_value = mock_capture
            
            # Mock gesture recognition
            mock_create_from_options.return_value.recognize_for_video.return_value.gestures = [(MagicMock(),)]
            mock_pyautogui.press.return_value = None

            # Call the start method
            start()

            # Assert that the expected methods are called
            mock_cap.assert_called()
            mock_capture.read.assert_called()
            mock_create_from_options.return_value.recognize_for_video.assert_called()
            mock_pyautogui.press.assert_called()

if __name__ == '__main__':
    unittest.main()

