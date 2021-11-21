import numpy as np
import glob
import os
import tqdm
import matplotlib
import matplotlib.pyplot as plt

class_names = ['ship']


# 位置坐标转换
# left, top,  right,  bottom
# centerX, centerY, width, height
def pointsToCenter(boxes):
    return np.concatenate(
        ((boxes[:, :2] + boxes[:, 2:]) / 2, boxes[:, 2:] - boxes[:, :2]), 1)


def centerToPoints(boxes):
    return np.concatenate(
        (boxes[:, :2] - boxes[:, 2:] / 2, boxes[:, :2] + boxes[:, 2:] / 2), 1)


def calculate_iou(box, boxes):
    # 左上角
    LT = np.maximum(box[:2], boxes[:, :2])
    # 右下角
    RB = np.minimum(box[2:], boxes[:, 2:])
    wh = RB - LT
    wh[wh < 0] = 0
    # A∩B
    intersection = wh[:, 0] * wh[:, 1]
    # box和boxes的面积
    # shape 1
    area_a = (box[2] - box[0]) * (box[3] - box[1])
    # shape N
    area_b = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    iou_ = intersection / (1e-10 + area_a + area_b - intersection)

    return iou_


def parserTxt(file, is_with_classes=True):
    with open(file, 'r') as f:
        lines = np.array([i.split() for i in f.readlines()])
        if is_with_classes:
            # 取出gt_boxes
            boxes = lines[:, 1:].astype(np.float32)
        else:
            boxes = lines.astype(np.float32)
    return boxes


def txt_writer(f, numpy_data):
    for i in numpy_data:
        str_to_write = [str(j)+' ' for j in i]
        f.writelines(str_to_write)
        f.write('\n')


if __name__ == '__main__':
    gt_path = '/Users/keyanchen/Files/Dataset/704/SSDD数据以及标签/Txt'
    gt_path1 = '/Users/keyanchen/Files/Dataset/704/AIR-SARShip-1.0/Txt'
    gt_path2 = '/Users/keyanchen/Files/Dataset/704/ship_detection_online/Txt'
    file_list = glob.glob(os.path.join(gt_path, '*.txt'))
    file_list.extend(glob.glob(os.path.join(gt_path1, '*.txt')))
    file_list.extend(glob.glob(os.path.join(gt_path2, '*.txt')))
    pbar = tqdm.tqdm(total=len(file_list))
    bboxes = []
    for gt_file in file_list:
        pbar.update(1)
        gt_boxes = parserTxt(gt_file, is_with_classes=True)
        bboxes += gt_boxes.flatten().tolist()
    pbar.close()
    bboxes = np.array(bboxes).reshape(-1, 4)
    w = bboxes[:, 2] - bboxes[:, 0]
    h = bboxes[:, 3] - bboxes[:, 1]

    # 设置matplotlib正常显示中文和负号
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号

    """
    绘制直方图
    data:必选参数，绘图数据
    bins:直方图的长条形数目，可选项，默认为10
    normed:是否将得到的直方图向量归一化，可选项，默认为0，代表不归一化，显示频数。normed=1，表示归一化，显示频率。
    facecolor:长条形的颜色
    edgecolor:长条形边框的颜色
    alpha:透明度
    """
    plt.hist(w, bins=40, normed=0, facecolor="blue", edgecolor="black", alpha=0.7)
    # 显示横轴标签
    plt.xlabel("size")
    # 显示纵轴标签
    plt.ylabel("frequency")
    # 显示图标题
    plt.title("width")
    plt.show()

    plt.hist(h, bins=40, normed=0, facecolor="blue", edgecolor="black", alpha=0.7)
    # 显示横轴标签
    plt.xlabel("size")
    # 显示纵轴标签
    plt.ylabel("frequency")
    # 显示图标题
    plt.title("height")
    plt.show()
    print('max_w:%d\nmax_h:%d\nmin_w:%d\nmin_h:%d' % (max(w), max(h), min(w), min(h)))

