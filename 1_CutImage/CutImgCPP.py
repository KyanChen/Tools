import numpy as np
import cv2
import glob
import os
import tqdm
from skimage import io
from numba import jit


def cut_with_label(file_list, save_path, slice_size, overlap_ratio, donwsample_ratio, form_dir):
    refine_save_path = save_path
    for id, img_file in tqdm.tqdm(enumerate(file_list)):
        if form_dir:
            refine_save_path = save_path + '\\' + os.path.basename(img_file).split('.')[0]
        os.makedirs(refine_save_path, exist_ok=True)
        os.system(f"L:\Code\CutImgCPP\Seg.exe {img_file} {refine_save_path} {slice_size} {overlap_ratio} {donwsample_ratio}")


if __name__ == '__main__':
    img_path = r'L:\Detection\20211026RSAICP_Ship_Detection_Competition\RSAICP_Ship_Detection\train\mask_refine_66'
    overlap_ratio = 0.2
    slice_size = 256
    donwsample_ratio = 0.5
    save_path = r'L:\Detection\20211026RSAICP_Ship_Detection_Competition\RSAICP_Ship_Detection\train\Ship_Comp_256_Down2_Toal'  # 切片保存的路径
    img_format = 'png'

    img_file_list = glob.glob(img_path + f'/*{img_format}')
    cut_with_label(img_file_list, save_path, slice_size, overlap_ratio, donwsample_ratio, form_dir=True)

