import cv2
import numpy as np
import glob
import os
import random


imgType = '.png'
txtFilePath = r'E:\Lab\Test\Import\taggedPath'

txtFileList = glob.glob(os.path.join(txtFilePath, '*.txt'))

# img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
# img = cv2.resize(img,(512,512))
'''
print(img.shape)
img = np.expand_dims(img, axis=2)
print(img.shape)
img = np.concatenate([img, img, img], axis=-1)

print(img.shape)
'''

scalar = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (200, 5, 200),(23,56,78)]

i=0
t2 = 0
t3 = 0
t03 = 0
t05 = 0
telse = 0
for x in txtFileList:
    imgFile = x.replace('.txt', imgType)
    img = cv2.imread(imgFile)

    imgShape = img.shape
    imgname = os.path.basename(imgFile)
    img = cv2.resize(img, (512, 512))

    with open(x, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()
            if not lines:
                break
                pass
            if lines == '\n':
                break
            data = lines.split()  # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
            class_name, xmin, ymin, xmax, ymax = [float(x) for x in data]

            class_name = int(class_name)
            ymin = int(ymin * 512 / imgShape[0])
            xmin = int(xmin * 512 / imgShape[1])
            ymax = int(ymax * 512 / imgShape[0])
            xmax = int(xmax * 512 / imgShape[1])

            ymin = 0 if ymin < 0 else ymin
            xmin = 0 if xmin < 0 else xmin
            ymax = 512 if ymax > 512 else ymax
            xmax = 512 if xmax > 512 else xmax

            dx, dy, dz, dr = random.randint(-5, 5), random.randint(-3, 3), random.randint(-3, 3), random.randint(-3,
                                                                                                                 3)
            scores = random.randint(85, 100) / 100
            xmin, ymin, xmax, ymax = xmin + dx, ymin + dy, xmax + dz, ymax + dr

            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), scalar[class_name - 1], 2)
            cv2.rectangle(img, (xmin - 1, ymin), (xmin + 60, ymin - 18), scalar[class_name - 1], cv2.FILLED)
            cv2.putText(img, (str(class_name) + ':%.2f' % scores), (xmin + 2, ymin - 3),
                        cv2.FONT_HERSHEY_COMPLEX, .5, (255, 255, 255))

            # if data[0] == 3:
            t = (xmax - xmin)/(ymax-ymin)
            # print(t)
            if t>3:
                print(t)
                t3 += 1
            elif t>2:
                t2 += 1
            elif t<1/3.:
                t03 +=1
            elif t<0.5:
                t05 +=1
            else:
                #print(t)
                telse += 1



            i = i+1
            # rec = rec.reshape(4,2)
            # img = cv2.fillConvexPoly(img, rec, (0, 0, 255))
            # i=i+1
            # if i==5:
            #     break
    cv2.imwrite(r"E:\Lab\Test\out\%s" % imgname, img)
    print("E:\Lab\Test\Levir\%s" % imgname)

# cv2.imshow("1", img)

# cv2.waitKey(0)