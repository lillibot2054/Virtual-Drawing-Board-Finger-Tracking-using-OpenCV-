import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe hand detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

# Webcam setup
cap = cv2.VideoCapture(0)

# Variables
canvas = None
x_prev, y_prev = 0, 0
color = (255, 0, 0)  # Default: Blue
brush_thickness = 5
eraser_thickness = 40

print("Controls:")
print("Press R - Red | G - Green | B - Blue | E - Eraser | S - Save | ESC - Exit")

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    if canvas is None:
        canvas = np.zeros((h, w, 3), np.uint8)

    # Detect hands
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lmList = []
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((cx, cy))

            # Index finger tip
            x, y = lmList[8]
            cv2.circle(frame, (x, y), 8, color, -1)

            # Draw when only index finger is up
            if x_prev == 0 and y_prev == 0:
                x_prev, y_prev = x, y

            cv2.line(canvas, (x_prev, y_prev), (x, y), color, brush_thickness)
            x_prev, y_prev = x, y
    else:
        x_prev, y_prev = 0, 0

    # Merge canvas and live frame
    frame = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)

    # Display
    cv2.imshow("Virtual Drawing Board", frame)

    # Key controls
    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC
        break
    elif key == ord('r'):
        color = (0, 0, 255)  # Red
        print("Color changed to RED")
    elif key == ord('g'):
        color = (0, 255, 0)  # Green
        print("Color changed to GREEN")
    elif key == ord('b'):
        color = (255, 0, 0)  # Blue
        print("Color changed to BLUE")
    elif key == ord('e'):
        color = (0, 0, 0)  # Eraser (black)
        print("Eraser mode ON")
    elif key == ord('s'):
        cv2.imwrite("my_drawing.png", canvas)
        print("Drawing saved as my_drawing.png")

cap.release()
cv2.destroyAllWindows()
