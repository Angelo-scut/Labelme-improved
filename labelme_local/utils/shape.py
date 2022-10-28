import math
import uuid

import cv2
import numpy as np
import PIL.Image
import PIL.ImageDraw

from labelme_local.logger import logger


def polygons_to_mask(img_shape, polygons, shape_type=None):
    logger.warning(
        "The 'polygons_to_mask' function is deprecated, "
        "use 'shape_to_mask' instead."
    )
    return shape_to_mask(img_shape, points=polygons, shape_type=shape_type)

def ellipse_with_angle(im, x, y, major, minor, angle, color, thickness=3):
    # take an existing image and plot an ellipse centered at (x,y) with a
    # defined angle of rotation and major and minor axes.
    # center the image so that (x,y) is at the center of the ellipse
    # x -= int(major/2)
    # y -= int(major/2)

    ellipse_im = np.array(im)
    cv2.ellipse(ellipse_im, (int(x), int(y)), (int(major), int(minor)), angle, 0, 360, color, thickness)  # angle要求顺时针方向
    # maxaxis = int(max(major, minor) + 10)
    # create a new image in which to draw the ellipse
    # mask = np.zeros((int(2*minor+10), int(2*major+10)), dtype=np.uint8)
    # im_ellipse = PIL.Image.fromarray(mask)
    # im_ellipse = PIL.Image.new('RGB', (maxaxis, maxaxis), (255, 255, 255))
    # draw_ellipse = PIL.ImageDraw.Draw(im_ellipse)

    # draw the ellipse
    # ellipse_box = (5, 5, major+5, minor+5)
    # draw_ellipse.ellipse([5, 5, 2*major+5, 2*minor+5], outline=3)

    # rotate the new image
    # rotated = im_ellipse.rotate(angle)
    # rx, ry = rotated.size
    # rotated.save("testmask.png")
    # paste it into the existing image and return the result
    # im.paste(rotated, (x, y, x+rx, y+ry), mask=rotated)
    # im.paste(rotated, (int(x-rx/2), int(y-ry/2)))
    return ellipse_im

def is_livewire_close_enough(xy):
    spoint = xy[0]
    tpoint = xy[-1]
    if abs(spoint[0] - tpoint[0]) + abs(spoint[1] - tpoint[1]) < 10:
        return True
    else:
        return False

def shape_to_mask(
    img_shape, points, shape_type=None, line_width=10, point_size=5, isClose = False
):
    mask = np.zeros(img_shape[:2], dtype=np.uint8)
    mask = PIL.Image.fromarray(mask)
    draw = PIL.ImageDraw.Draw(mask)
    xy = [tuple(point) for point in points]
    ob_label = []
    if shape_type == "circle":
        assert len(xy) == 2, "Shape of shape_type=circle must have 2 points"
        (cx, cy), (px, py) = xy
        d = math.sqrt((cx - px) ** 2 + (cy - py) ** 2)
        draw.ellipse([cx - d, cy - d, cx + d, cy + d], outline=1, fill=1)
    elif shape_type == "rectangle":
        assert len(xy) == 2, "Shape of shape_type=rectangle must have 2 points"
        draw.rectangle(xy, outline=1, fill=1)
    elif shape_type == "line":
        assert len(xy) == 2, "Shape of shape_type=line must have 2 points"
        draw.line(xy=xy, fill=1, width=line_width)
    elif shape_type == "linestrip":
        draw.line(xy=xy, fill=1, width=line_width)
    elif shape_type == "point":
        assert len(xy) == 1, "Shape of shape_type=point must have 1 points"
        cx, cy = xy[0]
        r = point_size
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=1, fill=1)
    elif shape_type == "ellipse":
        assert len(xy) == 3, "Shape of shape_type=ellipse must have 3 points"
        (cx, cy), (ax, ay), (bx, by) = xy
        a = math.sqrt((cx - ax) ** 2 + (cy - ay) ** 2)
        b = math.sqrt((bx - ax) ** 2 + (by - ay) ** 2)
        angle = math.atan((ay - cy) /
                          (ax - cx + np.finfo(float).eps))
        # ob_label = [cx/img_shape[1], cy/img_shape[0], a/img_shape[1], b/img_shape[0], angle]
        # angle = angle * 180 / math.pi
        mask = ellipse_with_angle(mask, cx, cy, a, b, angle, (255,), thickness=-1)
        # if isClose:
        #     mask = ellipse_with_angle(mask, cx, cy, a, b, angle, (255,), thickness=-1)
        # else:
        #     mask = ellipse_with_angle(mask, cx, cy, a, b, angle, (255,))
    elif shape_type == "livewire":
        assert len(xy) > 2, "Livewire must have points more than 2"
        if is_livewire_close_enough(xy):
            draw.polygon(xy=xy, outline=1, fill=1)
        else:
            draw.line(xy=xy, fill=1, width=line_width)
        # if isClose:
        #     assert len(xy) > 2, "Polygon must have points more than 2"
        #     draw.polygon(xy=xy, outline=1, fill=1)
        # else:
        #     draw.line(xy=xy, fill=1, width=line_width)
    else:
        assert len(xy) > 2, "Polygon must have points more than 2"
        draw.polygon(xy=xy, outline=1, fill=1)
    mask = np.array(mask, dtype=bool)
    return mask


def shapes_to_label(img_shape, shapes, label_name_to_value, line_width=10, point_size=5, isClose=False):
    cls = np.zeros(img_shape[:2], dtype=np.int32)
    ins = np.zeros_like(cls)
    instances = []
    for shape in shapes:
        points = shape["points"]
        label = shape["label"]
        group_id = shape.get("group_id")
        if group_id is None:
            group_id = uuid.uuid1()
        shape_type = shape.get("shape_type", None)

        cls_name = label
        instance = (cls_name, group_id)

        if instance not in instances:
            instances.append(instance)
        ins_id = instances.index(instance) + 1
        cls_id = label_name_to_value[cls_name]

        mask = shape_to_mask(img_shape[:2], points, shape_type, line_width=line_width, point_size=point_size, isClose=isClose)
        cls[mask] = cls_id
        ins[mask] = ins_id

    return cls, ins


def labelme_shapes_to_label(img_shape, shapes, line_width=10, point_size=5, isClose=False):
    # logger.warn(
    #     "labelme_shapes_to_label is deprecated, so please use "
    #     "shapes_to_label."
    # )

    label_name_to_value = {"_background_": 0, "weldpool": 1, "keyhole": 2, "seam": 3}#{"_background_": 0, "weldpool": 3, "keyhole": 1, "seam": 2} #
    for shape in shapes:
        label_name = shape["label"]
        if label_name in label_name_to_value:
            label_value = label_name_to_value[label_name]
        else:
            label_value = len(label_name_to_value)
            label_name_to_value[label_name] = label_value

    lbl, _ = shapes_to_label(img_shape, shapes, label_name_to_value, line_width=line_width, point_size=point_size, isClose=isClose)
    return lbl, label_name_to_value


def bbox_for_eliipse(img_shape, shapes):  # 只支持一个椭圆的bbox，也就是目前仅支持用于焊接方面的检测
    label_name_to_value = {"_background_": 0}
    ob_label = []
    for shape in shapes:
        label_name = shape["label"]
        points = shape["points"]
        shape_type = shape.get("shape_type", None)
        if shape_type == "ellipse":
            xy = [tuple(point) for point in points]
            (cx, cy), (ax, ay), (bx, by) = xy
            a = math.sqrt((cx - ax) ** 2 + (cy - ay) ** 2)
            b = math.sqrt((bx - ax) ** 2 + (by - ay) ** 2)
            angle = math.atan2((ay - cy), (ax - cx))  # 范围是[-pi, pi]
            # angle = math.atan((ay - cy) /
            #                   (ax - cx + np.finfo(float).eps))  # 范围是[-pi/2, pi/2]
            ob_label = [1, cx/img_shape[1], cy/img_shape[0], a/img_shape[1], b/img_shape[0], angle]
    return ob_label

def masks_to_bboxes(masks):
    if masks.ndim != 3:
        raise ValueError(
            "masks.ndim must be 3, but it is {}".format(masks.ndim)
        )
    if masks.dtype != bool:
        raise ValueError(
            "masks.dtype must be bool type, but it is {}".format(masks.dtype)
        )
    bboxes = []
    for mask in masks:
        where = np.argwhere(mask)
        (y1, x1), (y2, x2) = where.min(0), where.max(0) + 1
        bboxes.append((y1, x1, y2, x2))
    bboxes = np.asarray(bboxes, dtype=np.float32)
    return bboxes
