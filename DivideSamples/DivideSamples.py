# 把数据按比例随机分成正负样本

import os
import glob
import random
import shutil

positive_rate = 0.7
sample_path = r'F:\DataSet\NWPU VHR-10 dataset\positive image set'
img_format = 'jpg'

img_file_list = glob.glob(os.path.join(sample_path, '*.%s' % img_format))
positive_index = random.sample(range(0, len(img_file_list)), int(positive_rate * len(img_file_list)))
negative_index = set(range(0, len(img_file_list))) - set(positive_index)

dst_path = os.path.join(os.path.dirname(img_file_list[0]), 'train')
if os.path.exists(dst_path):
    shutil.rmtree(dst_path)
os.makedirs(dst_path)

dst_path = os.path.join(os.path.dirname(img_file_list[0]), 'test')
if os.path.exists(dst_path):
    shutil.rmtree(dst_path)
os.makedirs(dst_path)

for i in positive_index:
    img_file = img_file_list[i]
    txt_file = img_file.replace(img_format, 'txt')
    img_file_save = os.path.join(os.path.dirname(img_file), 'train', os.path.basename(img_file))
    txt_file_save = img_file_save.replace(img_format, 'txt')
    shutil.copyfile(img_file, img_file_save)
    shutil.copyfile(txt_file, txt_file_save)

for i in negative_index:
    img_file = img_file_list[i]
    txt_file = img_file.replace(img_format, 'txt')
    img_file_save = os.path.join(os.path.dirname(img_file), 'test', os.path.basename(img_file))
    txt_file_save = img_file_save.replace(img_format, 'txt')
    shutil.copyfile(img_file, img_file_save)
    shutil.copyfile(txt_file, txt_file_save)

