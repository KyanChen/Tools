import numpy as np
import glob
import os
import shutil
from scipy.optimize import linear_sum_assignment as linear_assignment

# cal the detection rate and the false alarm rate

confidenceThreshold = 0.5
iOUThreshold = 0.4
classes_name = [1, 2, 3]

predict_txt_path = [r'Predict\Result\withoutRAM\Txt', r'Predict\Result\withRAM\Txt']
gt_path = r'Predict\Groundtruth'
img_path = r'Predict\Img'
img_path_to_copy = r'Predict\Img_select'
GT_path_to_copy = r'Predict\GT_select'
without_path_to_copy = r'Predict\without'
with_path_to_copy = r'Predict\with'
if os.path.exists(without_path_to_copy):
    shutil.rmtree(without_path_to_copy)
os.makedirs(without_path_to_copy)
if os.path.exists(with_path_to_copy):
    shutil.rmtree(with_path_to_copy)
os.makedirs(with_path_to_copy)

if os.path.exists(img_path_to_copy):
    shutil.rmtree(img_path_to_copy)
os.makedirs(img_path_to_copy)
if os.path.exists(GT_path_to_copy):
    shutil.rmtree(GT_path_to_copy)
os.makedirs(GT_path_to_copy)

def get_iou(bb_test, bb_gt):
    '''
    Computes IOU between two bboxes in the form [x1,y1,x2,y2]
    Parameters:
        bb_test: [x1,y1,x2,y2,...]
        bb_ground: [x1,y1,x2,y2,...]
    Returns:
        score: float, takes values between 0 and 1.
        score = Area(bb_test intersects bb_gt)/Area(bb_test unions bb_gt)
    '''
    xx1 = max(bb_test[0], bb_gt[0])
    yy1 = max(bb_test[1], bb_gt[1])
    xx2 = min(bb_test[2], bb_gt[2])
    yy2 = min(bb_test[3], bb_gt[3])
    w = max(0., xx2 - xx1)
    h = max(0., yy2 - yy1)
    area = w * h
    score = area / ((bb_test[2] - bb_test[0]) * (bb_test[3] - bb_test[1])
                    + (bb_gt[2] - bb_gt[0]) * (bb_gt[3] - bb_gt[1]) - area)
    return score

def assign(predict_boxes, real_boxes):
    iou_metric = []
    for box in predict_boxes:
        temp_iou = []
        for box2 in real_boxes:
            temp_iou.append(get_iou(box, box2))
        iou_metric.append(temp_iou)
    iou_metric = np.array(iou_metric)
    result = linear_assignment(-iou_metric)
    output = []
    output_iou = []
    for idx in range(len(result)):
        if iou_metric[result[idx][0],result[idx][1]] > iou_thresh:
            output.append(result[idx])
            output_iou.append(iou_metric[result[idx][0],result[idx][1]])
    return output, output_iou


#       predict
#     yes    no
# yes  TP    FN    real
# no   FP    TN

# acc = (TP + TN)/(TP+FN+FP+TN)
# recall = TP/(TP + FN)
#
# 调节score阈值，算出召回率从0到1时的准确率，得到一条曲线
# 计算曲线的下面积 则为AP


def get_auc(xy_arr):
    # 计算曲线下面积即AUC
    auc = 0.
    prev_x = 0
    for x, y in xy_arr:
        if x != prev_x:
            auc += (x - prev_x) * y
            prev_x = x
    x = [_v[0] for _v in xy_arr]
    y = [_v[1] for _v in xy_arr]
    # 画出auc图
    # plt.ylabel("False Positive Rate")
    # plt.plot(x, y)
    # plt.show()
    # print(xy_arr)
    return auc

def caculate_AP(predict_boxes, real_boxes):
    recall_arr = []
    acc_arr = []
    xy_arr = []
    score_arr = list(map(lambda input:float(input)*0.01, range(0, 101)))
    for score in score_arr:
        temp_predict_boxes = []
        for box in predict_boxes:
            if box[4]>score:
                temp_predict_boxes.append(box)
        result,_ = assign(temp_predict_boxes, real_boxes)
        TP = len(result)
        FN = len(real_boxes) - TP
        FP = len(temp_predict_boxes) - TP
        recall = TP/(TP+FN)
        acc = TP/(TP+FN+FP)
        recall_arr.append(recall)
        acc_arr.append(acc)
        xy_arr.append([recall,acc])
    return get_auc(xy_arr)


def get_mAP(all_predict_boxes, all_real_boxes):
    ap_arr = []
    for idx in range(len(all_predict_boxes)):
        ap_arr.append(caculate_AP(all_predict_boxes[idx], all_real_boxes[idx]))
    return np.mean(ap_arr)

def file_lines_to_list(path):
    with open(path) as f:
        content = f.readlines()
    # remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content


if __name__ == '__main__':

    predictFileList_without = glob.glob(os.path.join(predict_txt_path[0], '*.txt'))
    predictFileList_with = glob.glob(os.path.join(predict_txt_path[1], '*.txt'))
    gtFileList = glob.glob(os.path.join(gt_path, '*.txt'))
    predictFileList_without.sort()
    predictFileList_with.sort()
    gtFileList.sort()

    for i in range(len(gtFileList)):
        TP_without = [0, 0, 0]
        TP_with = [0, 0, 0]
        FP_without = [0, 0, 0]
        FP_with = [0, 0, 0]
        FN_without = [0, 0, 0]
        FN_with = [0, 0, 0]
        predictBboxList_without = []
        predictBboxList_with = []
        gtBboxList = []

        lineList = file_lines_to_list(predictFileList_without[i])
        for line in lineList:
            class_name, confidence, left, top, right, bottom = line.split()
            if float(confidence) < confidenceThreshold:
                continue
            predictBboxList_without.append([int(class_name), float(left), float(top), float(right), float(bottom)])

        lineList = file_lines_to_list(predictFileList_with[i])
        for line in lineList:
            class_name, confidence, left, top, right, bottom = line.split()
            if float(confidence) < confidenceThreshold:
                continue
            predictBboxList_with.append([int(class_name), float(left), float(top), float(right), float(bottom)])

        if os.path.basename(predictFileList_without[i]) != os.path.basename(gtFileList[i])\
                or os.path.basename(predictFileList_with[i]) != os.path.basename(gtFileList[i]):
            print("文件不对应")
            exit()
        lineList = file_lines_to_list(gtFileList[i])

        for line in lineList:
            class_name, left, top, right, bottom = line.split()
            if not (int(class_name) in classes_name):
                continue
            top = float(top) * 512 / 600
            left = float(left) * 512 / 800
            bottom = float(bottom) * 512 / 600
            right = float(right) * 512 / 800

            top = 0 if top < 0 else top
            left = 0 if left < 0 else left
            bottom = 512 if bottom > 512 else bottom
            right = 512 if right > 512 else right
            gtBboxList.append([int(class_name), float(left), float(top), float(right), float(bottom)])

        gtBboxIndex = set()
        for j in range(len(predictBboxList_without)):
            pre_class_name, pre_left, pre_top, pre_right, pre_bottom = predictBboxList_without[j]
            iOUList = []
            for k in range(len(gtBboxList)):
                gt_class_name, gt_left, gt_top, gt_right, gt_bottom = gtBboxList[k]
                curiOU = get_iou([pre_left, pre_top, pre_right, pre_bottom], [gt_left, gt_top, gt_right, gt_bottom])
                iOUList.append([curiOU, gt_class_name, k])
            iOUList.sort(reverse=True, key=lambda elem: elem[0])
            if not len(iOUList):
                FP_without[int(pre_class_name) - 1] += 1
                continue
            curiOU, gt_class_name, gt_index_to_exclude = iOUList[0]
            if curiOU < iOUThreshold:
                FP_without[int(pre_class_name)-1] += 1
            else:
                if pre_class_name != gt_class_name:
                    FP_without[int(pre_class_name) - 1] += 1
                else:
                    TP_without[int(pre_class_name) - 1] += 1
                    gtBboxIndex.add(gt_index_to_exclude)

        for j in range(len(gtBboxList)):
            if j not in gtBboxIndex:
                FN_without[int(gtBboxList[j][0]) - 1] += 1

        gtBboxIndex.clear()
        for j in range(len(predictBboxList_with)):
            pre_class_name, pre_left, pre_top, pre_right, pre_bottom = predictBboxList_with[j]
            iOUList = []
            for k in range(len(gtBboxList)):
                gt_class_name, gt_left, gt_top, gt_right, gt_bottom = gtBboxList[k]
                curiOU = get_iou([pre_left, pre_top, pre_right, pre_bottom], [gt_left, gt_top, gt_right, gt_bottom])
                iOUList.append([curiOU, gt_class_name, k])
            iOUList.sort(reverse=True, key=lambda elem: elem[0])
            if not len(iOUList):
                FP_with[int(pre_class_name) - 1] += 1
                continue
            curiOU, gt_class_name, gt_index_to_exclude = iOUList[0]
            if curiOU < iOUThreshold:
                FP_with[int(pre_class_name) - 1] += 1
            else:
                if pre_class_name != gt_class_name:
                    FP_with[int(pre_class_name) - 1] += 1
                else:
                    TP_with[int(pre_class_name) - 1] += 1
                    gtBboxIndex.add(gt_index_to_exclude)

        for j in range(len(gtBboxList)):
            if j not in gtBboxIndex:
                FN_with[int(gtBboxList[j][0]) - 1] += 1

        img_file = os.path.abspath(os.path.join(img_path, os.path.basename(gtFileList[i]).replace('.txt', '.jpg')))
        img_file_to_copy = os.path.join(img_path_to_copy, os.path.basename(img_file))
        GT_file_to_copy = os.path.join(GT_path_to_copy, os.path.basename(gtFileList[i]))

        flag_class_without = [False, False, False]
        flag_class_with = [False, False, False]

        detectionRate_without = [0.40, 0.45, 0.7]
        detectionRate_with = [0.5, 0.5, 0.5]
        falseAlarmRate_without = [0.8, 0.8, 0.8]
        falseAlarmRate_with = [0.7, 0.7, 0.7]
        for j in range(len(classes_name)):
            if (TP_without[j] + FN_without[j]) == 0 or\
                    TP_without[j] / (TP_without[j] + FN_without[j]) > detectionRate_without[j]:
                if (TP_without[j] + FP_without[j]) == 0 or\
                        FP_without[j] / (TP_without[j] + FP_without[j]) < falseAlarmRate_without[j]:
                    flag_class_without[j] = True

            if (TP_with[j] + FN_with[j]) == 0 or\
                    TP_with[j] / (TP_with[j] + FN_with[j]) > detectionRate_with[j]:
                if (TP_with[j] + FP_with[j]) == 0 or\
                        FP_with[j] / (TP_with[j] + FP_with[j]) < falseAlarmRate_with[j]:
                    flag_class_with[j] = True

        if all(flag_class_without) and all(flag_class_with):
            shutil.copy(img_file, img_file_to_copy)
            shutil.copy(gtFileList[i], GT_file_to_copy)
            shutil.copy(predictFileList_without[i], without_path_to_copy)
            shutil.copy(predictFileList_with[i], with_path_to_copy)

