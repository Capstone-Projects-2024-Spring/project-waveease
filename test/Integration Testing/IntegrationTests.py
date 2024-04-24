import unittest
from unittest.mock import patch, MagicMock
import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
official_version_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'officialVersion'))
sys.path.append(official_version_dir)
from gesture_recognition import start
import cv2

class TestWaveEaseIntegration(unittest.TestCase):

    @patch('gesture_recognition.configparser.ConfigParser')
    @patch('gesture_recognition.cap')
    @patch('gesture_recognition.pyautogui')
    @patch('gesture_recognition.GestureRecognizer.create_from_options')
    def test_integration(self, mock_create_from_options, mock_pyautogui, mock_cap, mock_configparser):
        # Mocking necessary objects
        mock_cap.return_value.isOpened.return_value = True
        mock_capture = MagicMock()
        mock_capture.read.return_value = (True, cv2.imread('dog_image.jpg'))  # Assume dog_image.jpg exists
        mock_cap.return_value = mock_capture
        mock_create_from_options.return_value.recognize_for_video.return_value.gestures = [(MagicMock(),)]
        mock_pyautogui.press.return_value = None

        start()

        mock_cap.assert_called()
        mock_capture.read.assert_called()
        mock_create_from_options.return_value.recognize_for_video.assert_called()
        mock_pyautogui.press.assert_called()

if __name__ == '__main__':
    unittest.main()
