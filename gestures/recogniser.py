import mediapipe as mp
import cv2
import math
from collections import deque, Counter

class GestureRecognizer:
    def __init__(self, debug=False):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.debug = debug
        self.gesture_history = deque(maxlen=5)

    def _calc_angle(self, a, b, c):
        ba = [a.x - b.x, a.y - b.y]
        bc = [c.x - b.x, c.y - b.y]
        dot_product = ba[0]*bc[0] + ba[1]*bc[1]
        mag_ba = math.hypot(*ba)
        mag_bc = math.hypot(*bc)
        if mag_ba * mag_bc == 0:
            return 0
        cos_angle = dot_product / (mag_ba * mag_bc)
        angle = math.acos(max(-1, min(1, cos_angle)))
        return math.degrees(angle)

    def _is_pointing(self, lm):
        index_angle = self._calc_angle(lm[6], lm[7], lm[8])
        middle_angle = self._calc_angle(lm[10], lm[11], lm[12])
        ring_angle = self._calc_angle(lm[14], lm[15], lm[16])
        pinky_angle = self._calc_angle(lm[18], lm[19], lm[20])

        if self.debug:
            print(f"Index: {index_angle:.1f}, Middle: {middle_angle:.1f}, Ring: {ring_angle:.1f}, Pinky: {pinky_angle:.1f}")

        return (index_angle > 150 and
                middle_angle < 130 and
                ring_angle < 130 and
                pinky_angle < 130)

    def _is_open_palm(self, lm):
        # Finger angles
        angles = [
            self._calc_angle(lm[6], lm[7], lm[8]),    # Index
            self._calc_angle(lm[10], lm[11], lm[12]),  # Middle
            self._calc_angle(lm[14], lm[15], lm[16]),  # Ring
            self._calc_angle(lm[18], lm[19], lm[20])   # Pinky
        ]

        # Thumb open check (x distance from wrist)
        thumb_tip = lm[4]
        thumb_ip = lm[3]
        thumb_mcp = lm[2]
        wrist = lm[0]
        thumb_open = abs(thumb_tip.x - wrist.x) > 0.1

        # Palm facing camera: middle finger tip should be closer than wrist (z-axis)
        facing_camera = lm[12].z < lm[0].z

        if self.debug:
            print(f"Finger angles: {[round(a, 1) for a in angles]}, Thumb open: {thumb_open}, Facing cam: {facing_camera}")

        return all(angle > 150 for angle in angles) and thumb_open and facing_camera

    def _get_most_common_gesture(self):
        if not self.gesture_history:
            return "Unknown"
        count = Counter(self.gesture_history)
        most_common, freq = count.most_common(1)[0]
        if freq >= 2:
            return most_common
        return "Unknown"

    def detect_gesture(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(frame_rgb)
        gesture = "Unknown"

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                lm = hand_landmarks.landmark
                wrist = lm[0]
                index_tip = lm[8]

                if self._is_pointing(lm):
                    dx = index_tip.x - wrist.x
                    if dx > 0.02:
                        gesture = "Move Forward"
                    elif dx < -0.02:
                        gesture = "Move Backward"
                elif self._is_open_palm(lm):
                    gesture = "Stop"

                self.mp_draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

        self.gesture_history.append(gesture)
        smoothed = self._get_most_common_gesture()

        if self.debug:
            cv2.putText(frame, f'Gesture: {smoothed}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)

        return frame, smoothed
