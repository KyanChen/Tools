import os
import glob
import shutil
import tqdm
import time
import sched

file_path = 'D:\\'
to_path = r'I:\GF下载'

os.makedirs(to_path, exist_ok=True)


def move_file():
    file_list = glob.glob(file_path + '/*.tar.gz')
    for file in tqdm.tqdm(file_list):
        shutil.move(file, to_path + '/' + os.path.basename(file))
        print(f"move:{os.path.basename(file)}")
    print(time.strftime('%Y%m%d%H%M'))


s = sched.scheduler(time.time, time.sleep)

while True:
    s.enter(60*60, 0, move_file)
    s.run()

