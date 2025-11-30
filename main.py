import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe hand detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.6)

# Webcam setup
cap = cv2.VideoCapture(0)

# Variables
canvas = None
x_prev, y_prev = 0, 0
color = (255, 0, 0)  # Default: Blue
brush_thickness = 5
eraser_thickness = 40

# Undo/Reset functionality
drawing_history = []
MAX_HISTORY = 20

# Gesture state tracking
gesture_cooldown = 0
GESTURE_COOLDOWN_TIME = 30  # frames

print("Controls:")
print("1 Finger: Draw | 2 Fingers: Erase | 3 Fingers: Undo | 4 Fingers: Reset")
print("Press R/G/B - Colors | E - Eraser | S - Save | ESC - Exit")

def draw_color_palette(frame):
    """Visual interface with color palette"""
    colors = [
        (0, 0, 255),    # Red
        (0, 255, 0),    # Green  
        (255, 0, 0),    # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
        (255, 255, 255) # White (Eraser)
    ]
    color_names = ["R", "G", "B", "Y", "M", "C", "E"]
    
    for i, (col, name) in enumerate(zip(colors, color_names)):
        cv2.rectangle(frame, (10 + i*45, 10), (45 + i*45, 45), col, -1)
        cv2.rectangle(frame, (10 + i*45, 10), (45 + i*45, 45), (255, 255, 255), 2)
        text_color = (0, 0, 0) if col != (0, 0, 0) else (255, 255, 255)
        cv2.putText(frame, name, (20 + i*45, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)

def save_to_history():
    """Save current canvas state to history for undo functionality"""
    if len(drawing_history) >= MAX_HISTORY:
        drawing_history.pop(0)
    drawing_history.append(canvas.copy())

def count_extended_fingers(lmList):
    """Count how many fingers are extended"""
    fingers = []
    
    # Thumb
    thumb_tip = lmList[4]
    thumb_ip = lmList[3]
    if thumb_tip[0] > thumb_ip[0]:
        fingers.append(True)
    else:
        fingers.append(False)
    
    # Other four fingers
    for tip_id in [8, 12, 16, 20]:
        if lmList[tip_id][1] < lmList[tip_id - 2][1]:
            fingers.append(True)
        else:
            fingers.append(False)
    
    return sum(fingers), fingers

def draw_gesture_visualization(frame, lmList, fingers):
    """Visual feedback for gestures"""
    colors = [(0, 255, 0), (0, 255, 255), (0, 165, 255), (0, 0, 255), (255, 0, 0)]
    finger_tips = [4, 8, 12, 16, 20]
    
    for i, (tip_id, is_extended) in enumerate(zip(finger_tips, fingers)):
        x, y = lmList[tip_id]
        if is_extended:
            cv2.circle(frame, (x, y), 12, colors[i], -1)
            cv2.circle(frame, (x, y), 12, (255, 255, 255), 2)
        else:
            cv2.circle(frame, (x, y), 8, (100, 100, 100), -1)

def perform_gesture_action(finger_count, frame):
    """Execute actions based on finger count gestures"""
    global canvas, color, gesture_cooldown
    
    if gesture_cooldown > 0:
        return
    
    h, w = frame.shape[:2]
    
    if finger_count == 3:  # UNDO
        if drawing_history:
            canvas = drawing_history.pop()
            cv2.putText(frame, "UNDO", (w//2 - 50, h//2), 
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 3)
            print("Gesture: UNDO")
            gesture_cooldown = GESTURE_COOLDOWN_TIME
    
    elif finger_count == 4:  # RESET
        save_to_history()
        canvas = np.zeros((h, w, 3), np.uint8)
        cv2.putText(frame, "RESET", (w//2 - 60, h//2), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        print("Gesture: RESET")
        gesture_cooldown = GESTURE_COOLDOWN_TIME
    
    elif finger_count == 5:  # COLOR CHANGE
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), 
                  (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        current_idx = colors.index(color) if color in colors else 0
        color = colors[(current_idx + 1) % len(colors)]
        color_name = ["Blue", "Green", "Red", "Yellow", "Magenta", "Cyan"][(current_idx + 1) % len(colors)]
        cv2.putText(frame, f"COLOR: {color_name}", (w//2 - 100, h//2), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)
        print(f"Gesture: COLOR CHANGE to {color_name}")
        gesture_cooldown = GESTURE_COOLDOWN_TIME

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    if canvas is None:
        canvas = np.zeros((h, w, 3), np.uint8)

    draw_color_palette(frame)

    if gesture_cooldown > 0:
        gesture_cooldown -= 1

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    current_finger_count = 0
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lmList = []
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((cx, cy))

            if len(lmList) >= 21:
                finger_count, fingers = count_extended_fingers(lmList)
                current_finger_count = finger_count
                draw_gesture_visualization(frame, lmList, fingers)
                
                x, y = lmList[8]

                # Perform gesture actions
                if finger_count >= 3:
                    perform_gesture_action(finger_count, frame)

                # Draw Mode
                elif finger_count == 1 and fingers[1]:
                    if x_prev == 0 and y_prev == 0:
                        x_prev, y_prev = x, y
                    
                    # ✅ FIXED distance formula
                    distance = np.sqrt((x - x_prev)**2 + (y - y_prev)**2)
                    if np.isnan(distance) or np.isinf(distance):
                        distance = 0
                    steps = max(1, int(distance / 2))
                    
                    for i in range(steps + 1):
                        if steps > 0:
                            x_i = int(x_prev + (x - x_prev) * i / steps)
                            y_i = int(y_prev + (y - y_prev) * i / steps)
                            if color == (0, 0, 0):  # Eraser
                                cv2.circle(canvas, (x_i, y_i), eraser_thickness, (0, 0, 0), -1)
                            else:
                                cv2.circle(canvas, (x_i, y_i), brush_thickness, color, -1)
                    
                    x_prev, y_prev = x, y

                # Eraser Mode
                elif finger_count == 2 and fingers[1] and fingers[2]:
                    cv2.circle(frame, (x, y), 30, (0, 0, 255), 3)
                    cv2.circle(canvas, (x, y), eraser_thickness, (0, 0, 0), -1)
                    x_prev, y_prev = x, y

                else:
                    x_prev, y_prev = 0, 0
    else:
        x_prev, y_prev = 0, 0

    # Merge canvas and live frame
    frame = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)

    mode_text = "DRAW" if color != (0, 0, 0) else "ERASE"
    color_display = color if color != (0, 0, 0) else (255, 255, 255)

    cv2.putText(frame, f'Fingers: {current_finger_count}', (w - 150, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f'Mode: {mode_text}', (10, h - 80), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_display, 2)
    cv2.putText(frame, f'History: {len(drawing_history)}/{MAX_HISTORY}', (10, h - 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, '1:Draw | 2:Erase | 3:Undo | 4:Reset | 5:Color', (10, h - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow("Virtual Drawing Board - Gesture Controls", frame)

    # Keyboard controls
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break
    elif key == ord('r'):
        color = (0, 0, 255)
        print("Color changed to RED")
    elif key == ord('g'):
        color = (0, 255, 0)
        print("Color changed to GREEN")
    elif key == ord('b'):
        color = (255, 0, 0)
        print("Color changed to BLUE")
    elif key == ord('e'):
        color = (0, 0, 0)
        print("Eraser mode ON")
    elif key == ord('s'):
        cv2.imwrite("my_drawing.png", canvas)
        print("Drawing saved as my_drawing.png")
    elif key == ord('z'):  # Undo (backup)
        if drawing_history:
            canvas = drawing_history.pop()
            print("Keyboard: UNDO")

cap.release()
cv2.destroyAllWindows()
