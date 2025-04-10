# Help Received: https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker
# Help Received: https://github.com/silverwing-coder/CourseSubjects/blob/master/CIS463%24ProgrammingForRobotics/MediaPipeDemo/HandLandmarks.py
# Help Recieved: Use of ChatGPT to help figure out why my camera was not on when running this code

# Author: Benjamin Davis


import cv2
# STEP 1: Import the necessary modules.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54)  # vibrant green

def draw_landmarks_on_image(rgb_image, detection_result):
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    annotated_image = np.copy(rgb_image)

    # Loop through the detected hands to visualize.
    for idx in range(len(hand_landmarks_list)):
        hand_landmarks = hand_landmarks_list[idx]
        handedness = handedness_list[idx]

        # Draw the hand landmarks.
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            hand_landmarks_proto,
            solutions.hands.HAND_CONNECTIONS,
            solutions.drawing_styles.get_default_hand_landmarks_style(),
            solutions.drawing_styles.get_default_hand_connections_style())

        # Get the top left corner of the detected hand's bounding box.
        height, width, _ = annotated_image.shape
        x_coordinates = [landmark.x for landmark in hand_landmarks]
        y_coordinates = [landmark.y for landmark in hand_landmarks]
        text_x = int(min(x_coordinates) * width)
        text_y = int(min(y_coordinates) * height) - MARGIN

        # Count fingers
        finger_count = count_fingers(hand_landmarks, handedness)

        # Draw handedness + finger count on the image
        text = f"{handedness[0].category_name}: {finger_count}"
        cv2.putText(annotated_image, text,
                    (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                    FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

    return annotated_image

def count_fingers(hand_landmarks, handedness):
    finger_tips_ids = [4, 8, 12, 16, 20]
    finger_pip_ids = [2, 6, 10, 14, 18]

    count = 0

    # Thumb
    if handedness[0].category_name == 'Right':
        if hand_landmarks[4].x > hand_landmarks[3].x:
            count += 1
    else:
        if hand_landmarks[4].x < hand_landmarks[3].x:
            count += 1

    # Other 4 fingers
    for tip_id, pip_id in zip(finger_tips_ids[1:], finger_pip_ids[1:]):
        if hand_landmarks[tip_id].y < hand_landmarks[pip_id].y:
            count += 1

    return count

def main():
    capture = cv2.VideoCapture(0)
    # STEP 2: Create an HandLandmarker object.
    
    base_options = python.BaseOptions(
        model_asset_path=r'C:\Users\davis\OneDrive - Virginia Military Institute\Documents\S6\Robotics\CIS463_assignments\hand_landmarker.task'
    )

    options = vision.HandLandmarkerOptions(base_options=base_options,
                                           num_hands=2)
    detector = vision.HandLandmarker.create_from_options(options)

    while (capture.isOpened()):
        success, image = capture.read()
        if(success):
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
            result = detector.detect(mp_image)

            anotated_image = draw_landmarks_on_image(image, result)

            cv2.imshow('Hand Landmarks', cv2.cvtColor(anotated_image, cv2.COLOR_RGB2BGR))

        if cv2.waitKey(1) == ord('q'):
            break

    capture.release()
    cv2.destroyWindow('Hand Landmarks')  # Close the specific window

if __name__ == '__main__':
    main()