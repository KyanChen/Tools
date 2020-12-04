import os
import glob
import cv2
import tqdm
from osgeo import gdal
import numpy as np
img_piece_size = (512, 512)


def get_file(in_path_list, img_format):
    file_list = []
    for file in in_path_list:
        if os.path.isdir(file):
            files = glob.glob(file + '/*')
            file_list.extend(get_file(files, img_format))
        else:
            if file.split('.')[-1] == img_format:
                file_list += [file]
    return file_list


def get_pieces(img_parent_path, pieces_path, img_format):
    file_list = get_file([img_parent_path], img_format)
    for img_path in tqdm.tqdm(file_list):
        pieces_save_path = pieces_path + '/' + os.path.basename(img_path).replace('.' + img_format, '')
        os.makedirs(pieces_save_path, exist_ok=True)
        cut_img_to_pieces(img_path, pieces_save_path, img_format)


def cut_img_to_pieces(img_file, save_folder, img_format):
    tiff_dataset = gdal.Open(img_file)
    nBand, rows, cols = tiff_dataset.RasterCount, tiff_dataset.RasterYSize, tiff_dataset.RasterXSize
    h_list = list(range(0, rows, img_piece_size[1]))
    h_list[-1] = rows - img_piece_size[1]
    w_list = list(range(0, cols, img_piece_size[0]))
    w_list[-1] = cols - img_piece_size[0]
    for h_step in h_list:
        for w_step in w_list:
            img_data = tiff_dataset.ReadAsArray(w_step, h_step, img_piece_size[1], img_piece_size[0])[:3]
            img_data = np.transpose(img_data, (1, 2, 0))
            img_piece = (img_data / 4).astype(np.uint8)
            cv2.imwrite(save_folder + '/%s_%d_%d.jpg' %
                        (os.path.basename(img_file).replace('.' + img_format, ''),
                         w_step, h_step), img_piece)


if __name__ == "__main__":
    img_parent_path = r'J:\GF1_GF6\GF1_WFV1_E127.3_N26.3_20180913_L1A0003450235'
    img_format = 'tiff'
    pieces_save_path = r'J:\GF1_GF6\GF1_WFV1_E127.3_N26.3_20180913_L1A0003450235\slices'
    get_pieces(img_parent_path, pieces_save_path, img_format)
