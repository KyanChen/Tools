import os
from PIL import Image
import shutil

imgType = '.jpg'

negative_samples_path = r'F:\ObjectDetection\ObjectDetectionResult\资源中心目标检测结果_尾矿库_20191106\GF1B_PMS_E117.0_N29.7_20191018_L1A1227711846_FUSION_GEO\source_img'
filenameList = os.listdir(negative_samples_path)

outSamplesPath = os.path.abspath(os.path.join(negative_samples_path, r'..\negativeSamples'))
if os.path.exists(outSamplesPath):
    shutil.rmtree(outSamplesPath)
os.makedirs(outSamplesPath)
for name in filenameList:
    filePath = os.path.join(negative_samples_path, name)
    try:
        Image.open(filePath)
    except:
        continue
    shutil.copyfile(filePath, os.path.join(outSamplesPath, name))
    with open(os.path.join(outSamplesPath, name.replace(imgType, '.txt')), 'w') as f:
        pass