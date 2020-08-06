import os
import shutil
import math
import numpy as np
import cv2
import random
import glob
mul = lambda arg1: arg1[0]*arg1[1]
add = lambda arg1: arg1[0]+arg1[1]

imgType = '.jpg'

class GetRandom:

    def __init__(self, inPath, outPath, **kwargs):
        self.inPath = inPath
        self.outPath = outPath

        if not os.path.exists(self.outPath):
            os.mkdir(self.outPath)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def getRandomFile(self):
        imgFileList = glob.glob(os.path.join(self.inPath, '*%s' % imgType))
        evaluationNum = int(3*len(imgFileList)/10.0)
        h = set()
        while len(h)<evaluationNum:
            h.add(imgFileList[random.randint(0, len(imgFileList)-1)])
        for x in h:
            imgFileMove = os.path.join(self.outPath, os.path.basename(x))
            txtFile = x.replace(imgType, '.txt')
            txtFileMove = imgFileMove.replace(imgType, '.txt')

            shutil.move(x, imgFileMove)
            shutil.move(txtFile, txtFileMove)




def main():
    inPath = r"E:\Lab\Dataset\NWPU VHR-10 dataset\data"
    outPath = os.path.abspath(os.path.join(inPath, r"..", "evaluation"))
    GR = GetRandom(inPath, outPath, smallWidth=2048, smallHeight=2048)
    GR.getRandomFile()




if __name__ == '__main__':
    main()





