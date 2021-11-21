import os
import skimage.io as io
import shutil
import glob
import cv2
import numpy as np

img_path = r'L:\Detection\20211026RSAICP_Ship_Detection_Competition\RSAICP_Ship_Detection\train\pos_samples_center'
img_format = 'png'
imgname_list = glob.glob(os.path.join(img_path, '*/*.%s' % img_format))
save_path = r'L:\Detection\20211026RSAICP_Ship_Detection_Competition\RSAICP_Ship_Detection\train\pos_samples_center_resize'
os.makedirs(save_path, exist_ok=True)
factor = 1/3

for imgname in imgname_list:
    img = cv2.imread(imgname)

    h, w, c = img.shape
    # to_h = int(h * factor)
    # to_w = int(w * factor)
    to_h = 256
    to_w = 256
    to_img = cv2.resize(img, (to_w, to_h))
    os.makedirs(save_path+'/'+ os.path.basename(os.path.dirname(imgname)), exist_ok=True)
    cv2.imwrite(save_path+'/'+ os.path.basename(os.path.dirname(imgname))+ '/'+os.path.basename(imgname), to_img)

    label_file_name = imgname.replace(img_format, 'txt')
    bboxes = np.loadtxt(label_file_name, float, ndmin=2)
    bboxes[:, 1::2] = (bboxes[:, 1::2] / w) * to_w
    bboxes[:, 2::2] = (bboxes[:, 2::2] / h) * to_h
    bboxes[:, 0] = 0
    np.savetxt(save_path+'/'+os.path.basename(os.path.dirname(imgname))+'/'+os.path.basename(label_file_name), bboxes, '%d %.4f %.4f %.4f %.4f')