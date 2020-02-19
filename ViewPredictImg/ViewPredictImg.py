import os
import cv2
import numpy as np

file_path = r'G:\Dataset\dataset_night\dataset_night_416'
classes = ['balloon']
classToWrite = 0
widthRatio = 1.5
heightRatio = 1.5

scalar = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (200, 5, 200)]


class ViewPredictImg:
    def __init__(self):
        self.file_path = os.path.abspath(file_path)
        assert os.path.exists(self.file_path), 'File path dose not exist!'
        self.class_to_write = classToWrite
        self.widthRatio = widthRatio
        self.heightRatio = heightRatio
        self.scalar = scalar
        self.tempPathName = os.path.abspath(os.path.join(self.file_path, r'.\temp'))
        if not os.path.exists(self.tempPathName):
            os.mkdir(self.tempPathName)
        self.curFile = self.readCurFile(self)
        if self.curFile > len(self.getFileList())-1 or self.curFile < 0:
            self.curFile = 0
        self.bboxList = []

    @staticmethod
    def readCurFile(self):
        txtFileName = self.tempPathName + r'\temp.txt'
        if os.path.exists(txtFileName):
            with open(txtFileName, 'r') as file:
                curFile = int(file.readline())
        else:
            curFile = 0
        return curFile

    @staticmethod
    def center_to_left(centerX, centerY, width, height):
        """
        Convert centerX, centerY, width, height to
        left, top, bottom, right form
        :return:
        """
        centerX, centerY, width, height = map(float, [centerX, centerY, width, height])
        left, top, bottom, right = int(centerX - width/2), int(centerY - height/2), \
            int(centerX + width/2), int(centerY + height/2)
        return left, top, bottom, right

    def readTag(self, filePathName, width, height):
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
                data = lines.split()  # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
                # dataToRead = list(map(int, data[1:]))
                classNum = classes.index(data[0])
                confidence, x1, y1, x2, y2 = [int(float(x)) for x in data[1:]]
                dataToRead = [classNum, widthRatio * x1, heightRatio * y1, widthRatio * x2, heightRatio * y2]
                dataToRead = [int(x) for x in dataToRead]
                self.bboxList.append(dataToRead)

    def writeCurFile(self, curFile):
        txtFileName = self.tempPathName + r'\temp.txt'
        with open(txtFileName, 'w') as file:
            file.writelines(str(curFile))

    def view(self):
        fileList = self.getFileList()
        cv2.namedWindow('curWindow')
        cv2.moveWindow('curWindow', 300, 100)
        while self.curFile < len(fileList):
            self.bboxList.clear()
            img = cv2.imdecode(np.fromfile(fileList[self.curFile], dtype=np.uint8), cv2.IMREAD_COLOR)
            # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            width, height, _ = img.shape
            self.readTag(fileList[self.curFile], width, height)

            while True:
                self.curImg = cv2.resize(img, (int(width * widthRatio), int(height * heightRatio)))
                print(str(self.curFile) + '/' + str(len(fileList)))

                for j in range(0, len(self.bboxList)):
                    class_num, x_1, y_1, x_2, y_2 = self.bboxList[j]
                    self.curImg = cv2.rectangle(self.curImg, (x_1, y_1), (x_2, y_2), scalar[class_num - 1], 2)
                    cv2.putText(self.curImg, classes[class_num], (x_1, y_1-5), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                                scalar[class_num - 1], 1)
                cv2.imshow("curWindow", self.curImg)

                key_pressed = cv2.waitKey(1)
                a_pressed = [ord('a'), ord('A')]
                d_pressed = [ord('d'), ord('D')]
                if key_pressed in d_pressed:
                    self.curFile = self.curFile + 1
                    self.writeCurFile(self.curFile)
                    break
                elif key_pressed in a_pressed:
                    self.curFile = self.curFile - 1
                    if self.curFile < 0:
                        self.curFile = 0
                    self.writeCurFile(self.curFile)
                    break

    def getFileList(self):
        fileList = []
        list = os.listdir(self.file_path)
        for i in range(0, len(list)):
            path = os.path.join(self.file_path, list[i])
            if os.path.isfile(path):
                file_path = os.path.split(path)  # 分割出目录与文件
                lists = file_path[1].split('.')  # 分割出文件与文件扩展名
                file_ext = lists[-1]  # 取出后缀名(列表切片操作)
                img_ext = ['bmp', 'jpeg', 'gif', 'psd', 'png', 'jpg', 'tif', 'tiff']
                if file_ext in img_ext:
                    fileList.append(path)
        fileList.sort()
        return fileList


if __name__ == '__main__':
    get_label = ViewPredictImg()
    get_label.view()

