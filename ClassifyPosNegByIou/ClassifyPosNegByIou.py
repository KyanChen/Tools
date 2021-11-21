import numpy as np
import glob
import os
import tqdm
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
    gt_path = r'F:\DataSet\sar_ship\SSDD数据以及标签\label_txt'
    proposal_path = r'F:\DataSet\sar_ship\SSDD数据以及标签\patch_txt'
    data = os.path.abspath(gt_path + r'/../' + 'data.txt')
    data_rate = os.path.abspath(gt_path + r'/../' + 'proposal_right_rate.txt')

    if os.path.exists(data):
        os.remove(data)
    data_writer = open(data, 'a')
    # gt框的数量
    gt_num = 0
    # 候选框数量
    proposal_num = 0
    # 正候选框数量
    proposal_pos_num = 0
    # 负候选框数量
    proposal_neg_num = 0
    # iou模糊候选框数量
    proposal_fuzzy_num = 0
    # 没有匹配到的gt数量
    gt_no_match_num = 0

    neg_threshold = 1e-7
    pos_threshold = 0.1

    proposal_file_list = glob.glob(proposal_path + r'/*.txt')
    pbar = tqdm.tqdm(total=len(proposal_file_list))
    for proposal_file in proposal_file_list:
        pbar.update(1)
        # gt_file = os.path.join(gt_path, os.path.basename(proposal_file).replace('8bits', 'label'))
        gt_file = os.path.join(gt_path, os.path.basename(proposal_file))
        proposal_all = parserTxt(proposal_file, is_with_classes=False)
        proposal_num += len(proposal_all)
        if not os.path.exists(gt_file) or os.path.getsize(gt_file) < 1:
            txt_writer(data_writer, np.insert(proposal_all[:, 4:], 0, 0, 1))
            continue
        gt_boxes = parserTxt(gt_file, is_with_classes=True)
        gt_num += len(gt_boxes)

        # 统计没有被候选框交叠过的gt
        gt_temp = np.zeros(len(gt_boxes))
        for idx, proposal_box in enumerate(proposal_all[:, 0:4]):
            iou = calculate_iou(proposal_box, gt_boxes)
            if np.any(iou > pos_threshold):
                gt_temp += iou > pos_threshold
                proposal_pos_num += 1
                txt_writer(data_writer, np.expand_dims(np.insert(proposal_all[idx, 4:], 0, 1, 0), axis=0))
            elif np.all(iou < neg_threshold):
                proposal_neg_num += 1
                txt_writer(data_writer, np.expand_dims(np.insert(proposal_all[idx, 4:], 0, 0, 0), axis=0))
            else:
                proposal_fuzzy_num += 1
        gt_no_match_num += np.sum(gt_temp == 0)
    pbar.close()
    with open(data_rate, 'w') as data_rate_f:
        str_ = "gt框数量: %d\n候选框数量: %d\n候选正样本框数量: %d\n候选负样本框数量: %d\niou模糊的候选样本框数量：%d\n没有候选框匹配的gt数量：%d" \
               % (gt_num, proposal_num, proposal_pos_num, proposal_neg_num, proposal_fuzzy_num, gt_no_match_num)
        data_rate_f.write(str_)


