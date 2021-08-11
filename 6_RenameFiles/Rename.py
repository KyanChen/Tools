import os
import glob

file_path = r'D:\Downloads'

file_list = glob.glob(os.path.join(file_path, '*.gz'))
for i in file_list:
    try:
        os.renames(i, i.replace('tar_2', 'tar'))
    except FileExistsError:
        os.remove(i)
