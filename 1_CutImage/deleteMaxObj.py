import cv2
import numpy as np
import glob
import random
import os
import shutil

scalar = [(0, 0, 255), (0, 255, 0), (255, 97, 108), (74, 244, 248), (252, 241, 24),
          (207, 22, 238), (255, 255, 0), (92, 168, 141)]
for i in range(10):
    b, g, r = random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)
    scalar.append((b, g, r))

imgPath = r"E:\Lab\Dataset\DOTA-v1.5\Processed\val\GoogleEarth_tagProcessed_cut"
outImgPath = r'E:\Lab\Dataset\DOTA-v1.5\Processed\val\in\out1'

if not os.path.exists(outImgPath):
    os.makedirs(outImgPath)

imgFileList = glob.glob(os.path.join(imgPath, '*.png'))
imgFileList.sort()
for x in imgFileList:
    img = cv2.imread(x, cv2.IMREAD_UNCHANGED)
    height, width, _ = img.shape
    # img = cv2.resize(img,(512,512))

    '''
    print(img.shape)
    img = np.expand_dims(img, axis=2)
    print(img.shape)
    img = np.concatenate([img, img, img], axis=-1)

    print(img.shape)
    '''
    txtFile = x.replace('.png', '.txt')
    i = 0
    if os.path.exists(txtFile):
        with open(txtFile, 'r') as file_to_read:
            # lines = file_to_read.readline()  # 整行读取数据
            # lines = file_to_read.readline()
            while True:
                lines = file_to_read.readline()
                if not lines:
                    break
                    pass
                data = lines.split()  # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
                # dataToRead = np.array(data[0:4])
                # dataToRead = [float(j) for j in data[0:8]]
                # rec = np.array(dataToRead).astype(np.int32)
                class_name, xmin, ymin, xmax, ymax = [int(x) for x in data]
                xmin, ymin, xmax, ymax, class_name = [int(x) for x in data]
                if (class_name in [1, 2, 3]) and (xmin < 0 or ymin < 0 or xmax > width or ymax > height):

                    print(x)
                    os.remove(x)
                    file_to_read.close()
                    os.remove(txtFile)
                    break
                if (class_name in [1, 2, 3]) and ((xmax-xmin)>0.8*width or(ymax-ymin)> 0.8*height):
                    print(x)
                    os.remove(x)
                    file_to_read.close()
                    os.remove(txtFile)
                    break

