import numpy as np
import cv2
import glob
import os
import tqdm
from skimage import io


def jaccard_numpy(rect, bboxes):
    intersection_left_bottom = np.maximum(rect[:2], bboxes[:, :2])
    intersection_right_top = np.minimum(rect[2:], bboxes[:, 2:])
    intersection_w_h = np.maximum(intersection_right_top - intersection_left_bottom + 1, 0)
    intersection = intersection_w_h[:, 0] * intersection_w_h[:, 1]
    rect_area = (rect[2] - rect[0] + 1) * (rect[3] - rect[1] + 1)
    bboxes_area = (bboxes[:, 2] - bboxes[:, 0] + 1) * (bboxes[:, 3] - bboxes[:, 1] + 1)
    iou = intersection / (rect_area + bboxes_area - intersection)
    return iou


def cut_with_label(file_list):
    for id, img_file in tqdm.tqdm(enumerate(file_list)):
        txt_file = img_file.replace('tiff', 'txt')
        bboxes = np.loadtxt(txt_file, ndmin=2)
        if len(bboxes) != 0:
            if bboxes[0][2] < 1:
                raise ValueError("标注格式有问题")
        else:
            bboxes = np.array([[-1, -1, -1, -1, -1]])
        img = io.imread(img_file)
        img_h, img_w, _ = img.shape
        w_list = list(range(0, img_w, SLICE_SIZE[0]))
        w_list[-1] = img_w - SLICE_SIZE[0]
        h_list = list(range(0, img_h, SLICE_SIZE[1]))
        h_list[-1] = img_h - SLICE_SIZE[1]

        x_start = float(img_file.split('_')[-2])
        y_start = float(img_file.split('_')[-1].replace('.tiff', ''))
        for w_start in w_list:
            for h_start in h_list:
                # convert to integer rect x1,y1,x2,y2
                rect = np.array([w_start, h_start, w_start+SLICE_SIZE[0], h_start+SLICE_SIZE[1]])
                # calculate IoU (jaccard overlap) b/t the cropped and gt boxes
                # overlap = jaccard_numpy(rect, bboxes[:, 1:])

                # cut the crop from the image
                img_data = img[h_start:(h_start + SLICE_SIZE[1]), w_start:(w_start + SLICE_SIZE[0]), :]

                # keep overlap with gt box IF center in sampled patch
                centers = (bboxes[:, 1:3] + bboxes[:, 3:]) / 2.0
                # mask in all gt boxes that above and to the left of centers
                m1 = (rect[0] < centers[:, 0]) * (rect[1] < centers[:, 1])
                # mask in all gt boxes that under and to the right of centers
                m2 = (rect[2] > centers[:, 0]) * (rect[3] > centers[:, 1])
                # mask in that both m1 and m2 are true
                mask = m1 * m2
                # have any valid boxes? try again if not
                current_boxes = None
                if mask.any():
                    # take only matching gt boxes
                    current_boxes = bboxes[mask, :].copy()
                    # should we use the box left and top corner or the crop's
                    current_boxes[:, 1:3] = np.maximum(current_boxes[:, 1:3], rect[:2])
                    # adjust to crop (by substracting crop's left,top)
                    current_boxes[:, 1:3] -= rect[:2]
                    current_boxes[:, 3:] = np.minimum(current_boxes[:, 3:], rect[2:])
                    # adjust to crop (by substracting crop's left,top)
                    current_boxes[:, 3:] -= rect[:2]
                file_name = '_'.join(os.path.basename(img_file).split('_')[:-2])
                img_save_path = SLICE_SAVED_PATH + '/' + os.path.basename(
                    os.path.dirname(img_file)) + '/' + file_name + '_' + repr(int(x_start + w_start)) + '_' + repr(
                    int(y_start + h_start)) + '.tiff'
                os.makedirs(os.path.dirname(img_save_path), exist_ok=True)
                io.imsave(img_save_path, img_data.astype(np.uint8))
                if current_boxes is None:
                    with open(img_save_path.replace('.tiff', '.txt'), 'w') as f:
                        pass
                else:
                    np.savetxt(img_save_path.replace('.tiff', '.txt'), current_boxes, fmt='%d %d %d %d %d')


if __name__ == '__main__':
    PATCH_PATH = r'K:\Positive_Patches'
    OVERLAP_RATE = 0.9
    SLICE_SIZE = (512, 512)
    SLICE_SAVED_PATH = r'K:\Positive_Patches\Slice'  # 切片保存的路径
    IMG_FORMAT = 'tiff'

    dir_list = glob.glob(PATCH_PATH + '/*')
    assert len(dir_list), PATCH_PATH + ' Empty!'
    if os.path.isfile(dir_list[int(len(dir_list) / 2)]):
        file_list = [x for x in dir_list if x.endswith(IMG_FORMAT)]
        cut_with_label(file_list)
    else:
        dir_list = [x for x in dir_list if os.path.isdir(x)]
        for dir in dir_list:
            file_list = glob.glob(dir + f'/*{IMG_FORMAT}')
            cut_with_label(file_list)

