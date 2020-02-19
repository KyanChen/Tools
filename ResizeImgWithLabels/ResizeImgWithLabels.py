import os
from PIL import Image
import shutil
import glob

imgFormat = '.jpg'
toSize = (512, 512)

samples_path = r'G:\ObjectDetection\ObjectDetectionCode\TailMineDetection\dataset\negativeSamples'

imgnameList = glob.glob(os.path.join(samples_path, '*%s' % imgFormat))

for imgname in imgnameList:
    imgPath = os.path.join(samples_path, imgname)
    try:
        img = Image.open(imgPath)

    except:
        continue
    width, height = img.size
    if width == toSize[0] and height == toSize[1]:
        continue
    img = img.resize(toSize, Image.BICUBIC)
    os.remove(imgPath)
    img.save(imgPath)
    labelPath = imgPath.replace(imgFormat, '.txt')
    bboxList = []
    with open(labelPath, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()  # 整行读取数据
            if not lines:
                break
                pass
            data = lines.split()  # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
            # dataToRead = list(map(int, data[1:]))
            classNum, x1, y1, x2, y2 = [int(float(x)) for x in data]
            widthRatio, heightRatio = toSize[0]/width, toSize[1]/height
            dataToRead = [classNum, widthRatio * x1, heightRatio * y1, widthRatio * x2, heightRatio * y2]
            dataToRead = [int(x) for x in dataToRead]
            bboxList.append(dataToRead)
    with open(labelPath, 'w') as file_to_write:
        for i in range(0, len(bboxList)):
            classNum, x1, y1, x2, y2 = bboxList[i]
            lineToWrite = str(classNum) + ' ' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + '\n'
            file_to_write.writelines(lineToWrite)