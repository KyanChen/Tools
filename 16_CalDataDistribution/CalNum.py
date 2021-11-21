import os
import glob
import pandas as pd
import numpy as np
#
file_list = glob.glob(r'M:\Tiny_Ship\20211110_Data\pos\*\*.txt')
print(len(file_list))
# 5648 1065 1361
# 6766 1305 1589
n_bbox = np.array([]).reshape(0, 4)
for txt_name in file_list:
    if os.path.getsize(txt_name) > 2:
        bboxes = np.loadtxt(txt_name, float, usecols=[1, 2, 3, 4], ndmin=2)
        bboxes = np.clip(bboxes, a_min=0, a_max=256)
        if len(bboxes):
            bbox_w_h = bboxes[:, 2:4] - bboxes[:, 0:2]
            bbox_min = np.min(bbox_w_h, axis=0)
            if np.any(bbox_min[0] <= 0) or np.any(bbox_min[1] <= 0):
                print(txt_name)
            n_bbox = np.concatenate((n_bbox, bboxes), axis=0)
print(len(n_bbox))
# w_h = n_bbox[:, 2:4] - n_bbox[:, 0:2]
# n_bbox_mean = np.mean(w_h, axis=0)
# n_bbox_min = np.min(w_h, axis=0)
# n_bbox_max = np.max(w_h, axis=0)
# area = np.mean(np.prod(w_h, axis=1))
# print(n_bbox_mean)
# print(n_bbox_min)
# print(n_bbox_max)
# print(np.sqrt(area))


# file = r'L:\Code\TinyShipDetection\Tools\generate_dep_info\tiny_ship_for_pretrain.csv'
# file_list = pd.read_csv(file)
# n_bbox = np.array([]).reshape(0, 5)
# for idx, data in file_list.iterrows():
#     txt_name = data['label']
#     if os.path.getsize(txt_name) > 2:
#         bboxes = np.loadtxt(txt_name, float, ndmin=2)
#         bboxes = np.clip(bboxes, a_min=0, a_max=256)
#         if len(bboxes):
#             n_bbox = np.concatenate((n_bbox, bboxes), axis=0)
# w_h = n_bbox[:, 3:5] - n_bbox[:, 1:3]
# n_bbox_mean = np.mean(w_h, axis=0)
# n_bbox_min = np.min(w_h, axis=0)
# n_bbox_max = np.max(w_h, axis=0)
# area = np.mean(np.prod(w_h, axis=1))
# print(n_bbox_mean)
# print(n_bbox_min)
# print(n_bbox_max)
# print(np.sqrt(area))
#
# file_path = r'L:\Tiny_Ship\20211026RSAICP_Ship_Detection_Competition\RSAICP_Ship_Detection\train\mask'
# file_list = glob.glob(file_path + '/*.txt')
# n_bbox = np.array([]).reshape(0, 8)
# for txt_name in file_list:
#     if os.path.getsize(txt_name) > 2:
#         bboxes = np.loadtxt(txt_name, int, usecols=[1, 2, 3, 4, 5, 6, 7, 8], delimiter=',', ndmin=2)
#         if len(bboxes):
#             n_bbox = np.concatenate((n_bbox, bboxes), axis=0)
# w_h = n_bbox[:, 4:6] - n_bbox[:, 0:2]
# n_bbox_mean = np.mean(w_h, axis=0)
# n_bbox_min = np.min(w_h, axis=0)
# n_bbox_max = np.max(w_h, axis=0)
# area = np.mean(np.prod(w_h, axis=1))
# print(n_bbox_mean)
# print(n_bbox_min)
# print(n_bbox_max)
# print(np.sqrt(area))


# file_path = r'L:\Detection\GF_1_2\GF_1_2_Ship_Select'
# file_list = glob.glob(file_path + '/*.txt')
# n_bbox = np.array([]).reshape(0, 4)
# for txt_name in file_list:
#     if os.path.getsize(txt_name) > 2:
#         bboxes = np.loadtxt(txt_name, float, usecols=[1, 2, 3, 4], ndmin=2)
#         # bboxes = np.clip(bboxes, a_min=0, a_max=512)
#         if len(bboxes):
#             bbox_w_h = bboxes[:, 2:4] - bboxes[:, 0:2]
#             bbox_min = np.min(bbox_w_h, axis=0)
#             if np.any(bbox_min[0] <= 0) or np.any(bbox_min[1] <= 0):
#                 print(txt_name)
#             n_bbox = np.concatenate((n_bbox, bboxes), axis=0)
#
# w_h = n_bbox[:, 2:4] - n_bbox[:, 0:2]
# n_bbox_mean = np.mean(w_h, axis=0)
# n_bbox_min = np.min(w_h, axis=0)
# n_bbox_max = np.max(w_h, axis=0)
# area = np.mean(np.prod(w_h, axis=1))
# print(n_bbox_mean)
# print(n_bbox_min)
# print(n_bbox_max)
# print(np.sqrt(area))
