import pandas as pd
import numpy as np
import csv

def ishid0(points):
    x_diff = max(abs(points['x'][5] - points['x'][9]), abs(points['x'][6] - points['x'][10]), abs(points['x'][7] - points['x'][11]), abs(points['x'][8] - points['x'][12]))
    up_mean = np.mean(points.loc[5:13, 'y'].values) 
    down_mean = np.mean(points.loc[:5, 'y'].values)+np.mean(points.loc[13:, 'y'].values)/2
    if (x_diff < 50) & (up_mean < down_mean):
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