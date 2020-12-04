import gdal
import numpy as np
import cv2

img_file = r''
output_img = r''
down_sample_factor = 100


tiff_dataset = gdal.Open(img_file)
nBand, y, x = tiff_dataset.RasterCount, tiff_dataset.RasterYSize, tiff_dataset.RasterXSize

buf_xsize = int(x/down_sample_factor)
buf_ysize = int(y/down_sample_factor)
buf = np.zeros((buf_ysize, buf_xsize, 3), dtype=int)
for i in range(3):
    buf[i] = tiff_dataset.GetRasterBand(i).ReadAsArray(0, 0, buf_ysize, buf_xsize,
                                                       buf[i], buf_ysize, buf_xsize)

img_out = (buf / 4).astype(np.uint8)
cv2.imwrite(output_img, img_out)