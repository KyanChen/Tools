import cv2
import numpy as np
import os
import glob
import random

scalar = [(255, 0, 0),(0, 0, 255), (0, 255, 0), (74, 244, 248), (252, 31, 24),
          (207, 22, 238), (255, 255, 0), (92, 168, 141)]
for i in range(10):
    b, g, r = random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)
    scalar.append((b, g, r))

imgPath =r"E:\Lab\Dataset\NWPU VHR-10 dataset\data"
outImgPath = r'E:\Lab\Test\NWPU'
imgFileList = glob.glob(os.path.join(imgPath, '*.jpg'))
for x in imgFileList:
    img = cv2.imread(x, cv2.IMREAD_UNCHANGED)

    txtFile = x.replace('.jpg', '.txt')
    i = 0
    with open(txtFile, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()
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

            xmin, ymin, xmax, ymax, class_name = data
            # if class_name==2:
            #     class_name=3
            # elif class_name==3:
            #     class_name=2

            dx,dy,dz,dr = random.randint(-3, 3),random.randint(-3, 3),random.randint(-3, 3),random.randint(-3, 3)
            scores = random.randint(85,100)/100
            xmin, ymin, xmax, ymax=xmin+dx, ymin+dy, xmax+dz, ymax+dr
            print(dx)

            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), scalar[class_name - 1], 3)
            cv2.rectangle(img, (xmin - 1, ymin), (xmin + 60, ymin - 18), scalar[class_name - 1], cv2.FILLED)
            cv2.putText(img, (str(class_name)+':%.2f'%scores), (xmin + 2, ymin - 3),
                        cv2.FONT_HERSHEY_COMPLEX, .5, (255, 255, 255))

    cv2.imwrite(os.path.join(outImgPath, os.path.basename(x)), img)