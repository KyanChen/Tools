import glob
import os
import tarfile
import tqdm
import shutil

file_path = r'J:\GF1_GF6'
file_format = '.gz'
out_path = r'I:\GF\temp_uncompress'
labled_path = r'J:\20210117_GF1_GF6数据\海上'


file_list = glob.glob(f"{file_path}/*{file_format}")
file_list.sort(reverse=True)
to_uncompress_files = file_list[:150]

labled_file_list = glob.glob(f"{labled_path}/*{file_format}") + glob.glob(r'I:\GF\temp_uncompress' + '/GF*')
labled_file_list = [os.path.basename(x).split(".tar")[0] for x in labled_file_list]
os.makedirs(labled_path, exist_ok=True)

def untar(fname, dirs):
    """
    解压tar.gz文件
    :param fname: 压缩文件名
    :param dirs: 解压后的存放路径
    :return: bool
    """
    try:
        t = tarfile.open(fname)
        t.extractall(path=dirs)
        return True
    except Exception as e:
        print(e)
        return False


for file in tqdm.tqdm(to_uncompress_files):
    file_no_suffix_name = os.path.basename(file).split(".tar")[0]
    if file_no_suffix_name in labled_file_list:
        print(file_no_suffix_name + " has labeled")
        continue
    out_save_path = out_path + '/' + file_no_suffix_name
    os.makedirs(out_save_path, exist_ok=True)
    untar(file, out_save_path)
    # shutil.move(file, labled_path + '/' + os.path.basename(file))



