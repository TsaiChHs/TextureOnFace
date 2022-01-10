import pandas as pd
import numpy as np
import csv

def finger_stand(points):
    fingers = []
    hands = int(points.shape[0]//21)
    for i in range(hands):
        if (points['y'][i+4] < points['y'][i+5]): # 拇指
            fingers.append(0+5*i)
        if (points['y'][i+8] < points['y'][i+6]): # 食指
            fingers.append(1+5*i)
        if (points['y'][i+12] < points['y'][i+10]): # 中指
            fingers.append(2+5*i)
        if (points['y'][i+16] < points['y'][i+14]): # 無名指
            fingers.append(3+5*i)
        if (points['y'][i+20] < points['y'][i+18]): # 小指
            fingers.append(4+5*i)
    return fingers

def ishid0(points):
    x_diff = max(abs(points['x'][5] - points['x'][9]), abs(points['x'][6] - points['x'][10]), abs(points['x'][7] - points['x'][11]), abs(points['x'][8] - points['x'][12]))
    fingers = finger_stand(points)
    if ((fingers == [1, 2]) | (fingers == [6, 7])) & (x_diff < 50):
        return True
    else:
        return False

def fingerRecognitiion(data):
    points = pd.DataFrame(data, columns = ['x', 'y'])
    
    # print(points)
    # with open('points_fid0-1.csv', 'a+', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     for p in range(points.shape[0]):
    #         writer.writerow([p, points['x'][p], points['y'][p]])
    # csvfile.close()

    if ishid0(points):
        return 0
    else:
        return -1