import glob
import tqdm
import os

file_path = r'J:\GF1_6'
file_format = '.gz'

file_list = glob.glob(f"{file_path}/*{file_format}")
file_list.sort(reverse=True)
for i in tqdm.tqdm(range(len(file_list))):
    for j in range(i+1, len(file_list)):
        try:
            file_i_name = os.path.basename(file_list[i]).split(".tar")[0]
            file_j_name = os.path.basename(file_list[j]).split(".tar")[0]
            if file_i_name == file_j_name:
                os.remove(file_list[j])
        except Exception as err:
            print(err)
