import glob
import os
import numpy as np
from skimage import io


# left top right bottom 2 cx cy width height
def corner2center(corner, w, h):
    if len(corner.shape) == 1:
        corner = np.expand_dims(corner, 0)
    center_xy = (corner[:, :2] + corner[:, 2:])/2
    center_wh = corner[:, 2:] - corner[:, :2]
    center = np.hstack([center_xy, center_wh])
    center[:, ::2] /= w
    center[:, 1::2] /= h
    return center


# cx cy width height 2 left top right bottom
def center2corner(center, w, h):
    if len(center.shape) == 1:
        center = np.expand_dims(center, 0)
    center[:, ::2] *= w
    center[:, 1::2] *= h
    corner_lt = center[:, :2] - center[:, 2:] / 2
    corner_rb = center[:, :2] + center[:, 2:] / 2
    corner = np.hstack([corner_lt, corner_rb])
    return corner


if __name__ == '__main__':

    in_path = r'F:\OneDrive\MyWork\Kaikeba\20201022公共场景下的口罩实时监测4,5\code\PyTorch-YOLOv3-master\data\mydata\train'
    img_list = glob.glob(in_path + '/*.jpg')
    for img_file in img_list:
        img = io.imread(img_file)
        h, w, _ = img.shape
        if not os.path.exists(img_file.replace('jpg', 'txt')):
            f = open(img_file.replace('jpg', 'txt'), 'w')
            f.close()
        data = np.loadtxt(img_file.replace('jpg', 'txt'), ndmin=2)
        if len(data) == 0:
            continue
        else:
            if data[0, 2] <= 1:
                data = np.hstack([data[:, 0, None], center2corner(data[:, 1:], w, h)])
            else:
                data = np.hstack([data[:, 0, None], corner2center(data[:, 1:], w, h)])
            np.savetxt(img_file.replace('jpg', 'txt'), data, fmt='%d %f %f %f %f')


