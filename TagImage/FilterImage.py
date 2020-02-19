# coding: utf-8
import cv2
import os
import shutil
from PIL import Image
import numpy as np


class FilterImage:
    def __init__(self, inPathName):
        self.inPathName = inPathName
        if not os.path.isabs(self.inPathName):
            self.inPathName = os.path.abspath(self.inPathName)
        if not os.path.exists(self.inPathName):
            os.mkdir(self.inPathName)
        self.outPathName = os.path.abspath(os.path.join(self.inPathName, '..\outPath'))
        if not os.path.exists(self.outPathName):
            os.mkdir(self.outPathName)

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
        return fileList

    def saveData(self, filePathName):
        shutil.move(filePathName, self.outPathName)
        file_path = os.path.splitext(filePathName)  # 分割出文件扩展名
        txtPathName = file_path[0] + '.txt'
        shutil.move(txtPathName, self.outPathName)

    def run(self):
        fileList = self.getFileList()
        for i in range(0, len(fileList)):
            img = cv2.imdecode(np.fromfile(fileList[i], dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            cv2.imshow("%s" % i, img)
            while True:
                key_pressed = cv2.waitKey(0)
                ok_pressed = [ord('y'), ord('Y')]
                no_pressed = [ord('n'), ord('N')]
                if key_pressed in ok_pressed:
                    break
                elif key_pressed in no_pressed:
                    self.saveData(fileList[i])
                    break
            cv2.destroyAllWindows()


def main():
    inPathName = r"E:\Lab\其他\20190314_data"
    filterImg = FilterImage(inPathName)
    filterImg.run()


if __name__ == '__main__':
    main()








