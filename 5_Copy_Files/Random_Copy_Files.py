import os
import glob
import shutil
import tqdm
import random
import numpy as np

'''
for InriaAerialImageDataset
'''

img_path = r'J:\20200923-建筑提取数据集\InriaAerialImageDataset\train\images'
gt_path = r'J:\20200923-建筑提取数据集\InriaAerialImageDataset\train\gt'

save_path = r'J:\20200923-建筑提取数据集\InriaAerialImageDataset\train'
path = ['train', 'val', 'test']
for i in path:
    os.makedirs(save_path + '/' + i + '/' + 'img', exist_ok=True)
    os.makedirs(save_path + '/' + i + '/' + 'gt', exist_ok=True)

names = ['austin', 'chicago', 'kitsap', 'tyrol-w', 'vienna']
for img_name in names:
    train_names = random.sample(range(1, 37), k=36-14)
    val_test_names = set(range(1, 37)) - set(train_names)
    val_names = random.sample(val_test_names, k=7)
    test_names = val_test_names - set(val_names)
    for i in train_names:
        shutil.copy(img_path + '/' + img_name + repr(i) + '.tif',
                    save_path + '/train/img/' + img_name + repr(i) + '.tif')
        shutil.copy(gt_path + '/' + img_name + repr(i) + '.tif',
                    save_path + '/train/gt/' + img_name + repr(i) + '.tif')

    for i in val_names:
        shutil.copy(img_path + '/' + img_name + repr(i) + '.tif',
                    save_path + '/val/img/' + img_name + repr(i) + '.tif')
        shutil.copy(gt_path + '/' + img_name + repr(i) + '.tif',
                    save_path + '/val/gt/' + img_name + repr(i) + '.tif')

    for i in test_names:
        shutil.copy(img_path + '/' + img_name + repr(i) + '.tif',
                    save_path + '/test/img/' + img_name + repr(i) + '.tif')
        shutil.copy(gt_path + '/' + img_name + repr(i) + '.tif',
                    save_path + '/test/gt/' + img_name + repr(i) + '.tif')



