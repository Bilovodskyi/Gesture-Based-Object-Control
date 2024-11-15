import pickle
import numpy as np

import cv2
import mediapipe as mp
import math
from multiprocessing import Queue

model_dict = pickle.load(open("./model.p", "rb"))
model = model_dict["model"]


# def calculate_distance(point1, point2):
#     return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def hand_tracking(queue):
    # Initialize MediaPipe Hands.
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
    cap = cv2.VideoCapture(0)
    mp_drawing = mp.solutions.drawing_utils

    rotation_gesture_active = False
    position_gesture_active = False

    try:
        while True:
            success, frame = cap.read()
            if not success:
                continue

            # Flip the image horizontally for a selfie-view display
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = hands.process(frame_rgb)
            data_aux = []
            x_ = []
            y_ = []

            data = {"rotation_x": 0, "rotation_y": 0, "position_x": 0, "position_y": 0}

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y

                        x_.append(x)
                        y_.append(y)

                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        data_aux.append(x - min(x_))
                        data_aux.append(y - min(y_))

                for hand_landmarks in results.multi_hand_landmarks:

                    index_tip = hand_landmarks.landmark[
                        mp_hands.HandLandmark.INDEX_FINGER_TIP
                    ]
                    # thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    prediction = model.predict([np.asarray(data_aux)])
                    # print(prediction)
                    # if distance < 0.1:
                    if int(prediction[0]) == 2:

                        if not rotation_gesture_active:
                            rotation_gesture_active = True
                            prev_real_x = index_tip.x
                            prev_real_y = index_tip.y
                            data["rotation_x"] = 0
                            data["rotation_y"] = 0
                        else:
                            real_x = index_tip.x - prev_real_x
                            real_y = index_tip.y - prev_real_y
                            prev_real_x = index_tip.x
                            prev_real_y = index_tip.y
                            data["rotation_x"] = real_x
                            data["rotation_y"] = real_y

                        # draw a circle to indicate detection
                        frame_height, frame_width, _ = frame.shape
                        cv2.circle(
                            frame,
                            (
                                int(index_tip.x * frame_width),
                                int(index_tip.y * frame_height),
                            ),
                            10,
                            (0, 255, 0),
                            -1,
                        )
                    elif int(prediction[0]) == 3:
                        if not position_gesture_active:
                            position_gesture_active = True
                            prev_real_x = index_tip.x
                            prev_real_y = index_tip.y
                            data["position_x"] = 0
                            data["position_y"] = 0
                        else:
                            real_x = index_tip.x - prev_real_x
                            real_y = index_tip.y - prev_real_y
                            prev_real_x = index_tip.x
                            prev_real_y = index_tip.y
                            data["position_x"] = real_x
                            data["position_y"] = real_y

                        # draw a circle to indicate detection
                        frame_height, frame_width, _ = frame.shape
                        cv2.circle(
                            frame,
                            (
                                int(index_tip.x * frame_width),
                                int(index_tip.y * frame_height),
                            ),
                            10,
                            (0, 255, 0),
                            -1,
                        )

                    else:
                        if rotation_gesture_active:
                            rotation_gesture_active = False
                        if position_gesture_active:
                            position_gesture_active = False

                    # Draw the landmarks on the frame
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )
            queue.put(data)

            # Display the resulting frame
            cv2.imshow("Hand Tracking", frame)

            # Exit on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        hands.close()


if __name__ == "__main__":
    from multiprocessing import Queue

    # Create a queue for sharing data
    data_queue = Queue()

    # Start the hand tracking function
    hand_tracking(data_queue)
