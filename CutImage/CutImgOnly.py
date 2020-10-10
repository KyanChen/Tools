import os
import glob
import cv2
import tqdm
from osgeo import gdal
import numpy as np
img_piece_size = (1024, 1024)


def get_pieces(img_parent_path, pieces_path, img_format):
    if not os.path.exists(pieces_path):
        os.makedirs(pieces_path)
    img_path_list = glob.glob(img_parent_path+'/*%s' % img_format)
    if len(img_path_list) == 0:
        img_path_list = glob.glob(img_parent_path + '/*')
        for img_path in tqdm.tqdm(img_path_list):
            if not os.path.isdir(img_path):
                continue
            single_img_pieces_path = pieces_path + '/' + os.path.basename(img_path)
            if not os.path.exists(single_img_pieces_path):
                os.makedirs(single_img_pieces_path)
            img_file_list = glob.glob(img_path + '/*%s' % img_format)
            for idx in range(len(img_file_list)):
                cut_img_to_pieces(img_file_list[idx], single_img_pieces_path, img_format)
    else:
        img_file_list = glob.glob(img_parent_path + '/*%s' % img_format)
        for idx in range(len(img_file_list)):
            pieces_save_path = pieces_path + '/' + os.path.basename(img_file_list[idx]).replace('.' + img_format, '')
            if not os.path.exists(pieces_save_path):
                os.makedirs(pieces_save_path)
            cut_img_to_pieces(img_file_list[idx], pieces_save_path, img_format)


def cut_img_to_pieces(img_file, save_folder, img_format):
    tiff_dataset = gdal.Open(img_file)
    nBand, rows, cols = tiff_dataset.RasterCount, tiff_dataset.RasterYSize, tiff_dataset.RasterXSize
    h_list = list(range(0, rows, img_piece_size[1]))
    h_list[-1] = rows - img_piece_size[1]
    w_list = list(range(0, cols, img_piece_size[0]))
    w_list[-1] = cols - img_piece_size[0]
    for h_step in h_list:
        for w_step in w_list:
            img_data = tiff_dataset.ReadAsArray(w_step, h_step, img_piece_size[1], img_piece_size[0])
            img_piece = img_data.astype(np.uint8)
            cv2.imwrite(save_folder + '/%s_%d_%d.jpg' %
                        (os.path.basename(img_file).replace('.' + img_format, ''),
                         w_step, h_step), img_piece)


if __name__ == "__main__":
    img_parent_path = r'I:\20200914'
    img_format = 'tiff'
    pieces_save_path = r'I:\20200914\slice'
    get_pieces(img_parent_path, pieces_save_path, img_format)
