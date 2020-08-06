import os
import shutil
import math
import numpy as np
import cv2
from tqdm import tqdm
import glob


class ShowBboxes(object):
    def __init__(self, in_path, out_path, img_format):
        self.in_path = in_path
        self.out_path = out_path
        self.img_format = img_format
        if not os.path.exists(self.out_path):
            os.makedirs(self.out_path)

    def get_file_list(self):
        file_list = glob.glob(self.in_path + '/*.%s' % self.img_format)
        return file_list

    def readTag(self, file_name):
        bbox_list = []
        if not os.path.exists(file_name):
            print("file do not exist")
            return bbox_list
        with open(file_name, 'r') as file_to_read:
            while True:
                lines = file_to_read.readline()  # 整行读取数据
                if not lines:
                    break
                data = lines.split()  # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
                # dataToRead = list(map(int, data[1:]))
                dataToRead = [int(float(x)) for x in data[:-1]]
                bbox_list.append(dataToRead)
        return bbox_list

    def draw_bboxes(self):
        img_file_list = self.get_file_list()
        for img_file in img_file_list:
            txt_file = img_file.replace(self.img_format, 'txt')
            bboxes = self.readTag(txt_file)
            img = cv2.imread(img_file)
            if len(bboxes) == 0:
                continue
            for bbox in bboxes:
                x1, y1, x2, y2 = bbox
                img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.imwrite(self.out_path+'/'+os.path.basename(img_file), img)


if __name__ == '__main__':
    in_path = r'/Users/keyanchen/Files/Code/电子所/Pieces'
    out_path = r'/Users/keyanchen/Files/Code/电子所/results'
    img_type = 'tiff'

    showBboxes = ShowBboxes(in_path, out_path, img_type)
    showBboxes.draw_bboxes()