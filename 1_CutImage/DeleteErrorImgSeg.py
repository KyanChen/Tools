import glob
from skimage import io
import tqdm
import numpy as np
import shutil
import os

img_dir = r'J:\20200923-建筑提取数据集\InriaAerialImageDataset\train\pieces\label'

img_file_list = glob.glob(img_dir + '/*.tiff')
for img_file in tqdm.tqdm(img_file_list):
    img = io.imread(img_file)
    h, w = img.shape
    num_255 = np.sum(img > 254)
    rate = num_255 / h / w
    if rate < 0.001:
        print(os.path.basename(img_file))
        os.remove(img_file)
        os.remove(img_file.replace("label", "img"))
