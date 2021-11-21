import numpy as np
# from scipy.optimize import linear_sum_assignment as linear_assignment
import glob
import os
# from scipy.integrate import trapz

# cal the detection rate and the false alarm rate

confidenceThreshold = 0.2
iOUThreshold = 0.005

predict_txt_path = r'G:\Coding\EfficientDet\EvalResults'
gt_path = r'F:\DataSet\GF1_2\total_data\val_refine'

classes_name = ['1', '2', '3']


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
    score = area / (((bb_test[2] - bb_test[0]) * (bb_test[3] - bb_test[1])
                    + (bb_gt[2] - bb_gt[0]) * (bb_gt[3] - bb_gt[1]) - area) + 1e-10)
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
    result_txt_to_write = os.path.abspath(predict_txt_path + '/../result.txt')
    predictFileList = glob.glob(predict_txt_path + '/*.txt')

    detectionRate = np.zeros(len(classes_name))
    falseAlarmRate = np.zeros(len(classes_name))
    TP = np.zeros(len(classes_name))
    FP = np.zeros(len(classes_name))
    FN = np.zeros(len(classes_name))
    for idx, pred_file in enumerate(predictFileList):
        predictBboxList = []
        gtBboxList = []
        lineList = file_lines_to_list(pred_file)
        for line in lineList:
            try:
                class_name, confidence, left, top, right, bottom = line.split()
                if float(confidence) < confidenceThreshold:
                    continue
            except:
                class_name, left, top, right, bottom = line.split()
            predictBboxList.append([class_name, float(left), float(top), float(right), float(bottom)])

        gt_file = gt_path + '/' + os.path.basename(pred_file)
        if not os.path.exists(gt_file):
            print("Not Found: " + gt_file)
        else:
            lineList = file_lines_to_list(gt_file)
            for line in lineList:
                try:
                    class_name, left, top, right, bottom = line.split()
                except:
                    _, class_name, left, top, right, bottom = line.split()
                if class_name not in classes_name:
                    continue
                gtBboxList.append([class_name, float(left), float(top), float(right), float(bottom)])

        gtBboxIndex = set()
        for k in range(len(predictBboxList)):
            pre_class_name, pre_left, pre_top, pre_right, pre_bottom = predictBboxList[k]
            iOUList = []
            for m in range(len(gtBboxList)):
                gt_class_name, gt_left, gt_top, gt_right, gt_bottom = gtBboxList[m]
                curiOU = get_iou([pre_left, pre_top, pre_right, pre_bottom], [gt_left, gt_top, gt_right, gt_bottom])
                iOUList.append([curiOU, gt_class_name, m])
            iOUList.sort(reverse=True, key=lambda elem: elem[0])
            if not len(iOUList):
                FP[classes_name.index(pre_class_name)] += 1
                continue
            curiOU, gt_class_name, gt_index_to_exclude = iOUList[0]
            if curiOU < iOUThreshold:
                FP[classes_name.index(pre_class_name)] += 1
            else:
                if pre_class_name != gt_class_name:
                    FP[classes_name.index(pre_class_name)] += 1
                else:
                    TP[classes_name.index(pre_class_name)] += 1
                    gtBboxIndex.add(gt_index_to_exclude)

        for k in range(len(gtBboxList)):
            if k not in gtBboxIndex:
                FN[classes_name.index(gtBboxList[k][0])] += 1
    for k in range(len(classes_name)):
        detectionRate[k] = TP[k]/(TP[k] + FN[k])
        falseAlarmRate[k] = FP[k]/(TP[k] + FP[k])
    detectionRateMean = 0
    falseAlarmRateMean = 0
    with open(result_txt_to_write, 'w') as fileToWrite:
        print('\t\t\t' + 'detectionRate\t' + 'falseAlarmRate\n')
        fileToWrite.writelines('\t\t\t' + 'detectionRate\t' + 'falseAlarmRate\n')
        for class_id, class_name in enumerate(classes_name):
            detectionRateMean += detectionRate[class_id]
            falseAlarmRateMean += falseAlarmRate[class_id]
            print(class_name + '\t\t' + '%.3f' % detectionRate[class_id] + '\t\t' + '%.3f' % falseAlarmRate[class_id] + '\n')
            fileToWrite.writelines(
                class_name + '\t\t' + '%.3f' % detectionRate[class_id] + '\t\t' + '%.3f' % falseAlarmRate[class_id] + '\n')
        detectionRateMean /= len(classes_name)
        falseAlarmRateMean /= len(classes_name)
        print('mean' + '\t\t' + '%.3f' % detectionRateMean + '\t\t' + '%.3f' % falseAlarmRateMean + '\n')
        fileToWrite.writelines(
            'mean' + '\t\t' + '%.3f' % detectionRateMean + '\t\t' + '%.3f' % falseAlarmRateMean)

