# Unit Tests
# Creator: Ashley

import unittest
import cv2
import pyautogui
from .unitTestHandDetector import HandDetector


class UnitTests(unittest.TestCase):
    def setUp(self):
        print("***Unit test initiated")
        # Initialize HandDetector object with appropriate parameters
        self.detector = HandDetector(mode=False, maxHands=1, detectionCon=0.8, minTrackCon=0.5)

    def tearDown(self):
        # No need to release video capture or close OpenCV windows here
        print("Unit test complete***", end='\n\n')
        pass

    # Hand Detection Unit Test (fails if no hand is detected within a certain # of frames)
    def test_hand_detection(self):
        print("Testing hand detection")
        # Initialize video capture from the webcam (change index if necessary)
        cap = cv2.VideoCapture(0)

        # Number of frames before test stops trying to detect hand
        timeout = 250
        frame_count = 0
        hand_detected = False

        while frame_count < timeout:
            # Read a frame from the webcam
            ret, frame = cap.read()

            # Perform hand detection on the frame
            hands, _ = self.detector.findHands(frame, flipType=False, draw=True)

            # Display the frame with hand detection
            cv2.imshow('Hand Detection Unit Test', frame)

            # Check if hands are detected
            if hands:
                hand_detected = True
                break

            frame_count += 1

            # Check for esc key press to exit the loop
            if cv2.waitKey(1) & 0xFF == 27:
                break

        # Release the video capture and close OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

        # Assert that a hard was detected during the test
        self.assertTrue(hand_detected, "No hand was detected within the timeframe")

    # Helper for Gesture Recognition Unit Tests (fails if a gesture is not recognized within a certain # of frames)
    def perform_gesture_recognition(self, gesture_name, expected_gesture, max_frames=250):
        print("Testing gesture recognition:", gesture_name)
        # Initialize video capture from the webcam (change index if necessary)
        cap = cv2.VideoCapture(0)

        gesture_recognized = False
        frame_count = 0

        while frame_count < max_frames:
            # Read a frame from the webcam
            ret, frame = cap.read()

            # Perform hand detection on the frame
            hands, _ = self.detector.findHands(frame, flipType=False, draw=True)

            # Perform gesture recognition if hands are detected
            if hands:
                for hand in hands:
                    # Get the finger states (up/down) from the hand landmarks
                    fingers = self.detector.fingersUp(hand)

                    # Check if the detected gesture matches the expected gesture
                    if fingers == expected_gesture:
                        print("Gesture recognized:", gesture_name)
                        gesture_recognized = True

            # Display the frame with gesture recognition
            cv2.imshow(f'Gesture Recognition Unit Test: {gesture_name}', frame)

            # Check for esc key press to exit the loop
            if cv2.waitKey(1) & 0xFF == 27:
                break

            frame_count += 1

        # Release the video capture and close OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

        # Assert that the gesture was recognized within the specified number of frames
        self.assertTrue(gesture_recognized, f"Gesture not recognized within the timeframe: {gesture_name}")

    # Gesture Recognition Unit Test for Thumb open, others bent
    def test_thumb_open(self):
        self.perform_gesture_recognition("Thumb open, others bent", [1, 0, 0, 0, 0])

    # Gesture Recognition Unit Test for Thumb bent, others open
    def test_thumb_bent(self):
        self.perform_gesture_recognition("Thumb bent, others open", [0, 1, 1, 1, 1])

    # Gesture Recognition Unit Test for All five fingers open
    def test_five_fingers_open(self):
        self.perform_gesture_recognition("Hand open", [1, 1, 1, 1, 1])

    # Gesture Recognition Unit Test for All five fingers open
    def test_five_fingers_bent(self):
        self.perform_gesture_recognition("Hand closed", [0, 0, 0, 0, 0])

    # Gesture Recognition Unit Test for Index finger bent
    def test_index_bent(self):
        self.perform_gesture_recognition("OK-Symbol", [1, 0, 1, 1, 1])

    # Gesture Recognition Unit Test for Index and Middle open
    def test_index_middle(self):
        self.perform_gesture_recognition("Peace Sign", [0, 1, 1, 0, 0])

    # Mouse Control Unit Test (fails if mouse was not moved within a certain # of frames)
    def test_mouse_control(self):
        print("Testing mouse control")
        # Initialize video capture from the webcam (change index if necessary)
        cap = cv2.VideoCapture(0)

        # Initialize cursor moved flag and frame counter
        cursor_moved = False
        frame_count = 0

        while frame_count < 250:  # Check for cursor movement within 250 frames
            # Read a frame from the webcam
            ret, frame = cap.read()

            # Perform hand detection on the frame
            hands, _ = self.detector.findHands(frame, flipType=False, draw=True)

            # Perform mouse control if hands are detected
            if hands:
                for hand in hands:
                    # Get hand landmarks
                    lmList = hand['lmList']

                    # Get the position of the index finger (assuming index finger is finger 8)
                    index_finger = lmList[8]

                    # Get the x, y coordinates of the index finger
                    x, y = index_finger[1], index_finger[2]

                    # Move the mouse cursor to the position of the index finger
                    pyautogui.moveTo(x, y)

                    # Print the position of the index finger (for demonstration purposes)
                    print("Index finger position:", x, y)

                    # Set cursor moved flag to True
                    cursor_moved = True

            # Display the frame with mouse control visualization
            cv2.imshow('Mouse Control Test', frame)

            # Increment frame counter
            frame_count += 1

            # Check for esc key press to exit the loop
            if cv2.waitKey(1) & 0xFF == 27:
                break

        # Release the video capture and close OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

        # Assert that the cursor has moved during the test
        self.assertTrue(cursor_moved, "Cursor did not move within the timeframe")


