import os
import glob
import shutil

look_dict = r'G:\Coding\EfficientDet\EvalResults1020_select2'
from_path = r'F:\DataSet\GF1_2\total_data\val'
to_path = r'F:\DataSet\GF1_2\total_data\val_select'

if os.path.exists(to_path):
    shutil.rmtree(to_path)
os.makedirs(to_path)

file_list = glob.glob(os.path.join(look_dict, '*.txt'))
for file in file_list:
    # if os.path.getsize(file) == 0:
    #     continue
    file_copy = os.path.join(from_path, os.path.basename(file).replace('txt', 'jpg'))
    file_to_copy_path = os.path.join(to_path, os.path.basename(file).replace('txt', 'jpg'))
    shutil.copyfile(file_copy, file_to_copy_path)
    shutil.copyfile(file_copy.replace('jpg', 'txt'), file_to_copy_path.replace('jpg', 'txt'))

