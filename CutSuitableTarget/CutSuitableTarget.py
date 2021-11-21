import os
import glob
import matplotlib.pyplot as plt
import numpy as np
import shutil
import cv2
import sys


srcPath = sys.argv[1]
# r'dataset/positiveSamples'
dstPath = sys.argv[2]

imgFormat = '.tiff'
generateTimes = 2
imgToSize = (512, 512)

imgFileList = glob.glob(os.path.join(srcPath, '*%s' % imgFormat))

dstPath = os.path.abspath(dstPath)
if os.path.exists(dstPath):
    shutil.rmtree(dstPath)
os.makedirs(dstPath)

def drawBboxes(img, bboxs):
    for bbox in bboxs:
        print(bbox)
        cv2.rectangle(img, tuple(bbox[0:2]), tuple(bbox[2:4]), (255, 0, 0), 2)
    plt.imshow(img)
    plt.show()


for imgFile in imgFileList:
    img = cv2.imread(imgFile)
    height, width, channel = img.shape
    txtFile = imgFile.replace(imgFormat, '.txt')
    bboxs = []
    try:
        with open(txtFile, 'r') as f_reader:
            line = f_reader.readline()
            while line:
                _, _, left, top, right, bottom = map(lambda x: int(float(x)), line.strip().split())
                bboxs.append([left, top, right, bottom])
                line = f_reader.readline()
    except:
        continue
    bboxs_numpy = np.array(bboxs)
    if bboxs_numpy.size == 0:
        continue
    else:
        min_value = bboxs_numpy.min(0)
        max_value = bboxs_numpy.max(0)
        min_left, min_top, max_right, max_bottom = min_value[0], min_value[1], max_value[2], max_value[3]

        # Generate Crop Image
        max_width_target = max_right - min_left
        max_height_target = max_bottom - min_top
        max_width_height = max(max_width_target, max_height_target)
        for i in range(generateTimes):
            try:
                left_crop = np.random.randint(min_left - max_width_height * np.random.randint(15, 20)/10,
                                              min_left- max_width_height * 0.3)
            except:
                left_crop = np.random.randint(min_left - max_width_height * np.random.randint(15, 20) / 10,
                                              min_left)
            left_crop = left_crop if left_crop > 0 else 0
            try:

                top_crop = np.random.randint(min_top - max_width_height * np.random.randint(15, 20)/10,
                                             min_top - max_width_height * 0.3)
            except:
                top_crop = np.random.randint(min_top - max_width_height * np.random.randint(15, 20) / 10,
                                             min_top)
            top_crop = top_crop if top_crop > 0 else 0

            right_crop = left_crop + int(max_width_height * np.random.randint(25, 35)/10)
            right_crop = right_crop if right_crop < width else width
            bottom_crop = top_crop + int(max_width_height * np.random.randint(25, 35)/10)
            bottom_crop = bottom_crop if bottom_crop < height else height


            img_crop = img[top_crop: bottom_crop, left_crop: right_crop]
            bboxs_numpy_cur = bboxs_numpy - np.tile(np.array([left_crop, top_crop]), 2)

            try:
                img_crop_resize = cv2.resize(img_crop, imgToSize)
            except:
                continue
            imgToWritePath = os.path.join(dstPath,
                                          '%s_%d%s' % (os.path.splitext(os.path.basename(imgFile))[0], i, imgFormat))
            cv2.imencode(imgFormat, img_crop_resize)[1].tofile(imgToWritePath)

            img_crop_height, img_crop_width, _ = img_crop.shape
            with open(imgToWritePath.replace(imgFormat, '.txt'), 'w') as f_writer:
                for bbox in bboxs_numpy_cur:
                    left_crop_resize, top_crop_resize, right_crop_resize, bottom_crop_resize = bbox
                    left_crop_resize = int(imgToSize[0] * left_crop_resize / img_crop_width)
                    right_crop_resize = int(imgToSize[0] * right_crop_resize / img_crop_width)
                    top_crop_resize = int(imgToSize[1] * top_crop_resize / img_crop_height)
                    bottom_crop_resize = int(imgToSize[1] * bottom_crop_resize / img_crop_height)

                    left_crop_resize = max(0, left_crop_resize)
                    right_crop_resize = min(imgToSize[0], right_crop_resize)
                    top_crop_resize = max(0, top_crop_resize)
                    bottom_crop_resize = min(imgToSize[1], bottom_crop_resize)

                    line = '%d %d %d %d %d\n' %\
                           (1, left_crop_resize, top_crop_resize, right_crop_resize, bottom_crop_resize)
                    f_writer.write(line)

            # drawBboxes(img_crop_resize, np.array([[left_crop_resize, top_crop_resize, right_crop_resize, bottom_crop_resize]]))

