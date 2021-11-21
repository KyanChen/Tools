import glob
import cv2
from skimage import io
import numpy as np

img_path = r'M:\Work\数据集标注样本\NWPU10\cloud\*.txt'
img_list = glob.glob(img_path)
img_format = '.jpg'

for img_file in img_list:
    img_file = img_file.replace('.txt', img_format)
    h = 100
    w = 300
    img = io.imread(img_file)[h:h+512, w:w+512, ...]
    io.imsave(img_file.replace(img_format, '_cut.png'), img)
    h, w, c = img.shape
    img = cv2.resize(img, (512, 512))
    alpha = io.imread(img_file.replace(img_format, '_alpha.png'))/ 255.
    reflectance = io.imread(img_file.replace(img_format, '_reflectance.png'))
    alpha = np.mean(alpha, axis=-1, keepdims=True)
    reflectance = np.mean(reflectance, axis=-1, keepdims=True)
    img_vis = img * (1 - alpha) + reflectance
    img_vis = np.clip(img_vis, 0, 255)
    img_vis = img_vis.astype(np.uint8)
    img_vis = cv2.resize(img_vis, (w, h))
    mean = np.mean(np.mean(img_vis, axis=0), axis=0)
    img_vis = cv2.copyMakeBorder(img_vis, 300, 300, 300, 300, borderType=cv2.BORDER_CONSTANT, value=mean)

    # cv2.imshow("1", img_vis[:, :, ::-1])
    # cv2.waitKey(0)
    io.imsave(img_file.replace(img_format, '_vis.png'), img_vis)
