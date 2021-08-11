import glob
import numpy as np
import os

file_list = np.loadtxt(r'G:\Coding\Tools\8_WebScrape\20210116.txt', dtype=str)
file_already_exist = glob.glob(r'D:\Downloads\*.gz')
file_already_exist = [os.path.basename(x) for x in file_already_exist]
filtered_files = []
t = {}
for x in file_list:
    flag = 0
    for y in file_already_exist:
        if y in x:
            t[y] = 1
            flag = 1
    if not flag:
        filtered_files.append(x)
diff = set(file_already_exist) - set(t.keys())
diff = list(diff)
np.savetxt("downfiles.txt", np.array(filtered_files), fmt='%s')
