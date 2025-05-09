# gesture_worker.py
import cv2
from gestures.recogniser import GestureRecognizer

def run_gesture_recognizer(shared_gesture):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Cannot open webcam.")
        return

    recognizer = GestureRecognizer()
    print("[INFO] Gesture recognizer started.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        _, gesture = recognizer.detect_gesture(frame)

        # Update the shared gesture string
        shared_gesture.value = gesture

        # Display (optional)
        cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Gesture Detection", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()
