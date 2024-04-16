import cv2
import mediapipe as mp
import numpy as np
import pyautogui

def draw_info_text(image, gesture, brect):
    info_text = gesture
    cv2.putText(image, info_text, (brect[0] + 5, brect[1] - 4),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    return image

def calc_bounding_rect(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]
    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_point = [np.array((landmark_x, landmark_y))]
        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv2.boundingRect(landmark_array)
    return [x, y, x + w, y + h]

def main():
    cap = cv2.VideoCapture(0)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_draw = mp.solutions.drawing_utils

    while True:
        success, img = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # List used to store finger extension status (True means extended)
                fingers = []

                # Obtain landmark coordinates for finger MCP (Metacarpophalangeal, metacarpophalangeal joint) and TIP (tip of the finger)
                for i, finger in enumerate([mp_hands.HandLandmark.INDEX_FINGER_MCP, mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
                                            mp_hands.HandLandmark.RING_FINGER_MCP]):
                    finger_mcp = hand_landmarks.landmark[finger]
                    finger_tip = hand_landmarks.landmark[finger + 3]

                    # Determine if fingers are extended (tip y-coordinate is less than metacarpophalangeal joint y-coordinate)
                    fingers.append(finger_tip.y < finger_mcp.y)

                # The thumb is a slightly special case, judged here by its x-coordinate #
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
                fingers.insert(0, thumb_tip.x < thumb_ip.x)

                rect = calc_bounding_rect(img, hand_landmarks)

                # Exit if all three specified fingers are raised
                if all(fingers[1:]):
                    break

        cv2.imshow("Hands", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    
if __name__ == "__main__":
    main()
