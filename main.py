import cv2
import mediapipe as mp
import numpy as np
from FaceTexture import hand2Texture

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

from finger_recognitiion import fingerRecognitiion

def main():
    # webcam
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        hID = -1
        success, image = cap.read()
        imageHeight, imageWidth, _ = image.shape
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue
        
        with mp_hands.Hands(
        max_num_hands=4, # 建議填入最少出現手數(以組為單位)
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
        
            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:

                    check_points = []
                    for point in mp_hands.HandLandmark:
                        normalizedLandmark = hand_landmarks.landmark[point]
                        pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)
                        # print(point)
                        # print(point.value)
                        # print(normalizedLandmark) 
                        # # 以下兩項一樣，但 pixelCoordinatesLandmark 有時候會是 None
                        # print(pixelCoordinatesLandmark)
                        # x = hand_landmarks.landmark[point.value].x*image.shape[1]
                        # y = hand_landmarks.landmark[point.value].y*image.shape[0]
                        # print(x, y)
                        check_points.append([round(hand_landmarks.landmark[point.value].x*image.shape[1], 1), round(hand_landmarks.landmark[point.value].y*image.shape[0], 1)])
                            
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

                    hID = fingerRecognitiion(check_points)

        hand2Texture(hID, image)

        # Flip the image horizontally for a selfie-view display.
        # cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
            
    cap.release()
    
main()