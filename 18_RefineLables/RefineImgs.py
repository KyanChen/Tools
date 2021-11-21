import glob
import os
import cv2
import numpy as np
import skimage.io as io

img_path = r'L:\Detection\Pretrain\Ship_GF12_256_donw1_Train'
img_file_list = glob.glob(img_path+'/*.txt')
for img_file in img_file_list:
    # img = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)
    # # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # os.remove(img_file)
    # cv2.imwrite(img_file.replace('tiff', 'png'), img)
    # io.imsave(img_file, img)

    bboxes = np.loadtxt(img_file, float, usecols=[1, 2, 3, 4], ndmin=2)
    refine_bboxes = np.insert(bboxes, 0, values=0, axis=1)
    np.savetxt(img_file, np.array(refine_bboxes), '%d %.4f %.4f %.4f %.4f')