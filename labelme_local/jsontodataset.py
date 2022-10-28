import argparse
import base64
import json
import os
import os.path as osp
import sys

def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)
this_dir = osp.dirname(__file__)
lib_path = osp.join(this_dir, '..')
add_path(lib_path)

import imgviz
import PIL.Image
import numpy as np
import cv2
import random

from labelme_local.logger import logger
from labelme_local import utils


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


def main(args):
    json_file = args.json_file
    if json_file is None:
        assert "json_file must be an existed path!"
    if args.out is None:
        out_dir = osp.join(json_file, "..", 'label_output')
    else:
        out_dir = args.out
    if not osp.exists(out_dir):
        os.mkdir(out_dir)

    filelist = os.listdir(json_file)
    for i in range(0, len(filelist)):
        path = osp.join(json_file, filelist[i])
        if osp.splitext(filelist[i])[-1] == ".json":
            data = json.load(open(path))
            imageData = data.get("imageData")

            if not imageData:
                imagePath = os.path.join(os.path.dirname(json_file), data["imagePath"])
                with open(imagePath, "rb") as f:
                    imageData = f.read()
                    imageData = base64.b64encode(imageData).decode("utf-8")
            img = utils.img_b64_to_arr(imageData)

            label_name_to_value = {"_background_": 0}
            for shape in sorted(data["shapes"], key=lambda x: x["label"]):
                label_name = shape["label"]
                if label_name in label_name_to_value:
                    label_value = label_name_to_value[label_name]
                else:
                    label_value = len(label_name_to_value)
                    label_name_to_value[label_name] = label_value
            lbl, _ = utils.shapes_to_label(
                img.shape, data["shapes"], label_name_to_value, isClose=args.isClose
            )

            label_names = [None] * (max(label_name_to_value.values()) + 1)
            for name, value in label_name_to_value.items():
                label_names[value] = name

            lbl_viz = imgviz.label2rgb(
                label=lbl, img=imgviz.asgray(img), label_names=label_names, loc="rb"
            )

            PIL.Image.fromarray(img).save(osp.join(out_dir, "img.png"))
            cv2.imwrite(osp.join(out_dir, "label.png"), lbl)
            # utils.lblsave(osp.join(out_dir, "label.png"), lbl)
            PIL.Image.fromarray(lbl_viz).save(osp.join(out_dir, "label_viz.png"))

            with open(osp.join(out_dir, "label_names.txt"), "w") as f:
                for lbl_name in label_names:
                    f.write(lbl_name + "\n")

    logger.info("Saved to: {}".format(out_dir))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='XiaoShun jsontodataset')
    parser.add_argument('-jf', '--json_file', default=None, type=str,
                        help='Path to the json files')
    parser.add_argument('-o', '--out', default=None, type=str,
                        help='Output Path for dataset')
    args = parser.parse_args()
    main(args)