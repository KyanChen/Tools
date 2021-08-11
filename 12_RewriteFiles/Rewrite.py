import glob
import os
from PIL import Image
import numpy as np
from skimage import io
import skimage
import tqdm
import threading


img_parent_path = r'J:\20200923-建筑提取数据集\WHU_Building\Aeial'
img_format = 'tif'

img_list = glob.glob(img_parent_path + '/*/*/*%s' % img_format)


def rewrite_files(img_files):
    for img_path in tqdm.tqdm(img_files):
        img = np.array(Image.open(img_path))
        img = skimage.img_as_ubyte(img)
        if os.path.exists(img_path.replace(img_format, 'png')):
            os.remove(img_path.replace(img_format, 'png'))
        io.imsave(img_path.replace(img_format, 'png'), img, check_contrast=False)


def check_file(img_file):
    if not os.path.exists(img_file.replace(img_format, 'png')):
        print(img_file)
        return 0
    return 1


def remove_files(img_files):
    for img_path in img_files:
        if check_file(img_path):
            os.remove(img_path)


if __name__ == '__main__':
    threads = []
    num_works = 8
    step = int(len(img_list) / num_works)
    for i in range(0, num_works):
        imgs = img_list[step*i: step*(i+1)]
        if i == num_works - 1:
            imgs = img_list[step*i: len(img_list)]
        t = threading.Thread(target=rewrite_files, args=(imgs,))
        threads.append(t)

    for i in range(0, num_works):
        threads[i].start()
    for i in range(0, num_works):
        threads[i].join()
    remove_files(img_list)

