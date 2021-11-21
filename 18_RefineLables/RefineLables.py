import os
import shutil
import math
import numpy as np
import cv2
from tqdm import tqdm
import glob

file_path = r'L:\Detection\20211026RSAICP_Ship_Detection_Competition\RSAICP_Ship_Detection\train\mask_refine_66'
save_path = r'L:\Detection\20211026RSAICP_Ship_Detection_Competition\RSAICP_Ship_Detection\train\mask_refine_66'
file_list = glob.glob(file_path + '/*.txt')
for file in file_list:
    bboxes = np.loadtxt(file, float, usecols=[1, 2, 3, 4, 5, 6, 7, 8], delimiter=',', ndmin=2)
    # if len(bboxes) == 0:
    #     continue
    refine_bboxes = []
    for bbox in bboxes:
        x1, y1, x2, y2, x3, y3, x4, y4 = bbox  # 逆时针
        cx, cy = (x1 + x2 + x3 + x4)/4, (y1 + y2 + y3 + y4)/4
        w, h = (x4 - x1 + x3 - x2)/2, (y2 - y1 + y3 - y4)/2
        w = 0.66 * w
        h = 0.66 * h
        l = cx - w/2
        t = cy - h/2
        r = cx + w/2
        b = cy + h/2
        # l, t, r, b = bbox
        refine_bboxes.append([0, l, t, r, b])
    np.savetxt(save_path + '/' + os.path.basename(file), np.array(refine_bboxes), '%d %.4f %.4f %.4f %.4f')
