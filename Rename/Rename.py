import os
import glob

file_path = r'/Users/keyanchen/Files/Dataset/704/AIR-SARShip-1.0/patch_txt'

file_list = glob.glob(os.path.join(file_path, '*.txt'))
for i in file_list:
    os.renames(i, i.replace('.tiff', ''))
