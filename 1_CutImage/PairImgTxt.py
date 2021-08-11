import os
import shutil
import math
import numpy as np
import cv2
import glob

inPath = r"E:\Lab\Dataset\NWPU VHR-10 dataset\negative image set"
imgType = '.jpg'


imgFileList = glob.glob(os.path.join(inPath, '*%s' % imgType))
for i in range(len(imgFileList)):
    imgFile = imgFileList[i]
    txtFile = imgFile.replace(imgType, '.txt')
    if not os.path.exists(txtFile):
        with open(txtFile, 'w') as fileToWrite:
            fileToWrite.close()