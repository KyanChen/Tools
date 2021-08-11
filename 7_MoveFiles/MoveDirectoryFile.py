import os
import glob
import shutil
import tqdm

look_dict = r'K:\Positive_Patches'
from_path = r'J:\GF1_6已标\已标TAR文件'
to_path = r'J:\20210117_GF1_GF6数据\海上'

os.makedirs(to_path, exist_ok=True)

file_list = glob.glob(look_dict + '/GF*') + glob.glob(r'K:\Positive_Patches\待确认\*') + glob.glob('I:\GF\Patches\GF*')


for file in tqdm.tqdm(file_list):
    file_name_no_suffix = os.path.basename(file)
    file_to_cut_path = from_path + '/' + file_name_no_suffix + '.tar.gz'
    if not os.path.exists(file_to_cut_path):
        print(file_name_no_suffix)
        continue
    file_cut_to_path = to_path + '/' + os.path.basename(file_to_cut_path)
    if os.path.exists(file_cut_to_path):
        os.remove(file_to_cut_path)
        continue
    shutil.move(file_to_cut_path, file_cut_to_path)

