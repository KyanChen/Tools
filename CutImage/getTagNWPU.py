import cv2
import numpy as np
import os
import glob
import random



imgPath =r"E:\Lab\Dataset\NWPU VHR-10 dataset\PositiveEvaluation"
imgFileList = glob.glob(os.path.join(imgPath, '*.jpg'))
for x in imgFileList:
    img = cv2.imread(x, cv2.IMREAD_UNCHANGED)
    txtFile = x.replace('.jpg', '.txt')
    bboxList = []

    with open(txtFile, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()  # 整行读取数据
            if not lines:
                break
                pass
            if lines == '\n':
                break
            data = lines.replace('(', '')
            data = data.replace(')', '')
            data = data.replace('\n', '')
            data = data.split(',')
            data = [int(x) for x in data]
            bboxList.append(data)

    with open(txtFile, 'w') as file:
        for i in range(0, len(bboxList)):
            for j in range(0, 4):
                ch = bboxList[i][j]
                file.write(str(ch) + ' ')
            file.write(str(bboxList[i][4]))
            file.write('\n')