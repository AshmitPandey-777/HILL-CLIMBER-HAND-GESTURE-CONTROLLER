import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller

# Open the webcam
cap = cv2.VideoCapture(0)

# Initialize MediaPipe and pynput
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
keyboard = Controller()

# Finger tip landmark numbers
fingertips = [4, 8, 12, 16, 20]

while True:
    success, frame = cap.read()
    if not success:
        continue

    # Flip the frame so it acts like a mirror
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            lm = hand_landmarks.landmark

            # Count fingers (excluding thumb)
            fingers_up = 0
            for tip in fingertips[1:]:
                if lm[tip].y < lm[tip - 2].y:
                    fingers_up += 1

            # Gesture to control game
            if fingers_up >= 4:
                keyboard.release(Key.right)
                keyboard.press(Key.left)
                cv2.putText(frame, 'BRAKE', (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            elif fingers_up <= 1:
                keyboard.release(Key.left)
                keyboard.press(Key.right)
                cv2.putText(frame, 'GAS', (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                keyboard.release(Key.left)
                keyboard.release(Key.right)
                cv2.putText(frame, 'NEUTRAL', (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    else:
        # If no hand detected
        keyboard.release(Key.left)
        keyboard.release(Key.right)
        cv2.putText(frame, 'NO HAND', (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2)

    # Show the camera feed
    cv2.imshow("Hill Climb - Hand Control", frame)

    # Exit when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything when done
cap.release()
cv2.destroyAllWindows()
