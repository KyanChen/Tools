import os
import shutil
import math
import numpy as np
import cv2
from tqdm import tqdm
import glob
import json


results = None
with open(r"D:\Ship\RSAICP_Ship_Detection\test\ship_results_down2_iter81.json", 'r', encoding='utf-8') as json_file:
    results = json.load(json_file)

def jaccard_numpy(rect, bboxes):
    intersection_left_top = np.maximum(rect[:2], bboxes[:, :2])
    intersection_right_bottom = np.minimum(rect[2:], bboxes[:, 2:])
    intersection_w_h = np.maximum(intersection_right_bottom - intersection_left_top + 1, 0)
    intersection = intersection_w_h[:, 0] * intersection_w_h[:, 1]
    rect_area = (rect[2] - rect[0] + 1) * (rect[3] - rect[1] + 1)
    bboxes_area = (bboxes[:, 2] - bboxes[:, 0] + 1) * (bboxes[:, 3] - bboxes[:, 1] + 1)
    iou = intersection / (rect_area + bboxes_area - intersection)
    return iou

class ShowBboxes(object):
    def __init__(self, img_path, save_path, img_format):
        self.img_path = img_path
        self.save_path = save_path
        self.img_format = img_format
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def get_file_list(self):
        file_list = glob.glob(self.img_path + '/GF1_1*.%s' % self.img_format)
        return file_list

    def readTag(self, file_name):
        bboxes = np.loadtxt(file_name, float, usecols=[1, 2, 5, 6], delimiter=',',  ndmin=2)
        return bboxes

    def draw_bboxes(self):
        img_file_list = self.get_file_list()
        for idx, img_file in enumerate(img_file_list):
            # txt_file = img_file.replace(self.img_format, 'txt')
            # bboxes_GT = self.readTag(txt_file) / 2
            n_bboxes = results[idx]['labels']

            bboxes = []
            for box in n_bboxes:
                l, t = box['points'][0]
                r, b = box['points'][2]
                bboxes.append([l/2, t/2, r/2, b/2])

            img_ori = cv2.imread(img_file)
            h, w, c = img_ori.shape

            img_ori = cv2.resize(img_ori, (int(w/2), int(h/2)))
            h = int(h/2)
            w = int(w/2)
            img = img_ori.copy()
            # if len(bboxes) == 0:
            #     continue
            for bbox in bboxes:
                # x1, y1, x2, y2 = bbox  # 逆时针
                # img = cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), thickness=2)
                # img = cv2.line(img, (x2, y2), (x3, y3), (0, 0, 255), thickness=2)
                # img = cv2.line(img, (x3, y3), (x4, y4), (0, 0, 255), thickness=2)
                # img = cv2.line(img, (x4, y4), (x1, y1), (0, 0, 255), thickness=2)
                # cx, cy = (x1 + x2)/2, (y1 + y2)/2
                # w, h = (x2 - x1), (y2 - y1)
                # w = 0.6*w
                # h = 0.6*h
                # l = cx - w/2
                # t = cy - h/2
                # r = cx + w/2
                # b = cy + h/2
                l, t, r, b = bbox
                img = cv2.rectangle(img, (int(l), int(t)), (int(r), int(b)), (0, 0, 255), 4)
                # img = cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            #     iou = jaccard_numpy(bbox, bboxes_GT)
            #     if any(iou > 0.1):
            #         continue
            #     else:
            #         cx, cy = (l+r)/2, (t+b)/2
            #         startx = int(cx - 128)
            #         starty = int(cy - 128)
            #         if startx < 0:
            #             startx = 0
            #         if starty < 0:
            #             starty = 0
            #         if startx + 256 > w:
            #             startx = w - 256
            #         if starty + 256 > h:
            #             starty = h - 256
            #         img_crop = img_ori[starty:starty+256, startx:startx+256, :]
            #         file_dir = os.path.dirname(save_path) + '/neg_samples_iter4/' + os.path.basename(img_file).replace('.png', '')
            #         os.makedirs(file_dir, exist_ok=True)
            #         cv2.imwrite(file_dir + f'/{startx}_{starty}.png', img_crop)
            #
            # for bbox in bboxes_GT:
            #     # x1, y1, x2, y2, x3, y3, x4, y4 = bbox  # 逆时针
            #     # l, t, r, b = x1, y1, x3, y3
            #     l, t, r, b = bbox
            #
            #     # cx, cy = (l+r)/2, (t+b)/2
            #     # startx = int(cx - 256)
            #     # starty = int(cy - 256)
            #     # if startx < 0:
            #     #     startx = 0
            #     # if starty < 0:
            #     #     starty = 0
            #     # if startx + 512 > w:
            #     #     startx = w - 512
            #     # if starty + 512 > h:
            #     #     starty = h - 512
            #     # img_crop = img_ori[starty:starty+512, startx:startx+512, :]
            #     # file_dir = os.path.dirname(save_path) + '/pos_samples_center/' + os.path.basename(img_file).replace('.png', '')
            #     # os.makedirs(file_dir, exist_ok=True)
            #     # img_file_name = file_dir + f'/{startx}_{starty}.png'
            #     # cv2.imwrite(img_file_name, img_crop)
            #     #
            #     # rect = np.array([startx, starty, startx+512, starty+512])
            #     # centers = (bboxes_GT[:, 0:2] + bboxes_GT[:, 2:]) / 2.0
            #     # m1 = (rect[0] < centers[:, 0]) * (rect[1] < centers[:, 1])
            #     # m2 = (rect[2] > centers[:, 0]) * (rect[3] > centers[:, 1])
            #     # mask = m1 * m2
            #     # current_boxes = None
            #     # if mask.any():
            #     #     current_boxes = bboxes_GT[mask, :].copy()
            #     #     current_boxes[:, 0:2] = np.maximum(current_boxes[:, 0:2], rect[:2])
            #     #     current_boxes[:, 0:2] -= rect[:2]
            #     #     current_boxes[:, 2:] = np.minimum(current_boxes[:, 2:], rect[2:])
            #     #     current_boxes[:, 2:] -= rect[:2]
            #     # if current_boxes is None:
            #     #     with open(img_file_name.replace('png', 'txt'), 'w') as f:
            #     #         pass
            #     # else:
            #     #     current_boxes = np.clip(current_boxes, a_min=0, a_max=1e10)
            #     #     current_boxes = np.insert(current_boxes, 0, values=0, axis=1)
            #     #     np.savetxt(img_file_name.replace('png', 'txt'), current_boxes,
            #     #                fmt='%d %.4f %.4f %.4f %.4f')
            #
            #
            #     img = cv2.rectangle(img, (int(l), int(t)), (int(r), int(b)), (0, 255, 0), 4)
            cv2.imwrite(self.save_path+'/vis_'+os.path.basename(img_file), img)


if __name__ == '__main__':
    img_path = r'M:\Work\Exp\LargeScaleImg'
    save_path = r'M:\Work\Exp\LargeScaleImg'
    img_type = 'png'

    showBboxes = ShowBboxes(img_path, save_path, img_type)
    showBboxes.draw_bboxes()