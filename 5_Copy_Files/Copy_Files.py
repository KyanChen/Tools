import os
import glob
import shutil
import tqdm
import numpy as np

look_dict = r'I:\陈剑奇已标\Delete.txt'
from_path = r'J:\GF1_6'
to_path = r'D:\陆地待确认'


os.makedirs(to_path, exist_ok=True)

# file_list = glob.glob(look_dict + '/*/Patches/*')
file_list = np.loadtxt(look_dict, dtype=str)
for file in tqdm.tqdm(file_list):
    # if os.path.getsize(file) == 0:
    #     continue
    # file_copy = os.path.join(from_path, os.path.basename(file).replace('txt', 'jpg'))
    file_copy = from_path + '/' + file + ".tar.gz"
    if not os.path.exists(file_copy):
        print(file_copy)
        continue
    file_to_copy_path = to_path + '/' + os.path.basename(file_copy)
    # shutil.copyfile(file_copy, file_to_copy_path)
    # shutil.copyfile(file_copy.replace('jpg', 'txt'), file_to_copy_path.replace('jpg', 'txt'))
    # shutil.copytree(file, file_to_copy_path)
    shutil.move(file_copy, file_to_copy_path)

