import os
import glob
from skimage import io
import tqdm
import gdal
import numpy as np
import shutil

img_piece_size = (2048, 1024)
img_parent_path = r'I:\GF\temp_uncompress'
img_format = 'tiff'
pieces_save_path = r'I:\GF\Patches'


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


def get_pieces(img_parent_path, pieces_path, img_format, is_1_level_need_convert=False):
    file_list = get_file([img_parent_path], img_format)
    file_list_names = [os.path.basename(x).replace('.tiff', '') for x in file_list]
    already_exist_files = [os.path.basename(x) for x in glob.glob(pieces_path + '/GF*')]

    file_list = [img_parent_path + '/' + x.split('-')[0] + f'/{x}.tiff' for x in (set(file_list_names) - set(already_exist_files))]
    for img_path in tqdm.tqdm(file_list):
        pieces_save_path = pieces_path + '/' + os.path.basename(img_path).replace('.' + img_format, '').split("-")[0]
        os.makedirs(pieces_save_path, exist_ok=True)
        try:
            cut_img_to_pieces(img_path, pieces_save_path, img_format, is_1_level_need_convert=False)
        except Exception as e:
            shutil.rmtree(pieces_save_path)
            with open("error.txt", 'a') as f:
                f.write(repr(e) + img_path)
                f.write('\n')


def cut_img_to_pieces(img_file: str, save_folder, img_format, is_1_level_need_convert=False):
    tiff_dataset_temp = gdal.Open(img_file, gdal.GA_ReadOnly)
    # 1级产品到2级产品
    # sr = osr.SpatialReference()
    # sr.SetWellKnownGeogCS('WGS84')
    if is_1_level_need_convert and "L1" in img_file:
        img_file = img_file.replace('.' + img_format, '_GEO.' + img_format)
        tiff_dataset = gdal.Warp(img_file, tiff_dataset_temp, format='GTiff',
                                 resampleAlg=gdal.GRIORA_Bilinear, outputType=gdal.GDT_Int16, rpc=True)
    else:
        tiff_dataset = tiff_dataset_temp
    nBand, height, width = tiff_dataset.RasterCount, tiff_dataset.RasterYSize, tiff_dataset.RasterXSize
    h_list = list(range(0, height, img_piece_size[1]))
    h_list[-1] = height - img_piece_size[1]
    w_list = list(range(0, width, img_piece_size[0]))
    w_list[-1] = width - img_piece_size[0]
    for h_step in h_list:
        for w_step in w_list:
            img_data = tiff_dataset.ReadAsArray(w_step, h_step, img_piece_size[0], img_piece_size[1])[:3][::-1]
            img_data = np.transpose(img_data, (1, 2, 0))
            if "GF6" in os.path.basename(img_file):
                normalize_factor = 16
            elif "GF1" in os.path.basename(img_file):
                normalize_factor = 4
            else:
                raise Exception("Un Implement")
            img_piece = (img_data / normalize_factor).astype(np.uint8)
            io.imsave(save_folder + '/%s_%d_%d.tiff' %
                              (os.path.basename(img_file).replace('.' + img_format, ''), w_step, h_step), img_piece)


if __name__ == "__main__":
    get_pieces(img_parent_path, pieces_save_path, img_format, is_1_level_need_convert=False)
