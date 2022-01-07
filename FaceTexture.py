import cv2
import mediapipe as mp
import numpy as np
import statistics
import math

def redEye(frame, face_mesh):
    left_eye_list = [153, 159, 33, 246, 7, 161, 163, 160, 144, 145, 158, 157, 154, 173, 155, 133]
    right_eye_list = [386, 380, 362, 398, 384, 385, 387, 388, 466, 263, 249, 390, 373, 374, 381, 382]
    
    # 載入更換眼睛圖案的圖片
    eye_normal = cv2.imread("redEye.png")

    # 轉換顏色為RGB並丟入face mesh運算
    h, w, d = frame.shape
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)

    if results.multi_face_landmarks:
        for eye_list in (left_eye_list, right_eye_list):
            # 歷遍左眼各點取得目前座標與眼睛大小
            for face_landmarks in results.multi_face_landmarks:
                eye_point = []
                eye_size = []
                for index in eye_list:
                    x = int(face_landmarks.landmark[index].x * w)
                    y = int(face_landmarks.landmark[index].y * h)
                    eye_point.append([x, y])
                    if index == eye_list[0] or index == eye_list[1]:
                        eye_size.append([x, y])
                if len(eye_size) == 2:
                    eye_len = int(math.pow(math.pow((eye_size[0][0] - eye_size[1][0]), 2) + math.pow((eye_size[0][1] - eye_size[1][1]), 2), 0.5))
                else:
                    eye_len = 0
            try:
                # 將取得的各點透過statistics計算出眼睛中心座標
                points = eye_point
                center = [statistics.mean(i) for i in zip(*points)]

                # 透過剛剛取得的眼睛大小, 將眼睛圖案的圖片轉換成適合的大小
                eye = cv2.resize(eye_normal, (eye_len, eye_len))

                # 透過一系列的處理將眼睛圖片貼在左眼上
                eye_gray = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)
                _, eye_mask = cv2.threshold(eye_gray, 25, 255, cv2.THRESH_BINARY_INV)

                img_height, img_width, _ = eye.shape
                x, y = int(center[0]-img_width/2), int(center[1]-img_height/2)
                eye_area = frame[y: y+img_height, x: x+img_width]
                eye_area_no_eye = cv2.bitwise_and(eye_area, eye_area, mask=eye_mask)
                final_eye = cv2.add(eye_area_no_eye, eye)
                final_eye = cv2.addWeighted(frame[y: y+img_height, x: x+img_width], 0.5, final_eye, 0.5, 0)
                frame[y: y+img_height, x: x+img_width] = final_eye
            # except:
            except Exception as exp:
                print("Some Error Occur", exp)
                pass
    return frame

def hand2Texture(hID, frame, face_mesh):
    if hID == -1:
        pass
    elif hID == 0:
        redEye(frame, face_mesh)

    cv2.imshow("MediaPipe FaceMesh", frame)