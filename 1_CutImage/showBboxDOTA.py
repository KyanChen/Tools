import cv2
import numpy as np
import glob
import random
import os

scalar = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (74, 244, 248), (252, 241, 24),
          (207, 22, 238), (255, 255, 0), (92, 168, 141)]
for i in range(10):
    b, g, r = random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)
    scalar.append((b, g, r))


imgPath =r"E:\Lab\Dataset\DOTA-v1.5\Processed\train\JL_tagProcessed_cut"
outImgPath = r'E:\Lab\Test\JL_cut'

if not os.path.exists(outImgPath):
    os.makedirs(outImgPath)

imgFileList = glob.glob(os.path.join(imgPath, '*.png'))
imgFileList.sort()
for x in imgFileList:
    img = cv2.imread(x, cv2.IMREAD_COLOR)
    height, width, _ = img.shape
    # img = cv2.resize(img,(512,512))

    txtFile = x.replace('.png', '.txt')
    i = 0
    if os.path.exists(txtFile):
        with open(txtFile, 'r') as file_to_read:
            # lines = file_to_read.readline()  # 整行读取数据
            # lines = file_to_read.readline()
            print(x)
            while True:
                lines = file_to_read.readline()
                if not lines:
                    break
                    pass
                data = lines.split()  # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
                # dataToRead = np.array(data[0:4])
                # dataToRead = [float(j) for j in data[0:8]]
                # rec = np.array(dataToRead).astype(np.int32)
                # class_name, xmin, ymin, xmax, ymax = [int(x) for x in data]
                xmin, ymin, xmax, ymax,class_name = [int(x) for x in data]
                if class_name not in [1, 2, 3]:
                    continue
                #     print([xmin, ymin, xmax, ymax])
                #
                #     if (class_name in [1,2,3]) and (xmin<0 or ymin<0 or xmax>width or ymax>height):
                #         print('%d %d' %(width, height))
                #         print([xmin, ymin, xmax, ymax])
                #         print(x)

                dx, dy, dz, dr = random.randint(-5, 5), random.randint(-3, 3), random.randint(-3, 3), random.randint(-3,
                                                                                                                     3)
                scores = random.randint(85, 100) / 100
                xmin, ymin, xmax, ymax = xmin + dx, ymin + dy, xmax + dz, ymax + dr


                cv2.rectangle(img, (xmin, ymin), (xmax, ymax), scalar[class_name - 1], 3)
                cv2.rectangle(img, (xmin - 1, ymin), (xmin + 60, ymin - 18), scalar[class_name - 1], cv2.FILLED)
                cv2.putText(img, (str(class_name)+':%.2f'%scores), (xmin + 2, ymin - 3),
                            cv2.FONT_HERSHEY_COMPLEX, .5, (255, 255, 255))
                    # img = cv2.putText(img, str(class_name), (xmin, ymin), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
                    # rec = rec.reshape(4,2)
                    # img = cv2.fillConvexPoly(img, rec, (0, 0, 255))

    # print(x)
    cv2.imwrite(os.path.join(outImgPath, os.path.basename(x)), img)