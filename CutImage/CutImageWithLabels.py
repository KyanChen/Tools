ratios = self.ratios.copy()
        # 需要调整两处的crop的w,h
        height, width, _ = img.shape
        if len(bboxes) == 0:
            if np.random.random() < self.prob and Config.IS_SRC_IMG_SIZE_NEAR_NET_SIZE:
                return img, bboxes, label
            while True:
                w = np.random.uniform(min(width - 1, ratios[0] * Config.INPUT_SIZE[0]),
                                      min(width, ratios[1] * Config.INPUT_SIZE[0]))
                h = np.random.uniform(min(height - 1, ratios[0] * Config.INPUT_SIZE[1]),
                                      min(height, ratios[1] * Config.INPUT_SIZE[1]))
                # aspect ratio constraint b/t .5 & 2
                if h / w < 8. / 10 or h / w > 10. / 8:
                    if not width / height < 8. / 10 or width / height > 10. / 8:
                        continue
                left = np.random.uniform(0, width - w)
                top = np.random.uniform(0, height - h)

                # convert to integer rect x1,y1,x2,y2
                rect = np.array(
                    [max(0, int(left)), max(0, int(top)), min(width - 1, int(left + w)), min(height - 1, int(top + h))])
                img = img[rect[1]:rect[3], rect[0]:rect[2], :]
                return img, bboxes, label
        if Config.IS_BBOX_SCALE_VARY_MUCH:
            bboxes_max_width = max(bboxes[:, 2] - bboxes[:, 0])
            bboxes_max_height = max(bboxes[:, 3] - bboxes[:, 1])

            max_width_ratio = bboxes_max_width / Config.INPUT_SIZE[0]
            max_height_ratio = bboxes_max_height / Config.INPUT_SIZE[1]
            max_ratio = max(max_width_ratio, max_height_ratio)
            if max_ratio > 1:
                ratios *= max_ratio
            elif max_ratio < 0.1:
                ratios *= 0.8
        for _ in range(6):
            for _ in range(40):
                if np.random.random() < self.prob and Config.IS_SRC_IMG_SIZE_NEAR_NET_SIZE:
                    return img, bboxes, label
                # randomly choose a mode
                mode = self.sample_options[np.random.randint(0, 5)]

                min_iou, max_iou = mode
                if min_iou is None:
                    min_iou = float('-inf')
                if max_iou is None:
                    max_iou = float('inf')

                # max trails (50)
                for _ in range(150):
                    current_img = img
                    # generate w and h
                    w = np.random.uniform(min(width-1, ratios[0] * Config.INPUT_SIZE[0]), min(width, ratios[1] * Config.INPUT_SIZE[0]))
                    h = np.random.uniform(min(height-1, ratios[0] * Config.INPUT_SIZE[1]), min(height, ratios[1] * Config.INPUT_SIZE[1]))
                    # aspect ratio constraint b/t .5 & 2
                    if h / w < 7. / 10 or h / w > 10. / 7:
                        if not width / height < 7. / 10 or width / height > 10. / 7:
                            continue
                    left = np.random.uniform(0, width - w)
                    top = np.random.uniform(0, height - h)

                    # convert to integer rect x1,y1,x2,y2
                    rect = np.array([max(0, int(left)), max(0, int(top)), min(width-1, int(left+w)), min(height-1, int(top+h))])

                    # calculate IoU (jaccard overlap) b/t the cropped and gt boxes
                    overlap = jaccard_numpy(bboxes, rect)

                    # is min and max overlap constraint satisfied? if not try again
                    if overlap.min() < min_iou and max_iou > overlap.max():
                        continue

                    # cut the crop from the image
                    current_img = current_img[rect[1]:rect[3], rect[0]:rect[2], :]

                    # keep overlap with gt box IF center in sampled patch
                    centers = (bboxes[:, :2] + bboxes[:, 2:]) / 2.0

                    # mask in all gt boxes that above and to the left of centers
                    m1 = (rect[0] < centers[:, 0]) * (rect[1] < centers[:, 1])

                    # mask in all gt boxes that under and to the right of centers
                    m2 = (rect[2] > centers[:, 0]) * (rect[3] > centers[:, 1])

                    # mask in that both m1 and m2 are true
                    mask = m1 * m2

                    # have any valid boxes? try again if not
                    if not mask.any():
                        continue

                    # take only matching gt boxes
                    current_boxes = bboxes[mask, :].copy()

                    # take only matching gt label
                    current_label = label[mask]

                    # should we use the box left and top corner or the crop's
                    current_boxes[:, :2] = np.maximum(current_boxes[:, :2], rect[:2])
                    # adjust to crop (by substracting crop's left,top)
                    current_boxes[:, :2] -= rect[:2]

                    current_boxes[:, 2:] = np.minimum(current_boxes[:, 2:], rect[2:])
                    # adjust to crop (by substracting crop's left,top)
                    current_boxes[:, 2:] -= rect[:2]

                    return current_img, current_boxes, current_label
            ratios *= 1.2