import numpy as np
import glob
import os


file_path = r'D:\Ship\RSAICP_Ship_Detection\test\img'
file_list = glob.glob(file_path + '/*.txt')
for txt_name in file_list:
    bboxes = np.loadtxt(txt_name, float, usecols=[1, 2, 5, 6], delimiter=',', ndmin=2)
    area = np.prod(bboxes[:, 2:] - bboxes[:, :2], axis=1)
    print(f'{os.path.basename(txt_name)}: min_area:{np.min(area)} max_area:{np.max(area)} mean_area:{np.mean(area)}')
