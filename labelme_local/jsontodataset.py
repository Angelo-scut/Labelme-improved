import argparse
import json
import os
import os.path as osp
import warnings
import copy
import numpy as np
import PIL.Image
from PIL import Image
# from skimage import io
import yaml
import cv2
from labelme_local import utils
import random

def ellipse_type(json_file, list, out, img_size):
    for i in range(0, len(list)):
        path = os.path.join(json_file, list[i])  # 获取每个json文件的绝对路径
        filename = list[i][:-5]  # 提取出.json前的字符作为文件名，以便后续保存Label图片的时候使用
        extension = list[i][-4:]
        if extension == 'json':
            if os.path.isfile(path):
                data = json.load(open(path))
                img = utils.image.img_b64_to_arr(data['imageData'])  # 根据'imageData'字段的字符可以得到原图像
                # lbl为label图片（标注的地方用类别名对应的数字来标，其他为0）lbl_names为label名和数字的对应关系字典
                lbl, lbl_names = utils.shape.labelme_shapes_to_label(img.shape, data[
                    'shapes'])  # data['shapes']是json文件中记录着标注的位置及label等信息的字段

                ebbx = utils.shape.bbox_for_eliipse(img.shape, data['shapes'])
                # captions = ['%d: %s' % (l, name) for l, name in enumerate(lbl_names)]
                lbl_viz = utils.shape.ellipse_with_angle(img, ebbx[1] * img.shape[1], ebbx[2] * img.shape[0],
                                                         ebbx[3] * img.shape[1], ebbx[4] * img.shape[0], ebbx[5],
                                                         255)  # cx/img_shape[1], cy/img_shape[0], a/img_shape[1], b/img_shape[0]
                # lbl_viz = utils.draw.draw_label(lbl, img, captions)
                out_dir = out + osp.basename(list[i])[:-5]
                out_dir = osp.join(osp.dirname(list[i]), out_dir)
                if not osp.exists(out_dir):
                    os.mkdir(out_dir)
                #
                # bmask = np.array(lbl)
                # bmask = bmask.astype(np.bool8)
                # color_mask = np.array([255, 0, 0], dtype=np.uint8)
                # im = np.array(img)
                # im[bmask] = im[bmask] * 0.5 + color_mask * 0.5
                # im = Image.fromarray(im)
                # im.save(osp.join(out_dir, '{}_visual.png'.format(filename)))

                img_path = out + 'images\\'
                label_path = out + 'labels\\'
                r = img_size / max(img.shape[0], img.shape[1])  # ratio 即需要将最长边缩放到设定的img_size(640)
                img = cv2.resize(img, (int(img.shape[1] * r), int(img.shape[0] * r)),
                                 interpolation=cv2.INTER_AREA if r < 1 else cv2.INTER_LINEAR)
                PIL.Image.fromarray(img).save(osp.join(img_path, '{}.png'.format(filename)))
                # PIL.Image.fromarray(img).save(osp.join(out_dir, '{}_source.png'.format(filename)))
                PIL.Image.fromarray(lbl).save(osp.join(out_dir, '{}_mask.png'.format(filename)))
                PIL.Image.fromarray(lbl_viz).save(osp.join(out_dir, '{}_viz.jpg'.format(filename)))

                # with open(osp.join(out_dir, 'label_names.txt'), 'w') as f:
                #     for lbl_name in lbl_names:
                #         f.write(lbl_name + '\n')

                if ebbx:
                    with open(osp.join(label_path, '{}.txt'.format(filename)), 'w') as f:
                        for e in range(len(ebbx)):
                            if e == 0:
                                f.write(str(ebbx[e]) + ' ')
                            elif e == len(ebbx) - 1:
                                f.write(str(format(ebbx[e], '.4f')))
                            else:
                                f.write(str(format(ebbx[e], '.4f')) + ' ')


def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument('json_file')   # 标注文件json所在的文件夹
    # parser.add_argument('-o', '--out', default=None)
    # args = parser.parse_args()
    img_size = 640
    json_file = "./testimage"  # args.json_file
    out = "./testimage/"
    color_mask = np.array([255, 0, 0], dtype=np.uint8)  # 可是化的颜色
    list = os.listdir(json_file)  # 获取json文件列表
    # ellipse_type(json_file, list, out, img_size)
    for i in range(0, len(list)):
        path = os.path.join(json_file, list[i])  # 获取每个json文件的绝对路径
        filename = list[i][:-5]  # 提取出.json前的字符作为文件名，以便后续保存Label图片的时候使用
        extension = list[i][-4:]
        if extension == 'json':
            if os.path.isfile(path):
                data = json.load(open(path))
                img = utils.image.img_b64_to_arr(data['imageData'])  # 根据'imageData'字段的字符可以得到原图像
                # lbl为label图片（标注的地方用类别名对应的数字来标，其他为0）lbl_names为label名和数字的对应关系字典
                lbl, lbl_names = utils.shape.labelme_shapes_to_label(img.shape, data['shapes'],
                                                                     isClose=False)  # data['shapes']是json文件中记录着标注的位置及label等信息的字段
                out_dir = out + osp.basename(list[i])[:-5]
                out_dir = osp.join(osp.dirname(list[i]), out_dir)
                if not osp.exists(out_dir):
                    os.mkdir(out_dir)
                PIL.Image.fromarray(lbl).save(osp.join(out_dir, '{}_mask.png'.format(filename)))


def checkmsak():
    mask = Image.open('./testimage/back10166/back10166_mask.png').convert('L')
    im = Image.open('./testimage/back10166.png')
    mask1 = mask
    mask.putpalette([0, 0, 0,
                     255, 0, 0,
                     0, 0, 0])
    # mask1 = np.array(mask1)
    # bmask = mask1
    # bmask = bmask.astype(np.bool8)
    # color_mask = np.array([255, 0, 0], dtype=np.uint8)
    # im = np.array(im)
    # im[bmask] = im[bmask] * 0.5 + color_mask * 0.5
    # im = Image.fromarray(im)
    mask.show()
    # im.show()


def lwlabel(file_path, out_path):
    file_list = os.listdir(file_path)
    parent_path = ["train", "val"]
    child_path = ["Image", "Label", "visual"]
    for parent in parent_path:
        temp_path = os.path.join(out_path, parent)
        if not osp.exists(temp_path):
            os.mkdir(temp_path)
        for child in child_path:
            temp_path = os.path.join(out_path, parent, child)
            if not osp.exists(temp_path):
                os.mkdir(temp_path)
    train_file_path = os.path.join(out_path, "train")
    val_file_path = os.path.join(out_path, "val")
    color_list = [[0, 255, 255],
                  [0, 255, 0],
                  [255, 0, 0],
                  [255, 255, 0]]
    a, b = 150, 650
    # from sklearn.model_selection import train_test_split
    # train, test = train_test_split(file_list, test_size=0.2, random_state=42)
    # file_list = test
    # file_list = ["Q226.json"]
    train_num, val_num = 0, 0
    isTest = True
    for i in range(0, len(file_list)):
        path = os.path.join(file_path, file_list[i])  # 获取每个json文件的绝对路径
        filename = file_list[i][:-5]  # 提取出.json前的字符作为文件名，以便后续保存Label图片的时候使用
        extension = file_list[i][-4:]
        if extension == 'json':
            if os.path.isfile(path):
                random_num = random.randint(0, 100)
                data = json.load(open(path))
                img = cv2.imread(os.path.join(file_path, filename) + '.jpg', 1)
                # img = utils.image.img_b64_to_arr(data['imageData'])  # 根据'imageData'字段的字符可以得到原图像
                # remember to change the "label_name_to_value"
                lbl, lbl_names = utils.shape.labelme_shapes_to_label(img.shape, data['shapes'], line_width=1, isClose=True)
                # img = img[a:, (b-400):(b+400)]
                # lbl = lbl[a:, (b-400):(b+400)]
                # img = img[:, 300:1000, :]
                # lbl = lbl[:, 300:1000]
                if random_num < 80 and not isTest:
                    cv2.imwrite(osp.join(train_file_path, 'Label', '{}.png'.format(str(train_num))), lbl.astype(np.uint8))
                    cv2.imwrite(osp.join(train_file_path, 'Image', '{}.jpg'.format(str(train_num))), img.astype(np.uint8))
                    train_num += 1
                else:
                    cv2.imwrite(osp.join(val_file_path, 'Label', '{}.png'.format(str(val_num))), lbl.astype(np.uint8))
                    cv2.imwrite(osp.join(val_file_path, 'Image', '{}.jpg'.format(str(val_num))), img.astype(np.uint8))
                    val_num += 1
                # PIL.Image.fromarray(lbl).save(osp.join(out_path, '{}_mask.png'.format(filename)), format='PNG')
                # PIL.Image.fromarray(img).save(osp.join(out_path, '{}.png'.format(filename)))
                # img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
                for j in range(1, lbl.max()+1):
                    temp = lbl.copy()
                    temp[temp != j] = 0
                    temp[temp == j] = 1
                    temp = temp.astype(np.bool8)
                    color_mask = np.array(color_list[j-1], dtype=np.uint8)
                    img[temp] = img[temp] * 0.8 + color_mask * 0.2
                if random_num < 80 and not isTest:
                    cv2.imwrite(osp.join(train_file_path, 'visual', '{}_visual.jpg'.format(str(train_num))),
                                img.astype(np.uint8))
                else:
                    cv2.imwrite(osp.join(val_file_path, 'visual', '{}_visual.jpg'.format(str(val_num))),
                                img.astype(np.uint8))
                cv2.waitKey(5)
                # PIL.Image.fromarray(img).save(osp.join(out_visual, '{}_visual.png'.format(filename)))
    print(train_num)
    print(val_num)


if __name__ == '__main__':
    # main()
    # print('Finished!')
    # checkmsak()
    file_path = "E:/OneDrive/My_paper/Program/xsStereoVision/data/HomographyTransform/3/test_10mm304_520A-560A"
    save_path = "E:/OneDrive/My_paper/Program/xsStereoVision/data/HomographyTransform/3/data"
    lwlabel(file_path, save_path)
    # img = cv2.imread("E:\OneDrive\My_paper\Program\Gapcontrol\data\\0713\\train\weldpool\\test\\test\\35_mask.png", 0)
    # img = img * 100
    # print(np.max(img))
    # cv2.imshow("s", img)
    # cv2.waitKey()