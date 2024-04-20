import cv2
import mediapipe as mp

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
                                            mp_hands.HandLandmark.RING_FINGER_MCP, mp_hands.HandLandmark.PINKY_MCP]):
                    finger_mcp = hand_landmarks.landmark[finger]
                    finger_tip = hand_landmarks.landmark[finger + 3]

                    # Determine if fingers are extended (tip y-coordinate is less than metacarpophalangeal joint y-coordinate)
                    fingers.append(finger_tip.y < finger_mcp.y)

                # The thumb is a slightly special case, judged here by its x-coordinate #
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
                fingers.insert(0, thumb_tip.x > thumb_ip.x)

                # Detect all fingers extended
                if all(fingers):
                    # 'Stop' Command
                    print("Stop")

                # Detect pointer, middle, and thumb extended
                elif fingers[1] and fingers[2] and fingers[0]:
                    # 'Display Camera' Command
                    print(f"Camera Device: {cv2.VideoCapture(0).get(cv2.CAP_PROP_BACKEND)}")

                # Print the corresponding number based on the number of fingers stretched out
                # if all(not f for f in fingers):
                    # print("6 - Fist")
                # else:
                    # print(f"{fingers.count(True)} - Fingers extended")

                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Hands", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()