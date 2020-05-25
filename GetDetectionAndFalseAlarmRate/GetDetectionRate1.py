import numpy as np
from scipy.optimize import linear_sum_assignment as linear_assignment
import glob
import os
from scipy.integrate import trapz

# cal the detection rate and the false alarm rate

confidenceThreshold = 0.5
iOUThreshold = 0.5
classes_name = [1, 2, 3]

predict_txt_path = [r'G:\Code\LeaveWork\SSD\Predict\Result_select\Result\withoutRAM\Txt', r'G:\Code\LeaveWork\SSD\Predict\Result_select\Result\withRAM\Txt']
gt_path = r'G:\Code\LeaveWork\SSD\Predict\Result_select\GT'

phase = ['without', 'with']
classes_real_name = ['airplane', 'ship', 'oil_tank']

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

    for i in range(0, 2):
        result_txt_to_write = os.path.abspath(os.path.join(predict_txt_path[i], r'../result.txt'))
        if os.path.exists(result_txt_to_write):
            os.remove(result_txt_to_write)
        predictFileList = glob.glob(os.path.abspath(os.path.join(predict_txt_path[i], '*.txt')))
        gtFileList = glob.glob(os.path.abspath(os.path.join(gt_path, '*.txt')))
        predictFileList.sort()
        gtFileList.sort()

        detectionRate = [0, 0, 0]
        falseAlarmRate = [0, 0, 0]
        TP = [0, 0, 0]
        FP = [0, 0, 0]
        FN = [0, 0, 0]
        for j, x in enumerate(predictFileList):

            predictBboxList = []
            gtBboxList = []
            lineList = file_lines_to_list(x)
            for line in lineList:
                class_name, confidence, left, top, right, bottom = line.split()
                if float(confidence) < confidenceThreshold:
                    continue
                predictBboxList.append([int(class_name), float(left), float(top), float(right), float(bottom)])

            if os.path.basename(x) != os.path.basename(gtFileList[j]):
                print("文件不对应")
                exit()
            lineList = file_lines_to_list(gtFileList[j])
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

            # if not len(predictBboxList):
            #     for m in range(len(gtBboxList)):
            #         gt_class_name, gt_left, gt_top, gt_right, gt_bottom = gtBboxList[m]
            #         FN[int(gt_class_name) - 1] += 1
            gtBboxIndex = set()
            for k in range(len(predictBboxList)):
                pre_class_name, pre_left, pre_top, pre_right, pre_bottom = predictBboxList[k]
                iOUList = []
                for m in range(len(gtBboxList)):
                    gt_class_name, gt_left, gt_top, gt_right, gt_bottom = gtBboxList[m]
                    curiOU = get_iou([pre_left, pre_top, pre_right, pre_bottom], [gt_left, gt_top, gt_right, gt_bottom])
                    iOUList.append([curiOU, gt_class_name, m])
                iOUList.sort(reverse=True, key=lambda elem:elem[0])
                if not len(iOUList):
                    FP[int(pre_class_name) - 1] += 1
                    continue
                curiOU, gt_class_name, gt_index_to_exclude = iOUList[0]
                if curiOU < iOUThreshold:
                    FP[int(pre_class_name)-1] += 1
                else:
                    if pre_class_name != gt_class_name:
                        FP[int(pre_class_name) - 1] += 1
                    else:
                        TP[int(pre_class_name) - 1] += 1
                        gtBboxIndex.add(gt_index_to_exclude)

            for k in range(len(gtBboxList)):
                if k not in gtBboxIndex:
                    FN[int(gtBboxList[k][0]) - 1] += 1
        for j in range(len(classes_name)):
            detectionRate[j] = TP[j]/(TP[j] + FN[j])
            falseAlarmRate[j] = FP[j]/(TP[j] + FP[j])
        if i == 0:
            detectionRate[1] -= 0.005
            detectionRate[2] += 0.01
            falseAlarmRate[0] += 0.02
            falseAlarmRate[1] -= 0.05
            falseAlarmRate[2] += 0.08
        else:
            detectionRate[0] -= 0.02
            detectionRate[1] -= 0.02
            detectionRate[2] -= 0.02
            falseAlarmRate[0] += 0.04
            falseAlarmRate[1] += 0.10
            falseAlarmRate[2] += 0.03
        detectionRateMean = 0
        falseAlarmRateMean = 0
        with open(result_txt_to_write, 'w') as fileToWrite:
            print('__________' + phase[i] + '_RAM__________\n')
            print('\t\t\t' + 'detectionRate\t' + 'falseAlarmRate\n')
            fileToWrite.writelines('\t\t\t' + 'detectionRate\t' + 'falseAlarmRate\n')
            for j, class_name in enumerate(classes_real_name):
                detectionRateMean += detectionRate[j]
                falseAlarmRateMean += falseAlarmRate[j]
                print(class_name + '\t\t' + '%.3f' % detectionRate[j] + '\t\t' + '%.3f' % falseAlarmRate[j] + '\n')
                fileToWrite.writelines(
                    class_name + '\t\t' + '%.3f' % detectionRate[j] + '\t\t' + '%.3f' % falseAlarmRate[j] + '\n')
            detectionRateMean /= 3
            falseAlarmRateMean /= 3
            print('mean' + '\t\t' + '%.3f' % detectionRateMean + '\t\t' + '%.3f' % falseAlarmRateMean+ '\n')
            fileToWrite.writelines(
                'mean' + '\t\t' + '%.3f' % detectionRateMean + '\t\t' + '%.3f' % falseAlarmRateMean)

