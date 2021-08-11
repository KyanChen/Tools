import os
import shutil
import math
import numpy as np
import cv2
from tqdm import tqdm
import glob

mul = lambda arg1: arg1[0]*arg1[1]
add = lambda arg1: arg1[0]+arg1[1]

imgType = '.tiff'

class DatasetNormalize:
    GoogleEarthNum = 0
    GF_2Num=0
    JL_1Num=0
    classNumCal = np.zeros([18])

    # big image is [Bx, By], small image is [Sx, Sy]
    # BigImgSize, smallWidth
    def __init__(self, inPath, outPath, **kwargs):
        self.inPath = inPath
        self.outPath = outPath
        self.PreTxtInfor = ''

        if os.path.exists(self.outPath):
            shutil.rmtree(self.outPath)
        os.makedirs(self.outPath)
        for key, value in kwargs.items():
            setattr(self, key, value)

    # 获取指定后缀名的文件列表，输入为文件夹路径
    def getFileList(self, filePath):
        fileList = []
        list = os.listdir(filePath)
        for i in range(0, len(list)):
            path = os.path.join(filePath, list[i])
            if os.path.isfile(path):
                file_path = os.path.split(path)  # 分割出目录与文件
                lists = file_path[1].split('.')  # 分割出文件与文件扩展名
                file_ext = lists[-1]  # 取出后缀名(列表切片操作)
                img_ext = ['bmp', 'jpeg', 'gif', 'psd', 'png', 'jpg', 'tif', 'tiff']
                if file_ext in img_ext:
                    fileList.append(path)
        return fileList

    def readImg(self, fileName):
        img = cv2.imread(fileName, cv2.IMREAD_LOAD_GDAL)
        return img, img.shape[1], img.shape[0]

    def maxXYPieces(self, BigWidth, BigHeight):
        maxXPiece = round(float(BigWidth) / self.smallWidth)
        maxYPiece = round(float(BigHeight) / self.smallHeight)


        return [maxXPiece, maxYPiece]

    def pairImgTxt(self, filePath):
        imgFileList = glob.glob(os.path.join(filePath, '*%s' % imgType))
        pbar1 = tqdm(total=len(imgFileList))
        for i in range(len(imgFileList)):
            pbar1.update(1)
            imgFile = imgFileList[i]

            self.saveImgTo3D(imgFile)
            txtFile = imgFile.replace(imgType, '.txt')
            if not os.path.exists(txtFile):
                with open(txtFile, 'w') as fileToWrite:
                    fileToWrite.close()
        pbar1.close()



    # 得到切片和对应标签
    def getPiece(self):
        # 图片文件列表
        imgFileList = self.getFileList(self.inPath)

        pbar = tqdm(total=len(imgFileList))
        for i in range(len(imgFileList)):
            pbar.update(1)
            imgFile = imgFileList[i]
            txtFile = imgFile.replace(imgType, '.txt')

            bboxList = self.readTag(txtFile)
            img, width, height = self.readImg(imgFileList[i])
            img = img[:, :, :3]
            maxPiecesX, maxPiecesY = self.maxXYPieces(width, height)

            flag = False
            curXPiece, curYPiece = 0, 0
            if maxPiecesX <= 1 and maxPiecesY <= 1:
                shutil.copy(imgFile, self.outPath)
                shutil.copy(txtFile, self.outPath)
                continue

            elif maxPiecesX <= 1 and maxPiecesY > 1:
                curXPiece, curYPiece = 0, 0
                while curYPiece < maxPiecesY:
                    curY = curYPiece * self.smallHeight
                    if curYPiece < maxPiecesY-1:
                        imgCrop = img[curY: curY + self.smallHeight]
                    elif curYPiece == maxPiecesY-1:
                        imgCrop = img[curY:]
                    imgBasename = os.path.basename(imgFile)
                    imgCropFile = os.path.join(self.outPath,
                                               (imgBasename.replace(imgType, '') + '_' + str(curYPiece) + '_'
                                                + str(curXPiece) + imgType))
                    cv2.imwrite(imgCropFile, imgCrop)
                    curYPiece += 1
            elif maxPiecesX > 1 and maxPiecesY <= 1:
                curXPiece, curYPiece = 0, 0
                while curXPiece < maxPiecesX:
                    curX = curXPiece * self.smallWidth
                    if curXPiece < maxPiecesX-1:
                        imgCrop = img[0:, curX: curX + self.smallWidth]
                    elif curXPiece == maxPiecesX-1:
                        imgCrop = img[0:, curX:]
                    imgBasename = os.path.basename(imgFile)
                    imgCropFile = os.path.join(self.outPath,
                                               (imgBasename.replace(imgType, '') + '_' + str(curYPiece) + '_'
                                                + str(curXPiece) + imgType))
                    cv2.imwrite(imgCropFile, imgCrop)
                    curXPiece += 1

            elif maxPiecesX > 0 and maxPiecesY > 0:
                curXPiece, curYPiece = 0, 0
                while curYPiece < maxPiecesY:
                    curX = curXPiece * self.smallWidth
                    curY = curYPiece * self.smallHeight
                    # 普通情况
                    imgCrop = img[curY: curY + self.smallHeight, curX: curX + self.smallWidth]
                    if curXPiece == maxPiecesX-1:
                        imgCrop = img[curY: curY + self.smallHeight, curX:]
                        flag = True

                    if curYPiece == maxPiecesY-1:
                        imgCrop = img[curY:, curX: curX + self.smallWidth]
                    if curYPiece == maxPiecesY - 1 and curXPiece == maxPiecesX-1:
                        imgCrop = img[curY:, curX:]
                    imgBasename = os.path.basename(imgFile)
                    imgCropFile = os.path.join(self.outPath,
                                               (imgBasename.replace(imgType, '') + '_' + str(curYPiece) + '_'
                                                + str(curXPiece) + imgType))
                    cv2.imwrite(imgCropFile, imgCrop)
                    curXPiece += 1
                    if flag:
                        flag = False
                        curYPiece += 1
                        curXPiece = 0
            for k in range(len(bboxList)):
                # print(width, height)
                # print(bboxList[k])
                # x_1, y_1, x_2, y_2, classNum = bboxList[k]
                classNum = 1
                x_1, y_1, x_2, y_2 = bboxList[k]
                if x_1<0 or y_1<0 or x_2>width or y_2>height:
                    continue
                x = math.floor(float(x_1) / self.smallWidth)
                if (maxPiecesX-1>0) and (x > maxPiecesX-1) or (maxPiecesX<=1 and x>=1) or ((x == maxPiecesX-1) and (maxPiecesX > math.floor(float(width) / self.smallWidth))):
                    x = maxPiecesX-1
                y = math.floor(float(y_1) / self.smallHeight)
                if (maxPiecesY-1>0) and (y > maxPiecesY-1) or (maxPiecesY<=1 and y>=1) or ((y == maxPiecesY-1) and (maxPiecesY > math.floor(float(height) / self.smallHeight))):
                    y = maxPiecesY-1

                deltaX = x_2-x_1
                deltaY = y_2-y_1


                imgBasename = os.path.basename(imgFile)
                imgLabelFile = os.path.join(self.outPath, (imgBasename.replace(imgType, '') + '_'
                                                           + str(y) + '_' + str(x) + '.txt'))

                x1 = x_1 - self.smallWidth * x
                y1 = y_1 - self.smallHeight * y
                x2 = x1 + deltaX
                y2 = y1 + deltaY
                imgCropFile = imgLabelFile.replace('.txt', imgType)
                imgCrop = cv2.imread(imgCropFile)
                widthCrop, heightCrop = imgCrop.shape[1], imgCrop.shape[0]

                with open(imgLabelFile, 'a') as fileToWrite:
                    x2 = widthCrop if x2 > widthCrop else x2
                    y2 = heightCrop if y2 > heightCrop else y2
                    stringTxt = str(int(x1)) + ' ' + str(int(y1)) + ' ' + str(int(x2)) + ' ' + str(int(y2)) + ' '\
                                + str(classNum)+ '\n'
                    fileToWrite.writelines(stringTxt)
                # 恢复
                x2 = x1 + deltaX
                y2 = y1 + deltaY
                if x2 > widthCrop and y2 < heightCrop:
                    imgBasename = os.path.basename(imgFile)
                    imgLabelFile = os.path.join(self.outPath, (imgBasename.replace(imgType, '') + '_'
                                                               + str(y) + '_' + str(x+1) + '.txt'))
                    with open(imgLabelFile, 'a') as fileToWrite:
                        x2 = x2 - widthCrop
                        stringTxt = str(int(0.0)) + ' ' + str(int(y1)) + ' ' + str(int(x2)) + ' ' + str(int(y2)) + ' ' \
                                    + str(classNum)+'\n'
                        fileToWrite.writelines(stringTxt)

                x2 = x1 + deltaX
                y2 = y1 + deltaY
                if x2 < widthCrop and y2 > heightCrop:
                    imgBasename = os.path.basename(imgFile)
                    imgLabelFile = os.path.join(self.outPath, (imgBasename.replace(imgType, '') + '_'
                                                               + str(y+1) + '_' + str(x) + '.txt'))
                    with open(imgLabelFile, 'a') as fileToWrite:
                        y2 = y2 - heightCrop
                        stringTxt = str(int(x1)) + ' ' + str(int(0.0)) + ' ' + str(int(x2)) + ' ' + str(int(y2)) + ' ' \
                                    + str(classNum)+'\n'
                        fileToWrite.writelines(stringTxt)

                x2 = x1 + deltaX
                y2 = y1 + deltaY
                if x2 > widthCrop and y2 > heightCrop:
                    imgBasename = os.path.basename(imgFile)
                    imgLabelFile = os.path.join(self.outPath, (imgBasename.replace(imgType, '') + '_'
                                                               + str(y) + '_' + str(x+1) + '.txt'))
                    with open(imgLabelFile, 'a') as fileToWrite:
                        x2 = x2 - widthCrop
                        stringTxt = str(int(0.0)) + ' ' + str(int(y1)) + ' ' + str(int(x2)) + ' ' + str(int(heightCrop))\
                                    +' '+str(classNum)+ '\n'
                        fileToWrite.writelines(stringTxt)

                    imgLabelFile = os.path.join(self.outPath, (imgBasename.replace(imgType, '') + '_'
                                                               + str(y+1) + '_' + str(x) + '.txt'))

                    x2 = x1 + deltaX
                    y2 = y1 + deltaY
                    with open(imgLabelFile, 'a') as fileToWrite:
                        y2 = y2 - heightCrop
                        stringTxt = str(int(x1)) + ' ' + str(int(0)) + ' ' + str(int(widthCrop)) + ' ' + str(int(y2)) + ' ' \
                                    + str(classNum)+ '\n'
                        fileToWrite.writelines(stringTxt)

                    imgLabelFile = os.path.join(self.outPath, (imgBasename.replace(imgType, '') + '_'
                                                               + str(y + 1) + '_' + str(x + 1) + '.txt'))

                    x2 = x1 + deltaX
                    y2 = y1 + deltaY
                    with open(imgLabelFile, 'a') as fileToWrite:
                        x2 = x2 - widthCrop
                        y2 = y2 - heightCrop
                        stringTxt = str(int(0.0)) + ' ' + str(int(0.0)) + ' ' + str(int(x2)) + ' ' + str(int(y2))\
                                    + ' '+ str(classNum)+ '\n'
                        fileToWrite.writelines(stringTxt)
        pbar.close()
        self.pairImgTxt(self.outPath)
        # self.deleteMaxBbox(self.outPath)


    def deleteMaxBbox(self, inPath):

        imgFileList = glob.glob(os.path.join(inPath,'*%s' % imgType))
        pbar = tqdm(total=len(imgFileList))
        for x in imgFileList:
            pbar.update(1)
            img = cv2.imread(x, cv2.IMREAD_UNCHANGED)
            height, width, _ = img.shape
            txtFile = x.replace(imgType, '.txt')
            if os.path.exists(txtFile):
                with open(txtFile, 'r') as file_to_read:
                    while True:
                        lines = file_to_read.readline()
                        if not lines:
                            break
                            pass
                        data = lines.split()  # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
                        xmin, ymin, xmax, ymax, class_name = [int(x) for x in data]
                        if (class_name in [1, 2, 3]) and (xmin < 0 or ymin < 0 or xmax > width or ymax > height):
                            os.remove(x)
                            file_to_read.close()
                            os.remove(txtFile)
                            break
                        if (class_name in [1, 2, 3]) and ((xmax - xmin) > 0.8 * width or (ymax - ymin) > 0.8 * height):
                            os.remove(x)
                            file_to_read.close()
                            os.remove(txtFile)
                            break
        pbar.close()

    # 获取标签到list
    def readTag(self, fileName):
        bboxList = []
        # file_path = os.path.splitext(filePathName)  # 分割出文件扩展名
        txtName = fileName
        if not os.path.exists(txtName):
            print("file do not exist")
            exit()
            # file_to_read = open(txtPathName, 'w')
            # file_to_read.close()
        with open(txtName, 'r') as file_to_read:
            # lines = file_to_read.readline()
            # self.PreTxtInfor = lines
            # lines = file_to_read.readline()
            # self.PreTxtInfor = self.PreTxtInfor + lines
            while True:
                lines = file_to_read.readline()  # 整行读取数据
                if not lines:
                    break
                    pass
                data = lines.split() # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
                # dataToRead = list(map(int, data[1:]))
                dataToRead = [int(float(x)) for x in data[1:]]
                bboxList.append(dataToRead)
        return bboxList


    # divide class
    def processTagForDOTA(self):
        className = ['plane', 'ship', 'storage-tank', 'baseball-diamond', 'tennis-court', 'basketball-court',
                     'ground-track-field', 'harbor',  'bridge', 'small-vehicle', 'large-vehicle', 'helicopter',
                     'swimming-pool', 'roundabout', 'soccer-ball-field', 'container-crane']
        classNumCal = np.zeros(16, dtype=np.int64)

        imgFileList = self.getFileList(self.inPath)

        pbar = tqdm(total=len(imgFileList))
        for i in range(len(imgFileList)):
            pbar.update(1)
            img = cv2.imread(imgFileList[i])
            height, width, _ = img.shape

            txtFile = imgFileList[i].replace(imgType, '.txt')
            txtName = os.path.basename(txtFile)
            outTxtPath = os.path.join(self.outPath, txtName)
            if not os.path.exists(txtFile):
                print("file do not exist:%s" % txtFile)
                exit()
            with open(txtFile, 'r') as file_to_read:
                with open(outTxtPath, 'w') as file_to_write:
                    lines = file_to_read.readline()  # 整行读取数据
                    lines = file_to_read.readline()
                    while True:
                        lines = file_to_read.readline()
                        if not lines:
                            break
                            pass
                        data = lines.split()  # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
                        x_1, y_1, x_2, y_2 = int(float(data[0])), int(float(data[1])), int(float(data[4])), int(float(data[5]))
                        # left,top,right,bottom
                        if x_1 <= x_2:
                            if y_1 <= y_2:
                                x1, y1, x2, y2 = x_1, y_1, x_2, y_2
                            elif y_1 > y_2:
                                x1, y1, x2, y2 = x_1, y_2, x_2, y_1
                        elif x_1 > x_2:
                            if y_1 <= y_2:
                                x1, y1, x2, y2 = x_2, y_1, x_1, y_2
                            elif y_1 > y_2:
                                x1, y1, x2, y2 = x_2, y_2, x_1, y_1

                        # 数据是否有效
                        if x1>width or y1>height:
                            continue
                        flag = False
                        # print('W:'+ str(width))
                        # print('H:'+str(height))
                        if x1 < 0:

                            x1 = 0
                            flag =True
                        if y1 < 0:

                            y1 = 0
                            flag = True
                        if x2 > width:

                            x2 = width
                            flag = True


                        if y2 > height:

                            y2 = height
                            flag = True

                        # if flag:
                        #     img = cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,255), 3)
                        #     print(str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2))
                        #     print(data[8])
                        #     img = cv2.resize(img,(int(width*0.5), int(height*0.5)))
                        #     cv2.imshow("1", img)
                        #     cv2.waitKey(0)
                        s = str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)

                        try:
                            classNumCal[className.index(data[8])] += 1
                            classNum = className.index(data[8]) + 1
                        except:
                            print(data[8])
                            return

                        s = s+ ' ' + str(classNum) + '\n'
                        file_to_write.writelines(s)
            shutil.copy(imgFileList[i], self.outPath)

        sourceInfor = (self.outPath).split('\\')
        txtInforToWrite = os.path.abspath(os.path.join(self.outPath, r'..\\%s_infor.txt' % sourceInfor[-1]))
        with open(txtInforToWrite, 'w') as fileToWrite:
            for i, data in enumerate(classNumCal):
                dataLine = className[i] + ':' + str(data) + '\n'
                fileToWrite.writelines(dataLine)
        pbar.close()

    # divide different image source
    def divideSource(self):
        num =[0, 0, 0, 0]
        source = ['GoogleEarth', 'GF', 'JL', 'NULL']
        imgFileList = self.getFileList(self.inPath)
        for i in range(len(imgFileList)):
            txtFile = imgFileList[i].replace(imgType, '.txt')
            if not os.path.exists(txtFile):
                print("file do not exist")
                exit()
            with open(txtFile, 'r') as file_to_read:
                lines = file_to_read.readline()  # 整行读取数据
                if not lines:
                    break
                    pass
                data = lines.split(":")  # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
                dataToRead = data[1].replace('\n', '')
                pass
            try:
                num[source.index(dataToRead)] += 1
            except:
                print("value null")
                num[3] += 1

            dataToWritePath = os.path.join(self.outPath, dataToRead)
            if not os.path.exists(dataToWritePath):
                os.mkdir(dataToWritePath)
            imgFileToWrite = os.path.join(dataToWritePath, os.path.basename(imgFileList[i]))
            txtFileToWrite = imgFileToWrite.replace(imgType, '.txt')
            if os.path.exists(imgFileToWrite):
                os.remove(imgFileToWrite)
            if os.path.exists(txtFileToWrite):
                os.remove(txtFileToWrite)
            shutil.copy(imgFileList[i], dataToWritePath)
            shutil.copy(txtFile, dataToWritePath)

        txtInforToWrite = os.path.join(self.outPath, r'infor.txt')
        with open(txtInforToWrite, 'w') as fileToWrite:
            for i, data in enumerate(num):
                dataLine = source[i] +  ':' + str(data) +'\n'
                fileToWrite.writelines(dataLine)

    def deleteTxt(self):
        fileList = []
        list = os.listdir(self.outPath)
        for i in range(0, len(list)):
            path = os.path.join(self.outPath, list[i])
            if os.path.isfile(path):
                file_path = os.path.split(path)  # 分割出目录与文件
                lists = file_path[1].split('.')  # 分割出文件与文件扩展名
                file_ext = lists[-1]  # 取出后缀名(列表切片操作)
                img_ext = ['txt']
                if file_ext in img_ext:
                    fileList.append(path)
        for i in range(len(fileList)):
            imgFile = fileList[i].replace('.txt', imgType)
            if os.path.exists(imgFile):
                pass
            else:
                print(fileList[i])
                os.remove(fileList[i])

    def saveImgTo3D(self, imgPath):
        if os.path.isfile(imgPath):
            img = cv2.imread(imgPath)
            cv2.imwrite(imgPath, img)
        else:
            fileList = self.getFileList(imgPath)
            for i in range(len(fileList)):
                img = cv2.imread(fileList[i])
                cv2.imwrite(fileList[i], img)

    def caculateInformation(self, imgPath):
        fileList = []
        totalObj = 0
        totalNumClasses = [0, 0, 0]
        list = os.listdir(imgPath)
        for i in range(0, len(list)):
            path = os.path.join(imgPath, list[i])
            if os.path.isfile(path):
                file_path = os.path.split(path)  # 分割出目录与文件
                lists = file_path[1].split('.')  # 分割出文件与文件扩展名
                file_ext = lists[-1]  # 取出后缀名(列表切片操作)
                img_ext = ['txt']
                if file_ext in img_ext:
                    fileList.append(path)
        for i in range(len(fileList)):
            txtFile = fileList[i]
            with open(txtFile, 'r') as file_to_read:
                while True:
                    lines = file_to_read.readline()  # 整行读取数据
                    if not lines:
                        break
                        pass
                    totalObj +=1
                    data = lines.split()  # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
                    dataToRead = [int(x) for x in data]
                    totalNumClasses[dataToRead[0]-1] += 1
                    pass
        print(totalObj)
        print(totalNumClasses)

    def caculateInformationForDOTA(self, imgPath):
        fileList = []
        gsdList = []
        imgSizeList = []

        list = os.listdir(imgPath)
        for i in range(0, len(list)):
            path = os.path.join(imgPath, list[i])
            if os.path.isfile(path):
                file_path = os.path.split(path)  # 分割出目录与文件
                lists = file_path[1].split('.')  # 分割出文件与文件扩展名
                file_ext = lists[-1]  # 取出后缀名(列表切片操作)
                img_ext = ['txt']
                if file_ext in img_ext:
                    fileList.append(path)
        for i in range(len(fileList)):
            txtFile = fileList[i]
            with open(txtFile, 'r') as file_to_read:
                lines = file_to_read.readline()  # 整行读取数据
                if not lines:
                    break
                    pass
                lines = file_to_read.readline()  # 整行读取数据
                data = lines.split(":")

                gsd = data[1]
                gsd = gsd.replace('\n', '')
                if gsd == 'null':
                    break
                gsd = float(gsd)
                gsdList.append(gsd)

                imgFile = txtFile.replace('.txt', imgType)
                img = cv2.imread(imgFile)
                print(img.shape)

        print(min(gsdList))
        print(max(gsdList))

    def classNumInformation(self, imgPath):
        fileList = self.getFileList(imgPath)
        for i in range(len(fileList)):
            txtFile = fileList[i].replace(imgType, '.txt')
            txtName = os.path.basename(txtFile)
            if not os.path.exists(txtFile):
                print("file do not exist:%s" % txtFile)
                exit()
            with open(txtFile, 'r') as file_to_read:
                lines = file_to_read.readline()  # 整行读取数据

                lines = file_to_read.readline()

                while True:
                    lines = file_to_read.readline()
                    if not lines:
                        break
                        pass
                    data = lines.split()  # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
                    s = data[0] + ' ' + data[1] + ' ' + data[4] + ' ' + data[5]
                    # class 1: airplane
                    if data[8] == 'plane':
                        classNum = '1'
                        DatasetNormalize.classNumCal[0] += 1
                    elif data[8] == 'ship':
                        classNum = '2'
                        DatasetNormalize.classNumCal[1] += 1
                    # class 3: storage tank
                    elif data[8] == 'storage-tank':
                        classNum = '3'
                        DatasetNormalize.classNumCal[2] += 1
                    # class 4:baseball diamond
                    elif data[8] == 'baseball-diamond':
                        classNum = '4'
                        DatasetNormalize.classNumCal[3] += 1
                    # class 5: tennis court
                    elif data[8] == 'tennis-court':
                        classNum = '5'
                        DatasetNormalize.classNumCal[4] += 1
                    # class 6: basketball court
                    elif data[8] == 'basketball-court':
                        classNum = '6'
                        DatasetNormalize.classNumCal[5] += 1
                    # class 7: ground track field
                    elif data[8] == 'ground-track-field':
                        classNum = '7'
                        DatasetNormalize.classNumCal[6] += 1
                    elif data[8] == 'harbor':
                        classNum = '8'
                        DatasetNormalize.classNumCal[7] += 1
                    elif data[8] == 'bridge':
                        classNum = '9'
                        DatasetNormalize.classNumCal[8] += 1
                    # class 10: vehicle
                    elif data[8] == 'small-vehicle':
                        classNum = '10'
                        DatasetNormalize.classNumCal[9] += 1
                    elif data[8] == 'large-vehicle':
                        classNum = '11'
                        DatasetNormalize.classNumCal[10] += 1
                    elif data[8] == 'helicopter':
                        classNum = '12'
                        DatasetNormalize.classNumCal[11] += 1
                    elif data[8] == 'swimming-pool':
                        classNum = '13'
                        DatasetNormalize.classNumCal[12] += 1
                    elif data[8] == 'roundabout':
                        classNum = '14'
                        DatasetNormalize.classNumCal[13] += 1
                    elif data[8] == 'soccer-ball-field':
                        classNum = '15'
                        DatasetNormalize.classNumCal[14] += 1
                    elif data[8] == 'container-crane':
                        classNum = '16'
                        DatasetNormalize.classNumCal[15] += 1
                    else:
                        classNum = data[8]
                        print(classNum)

    def classNumInformationForNWPU(self, imgPath):
        fileList = self.getFileList(imgPath)
        for i in range(len(fileList)):
            txtFile = fileList[i].replace('.jpg', '.txt')
            txtName = os.path.basename(txtFile)
            if not os.path.exists(txtFile):
                print("file do not exist:%s" % txtFile)
                exit()
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
                    data = data.replace('\n','')
                    data = data.split(',')
                    data = [int(x) for x in data]
                    DatasetNormalize.classNumCal[data[4]-1] += 1
            img = cv2.imread(fileList[i])
            print(img.shape)

    def writeInfor(self, imgPath):

        outfile = r'F:\Code\Matlab\LeaveWork\dataSetSizePlot\LevirT.txt'
        imgFileList = glob.glob(os.path.join(imgPath, '*.jpg'))
        with open(outfile, 'w') as file_to_write:
            for i in range(len(imgFileList)):
                img = cv2.imread(imgFileList[i], cv2.IMREAD_UNCHANGED)
                txtFile = imgFileList[i].replace('.jpg', '.txt')
                height, width, _ = img.shape
                with open(txtFile, 'r') as file_to_read:
                    # lines = file_to_read.readline()
                    # lines = file_to_read.readline()
                    # if not lines:
                    #     break
                    #     pass
                    while True:
                        lines = file_to_read.readline()  # 整行读取数据
                        if not lines:
                            break
                            pass
                        # Levir
                        data = lines.split()
                        class_name, xmin, ymin, xmax, ymax = [float(x) for x in data]

                        # # NWPU
                        # if lines == '\n':
                        #     break
                        #
                        # data = lines.replace('(', '')
                        # data = data.replace(')', '')
                        # data = data.replace('\n', '')
                        # data = data.split(',')
                        # data = [int(x) for x in data]
                        # xmin, ymin, xmax, ymax, class_name = data



                        if class_name not in [1,2]:
                            continue

                        if xmin<0 or xmin>width or ymin<0 or ymin >height or xmax<0 or xmax>width or ymax <0 or ymax>height:
                            break


                        s = str(class_name)+' '+str(xmin)+' '+str(ymin)+' '+str(xmax)+' '+str(ymax)+' '+str(width)+' '+str(height)+'\n'
                        if xmin>xmax:
                            print(txtFile)
                        file_to_write.writelines(s)


def main():
    inPath = r"/Users/keyanchen/Files/Code/电子所/"
    outPath =r'/Users/keyanchen/Files/Code/电子所/Pieces'
    dn = DatasetNormalize(inPath, outPath, smallWidth=512, smallHeight=512)

    # dn.divideSource()
    # dn.processTagForDOTA()
    dn.getPiece()
    # dn.writeInfor(r'E:\Lab\Dataset\LEVIR\imageWithLabel\evaluation')


if __name__ == '__main__':
    main()





