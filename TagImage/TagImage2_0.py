# coding: utf-8
import cv2
import os
import shutil
from PIL import Image
import numpy as np

# first, change your data path,
# second, for program esc is undo a mark, mouse click and move is mark a bbox
# third, y or Y is to save. if no object in image, just only press Y or y

inPathName = r"E:\Lab\Dataset\20190612标图油罐\cky\新建文件夹"
classToWrite = 3


scalar = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (200, 5, 200)]


class TagImage:

    def __init__(self, inPathName):
        self.inPathName = inPathName
        if not os.path.isabs(self.inPathName):
            self.inPathName = os.path.abspath(self.inPathName)
        if not os.path.exists(self.inPathName):
            os.mkdir(self.inPathName)
        self.tempPathName = os.path.abspath(os.path.join(self.inPathName, r'.\temp'))
        if not os.path.exists(self.tempPathName):
            os.mkdir(self.tempPathName)
        self.curFile = self.readCurFile()
        if self.curFile > len(self.getFileList())-1 or self.curFile < 0:
            self.curFile = 0

        self.bboxList = []
        self.curImg = None
        self.curXY = [0, 0]
        self.initBboxXY = [0, 0]
        self.curBboxXY = [0, 0]
        self.isDrawFinished = True

    def readCurFile(self):
        txtFileName = self.tempPathName + r'\temp.txt'
        if os.path.exists(txtFileName):
            with open(txtFileName, 'r') as file:
                curFile = int(file.readline())
        else:
            curFile = 0
        return curFile

    def writeCurFile(self, curFile):
        txtFileName = self.tempPathName + r'\temp.txt'
        with open(txtFileName, 'w') as file:
            curFile = file.writelines(str(curFile))

    def getFileList(self):
        fileList = []
        list = os.listdir(self.inPathName)
        for i in range(0, len(list)):
            path = os.path.join(self.inPathName, list[i])
            if os.path.isfile(path):
                file_path = os.path.split(path)  # 分割出目录与文件
                lists = file_path[1].split('.')  # 分割出文件与文件扩展名
                file_ext = lists[-1]  # 取出后缀名(列表切片操作)
                img_ext = ['bmp', 'jpeg', 'gif', 'psd', 'png', 'jpg', 'tif']
                if file_ext in img_ext:
                    fileList.append(path)
        fileList.sort()
        return fileList

    def saveData(self, filePathName):
        if os.path.exists(os.path.join(self.outPathName, os.path.basename(filePathName))):
            os.remove(os.path.join(self.outPathName, os.path.basename(filePathName)))
        shutil.move(filePathName, self.outPathName)
        file_path = os.path.splitext(filePathName)  # 分割出文件扩展名
        txtPathName = file_path[0] + '.txt'
        if os.path.exists(os.path.join(self.outPathName, os.path.basename(txtPathName))):
            os.remove(os.path.join(self.outPathName, os.path.basename(txtPathName)))
        shutil.move(txtPathName, self.outPathName)

    def readTag(self, filePathName):
        file_path = os.path.splitext(filePathName)  # 分割出文件扩展名
        txtPathName = file_path[0] + '.txt'
        if not os.path.exists(txtPathName):
            file_to_read = open(txtPathName, 'w')
            file_to_read.close()
        with open(txtPathName, 'r') as file_to_read:
            while True:
                lines = file_to_read.readline()  # 整行读取数据
                if not lines:
                    break
                    pass
                data = lines.split() # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
                # dataToRead = list(map(int, data[1:]))
                dataToRead = [int(x) for x in data]
                self.bboxList.append(dataToRead)
                pass

    def saveTag(self, filePathName):
        file_path = os.path.splitext(filePathName)  # 分割出文件扩展名
        txtPathName = file_path[0] + '.txt'
        with open(txtPathName, 'w') as file:
            for i in range(0, len(self.bboxList)):
                for j in range(0, 4):
                    ch = self.bboxList[i][j]
                    file.write(str(ch) + ' ')
                file.write(str(self.bboxList[i][4]))
                file.write('\n')
                # dataToWrite = [str(x) + '\n' for x in dataToWrite]

    # 创建回调函数
    def draw_rectangle(self, event, x, y, flags, param):
        # 当按下左键是返回起始位置坐标
        global x1, y1
        self.curXY = [x, y]
        if event == cv2.EVENT_LBUTTONDOWN:
            x1, y1 = x, y
            self.initBboxXY = [x, y]
        # 当鼠标左键按下并移动是绘制图形。event可以查看移动，flag查看是否按下
        elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
            self.isDrawFinished = False
            self.curBboxXY = [x, y]
        elif event == cv2.EVENT_LBUTTONUP:
            self.isDrawFinished = True
            x1, y1, x2, y2 = self.getTLAndBR(x1, y1, x, y)
            self.bboxList.append([classToWrite, x1, y1, x2, y2])

    def getTLAndBR(self, x_1, y_1, x_2, y_2):
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
        return x1, y1, x2, y2




    def run(self):
        fileList = self.getFileList()
        while self.curFile < len(fileList):
            self.bboxList.clear()
            self.readTag(fileList[self.curFile])
            img = cv2.imdecode(np.fromfile(fileList[self.curFile], dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            cv2.namedWindow('curWindow')
            # 绑定事件
            cv2.setMouseCallback('curWindow', self.draw_rectangle)
            while True:
                self.curImg = np.copy(img)
                # print(len(self.bboxList))
                print(str(self.curFile)+'/'+str(len(fileList)))

                for j in range(0, len(self.bboxList)):
                    class_num, x_1, y_1, x_2, y_2 = self.bboxList[j]
                    self.curImg = cv2.rectangle(self.curImg, (x_1, y_1), (x_2, y_2), scalar[class_num-1], 2)
                    cv2.putText(self.curImg, str(class_num), (x_1, y_1), cv2.FONT_HERSHEY_COMPLEX, 0.8, scalar[class_num-1], 1)
                if not self.isDrawFinished:
                    cv2.rectangle(self.curImg, (self.initBboxXY[0], self.initBboxXY[1]),
                                  (self.curBboxXY[0], self.curBboxXY[1]), (255, 255, 255), 1)
                width, height, _ = self.curImg.shape
                cv2.line(self.curImg, (self.curXY[0], 0), (self.curXY[0], height), (255, 255, 255), 1)
                cv2.line(self.curImg, (0, self.curXY[1]), (width, self.curXY[1]), (255, 255, 255), 1)

                cv2.imshow("curWindow", self.curImg)
                key_pressed = cv2.waitKey(1)
                ok_pressed = [ord('y'), ord('Y')]
                a_pressed = [ord('a'), ord('A')]
                d_pressed = [ord('d'), ord('D')]
                undo_pressed = [27]
                if key_pressed in d_pressed:
                    self.saveTag(fileList[self.curFile])
                    self.curFile = self.curFile + 1
                    self.writeCurFile(self.curFile)
                    break
                elif key_pressed in a_pressed:
                    self.curFile = self.curFile - 1
                    if self.curFile < 0:
                        self.curFile = 0
                    self.writeCurFile(self.curFile)
                    break
                elif key_pressed in undo_pressed:
                    if len(self.bboxList):
                        self.bboxList.pop()
                    else:
                        continue

def main():
    filterImg = TagImage(inPathName)
    filterImg.run()


if __name__ == '__main__':
    main()


