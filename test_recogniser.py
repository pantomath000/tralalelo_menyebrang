# test_gesture_recognizer.py
import cv2
from gestures.recogniser import GestureRecognizer

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Cannot open webcam.")
        return

    recognizer = GestureRecognizer(debug=True)
    print("[INFO] Starting gesture recognizer. Press ESC to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)  # Mirror for natural interaction
        frame, gesture = recognizer.detect_gesture(frame)

        # Display gesture on screen
        cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Gesture Test", frame)

        # ESC to exit
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
