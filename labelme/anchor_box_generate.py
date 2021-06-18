import glob
import os
import sys
import xml.etree.ElementTree as ET
import numpy as np
from scipy.cluster.vq import kmeans
# from kmeans import kmeans, avg_iou

# 根文件夹
ROOT_PATH = 'E:\\OneDrive\\My_paper\\Program\\Track\\YOLOtrain\\datawithlabel\\NIT'
# 聚类的数目
CLUSTERS = 3
# 模型中图像的输入尺寸，默认是一样的
SIZE = 640


# 需要加载yolo训练数据和lable
def load_dataset(path):
    # jpegimages = os.path.join(path, 'JPEGImages')
    # if not os.path.exists(jpegimages):
    #     print('no JPEGImages folders, program abort')
    #     sys.exit(0)
    labels_txt = os.path.join(path, 'labels')
    if not os.path.exists(labels_txt):
        print('no labels folders, program abort')
        sys.exit(0)

    label_file = os.listdir(labels_txt)
    print('label count: {}'.format(len(label_file)))
    dataset = []

    for label in label_file:
        with open(os.path.join(labels_txt, label), 'r') as f:
            txt_content = f.readlines()

        for line in txt_content:
            line_split = line.split(' ')
            line_split.pop()
            roi_with = float(line_split[len(line_split) - 3])
            roi_height = float(line_split[len(line_split) - 2])
            if roi_with == 0 or roi_height == 0:
                continue
            dataset.append([roi_with, roi_height])
            # print([roi_with, roi_height])

    return np.array(dataset)


data = load_dataset(ROOT_PATH)
out = kmeans(data, CLUSTERS, iter=1000)  # 对训练样本聚类

print(out)
out = out[0]
# print("Accuracy: {:.2f}%".format(avg_iou(data, out) * 100))
print("Boxes:\n {}-{}".format(out[:, 0] * SIZE, out[:, 1] * SIZE))

ratios = np.around(out[:, 0] / out[:, 1], decimals=2).tolist()
print("Ratios:\n {}".format(sorted(ratios)))