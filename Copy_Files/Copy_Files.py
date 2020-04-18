import os
import glob
import shutil

look_dict = r'G:\Code\LeaveWork\SSD\Predict\with'
from_path = r'G:\Code\LeaveWork\SSD\Predict\GT_select'
to_path = r'G:\Code\LeaveWork\SSD\Predict\Result_select\GT'

if os.path.exists(to_path):
    shutil.rmtree(to_path)
os.makedirs(to_path)

file_list = glob.glob(os.path.join(look_dict, '*.txt'))
for file in file_list:
    if os.path.getsize(file) == 0:
        continue
    file_copy = os.path.join(from_path, os.path.basename(file).replace('txt', 'txt'))
    file_to_copy_path = os.path.join(to_path, os.path.basename(file).replace('txt', 'txt'))
    shutil.copyfile(file_copy, file_to_copy_path)

