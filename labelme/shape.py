import copy
import math

from qtpy import QtCore
from qtpy import QtGui

import numpy as np

import labelme.utils
# from labelme.cython.lwclass import lwclass
from lwclass import lwclass
# TODO(unknown):
# - [opt] Store paths instead of creating new ones at each paint.


DEFAULT_LINE_COLOR = QtGui.QColor(0, 255, 0, 128)  # bf hovering
DEFAULT_FILL_COLOR = QtGui.QColor(0, 255, 0, 128)  # hovering
DEFAULT_SELECT_LINE_COLOR = QtGui.QColor(255, 255, 255)  # selected
DEFAULT_SELECT_FILL_COLOR = QtGui.QColor(0, 255, 0, 155)  # selected
DEFAULT_VERTEX_FILL_COLOR = QtGui.QColor(0, 255, 0, 255)  # hovering
DEFAULT_HVERTEX_FILL_COLOR = QtGui.QColor(255, 255, 255, 255)  # hovering


class Shape(object):

    P_SQUARE, P_ROUND = 0, 1

    MOVE_VERTEX, NEAR_VERTEX = 0, 1

    # The following class variables influence the drawing of all shape objects.
    line_color = DEFAULT_LINE_COLOR
    fill_color = DEFAULT_FILL_COLOR
    select_line_color = DEFAULT_SELECT_LINE_COLOR
    select_fill_color = DEFAULT_SELECT_FILL_COLOR
    vertex_fill_color = DEFAULT_VERTEX_FILL_COLOR
    hvertex_fill_color = DEFAULT_HVERTEX_FILL_COLOR
    point_type = P_ROUND
    point_size = 8
    scale = 1.0  # 这里声明的变量是所有具体对象共有的，所以当使用Shape.scale = 2.0时，所有的Shape类对象的scale都是2.0
    offset = QtCore.QPoint()

    def __init__(
        self,
        path=None,
        label=None,
        line_color=None,
        shape_type=None,
        flags=None,
        group_id=None,
    ):
        self.label = label
        self.group_id = group_id
        self.points = []
        self.fill = False
        self.selected = False
        self.shape_type = shape_type
        self.flags = flags
        self.other_data = {}

        self._highlightIndex = None
        self._highlightMode = self.NEAR_VERTEX
        self._highlightSettings = {
            self.NEAR_VERTEX: (4, self.P_ROUND),
            self.MOVE_VERTEX: (1.5, self.P_SQUARE),
        }

        self._closed = False

        if line_color is not None:
            # Override the class line_color attribute
            # with an object attribute. Currently this
            # is used for drawing the pending line a different color.
            self.line_color = line_color

        self.shape_type = shape_type

        if path is not None:
            self.lw = lwclass(path)

    @property
    def shape_type(self):
        return self._shape_type

    @shape_type.setter
    def shape_type(self, value):
        if value is None:
            value = "polygon"
        if value not in [
            "polygon",
            "rectangle",
            "point",
            "line",
            "circle",
            "ellipse",
            "livewire",
            "linestrip",
        ]:
            raise ValueError("Unexpected shape_type: {}".format(value))
        self._shape_type = value

    def close(self):
        self._closed = True

    def addPoint(self, point):
        if self.points and point == self.points[0]:
            self.close()
        else:
            self.points.append(point)

    def canAddPoint(self):
        return self.shape_type in ["polygon", "linestrip"]

    def popPoint(self):
        if self.points:
            return self.points.pop()
        return None

    def insertPoint(self, i, point):
        self.points.insert(i, point)

    def removePoint(self, i):
        self.points.pop(i)

    def isClosed(self):
        return self._closed

    def setOpen(self):
        self._closed = False

    def getRectFromLine(self, pt1, pt2):
        x1, y1 = pt1.x(), pt1.y()
        x2, y2 = pt2.x(), pt2.y()
        return QtCore.QRectF(x1, y1, x2 - x1, y2 - y1)  # 起点、宽、长

    def paint(self, painter):  # 这里应该是绘制
        if self.points:
            color = (
                self.select_line_color if self.selected else self.line_color
            )
            pen = QtGui.QPen(color)
            # Try using integer sizes for smoother drawing(?)
            pen.setWidth(max(1, int(round(2.0 / self.scale))))
            painter.setPen(pen)

            line_path = QtGui.QPainterPath()
            vrtx_path = QtGui.QPainterPath()

            if self.shape_type == "rectangle":
                assert len(self.points) in [1, 2]
                if len(self.points) == 2:
                    rectangle = self.getRectFromLine(*self.points)
                    line_path.addRect(rectangle)
                for i in range(len(self.points)):
                    self.drawVertex(vrtx_path, i)
            elif self.shape_type == "circle":  # 画圆部分
                assert len(self.points) in [1, 2]
                if len(self.points) == 2:
                    rectangle = self.getCircleRectFromLine(self.points)
                    line_path.addEllipse(rectangle)
                for i in range(len(self.points)):
                    self.drawVertex(vrtx_path, i)
            elif self.shape_type == "ellipse":  # 画椭圆也是这样，暂时的
                assert len(self.points) in [1, 2, 3]
                if len(self.points) == 2:
                    line_path.moveTo(self.points[0])
                    line_path.lineTo(self.points[1])
                elif len(self.points) == 3:
                    # painter.drawEllipse(self.points[0],
                    #                     math.sqrt(math.pow(self.points[0].x()-self.points[1].x(), 2) +
                    #                               math.pow(self.points[0].y()-self.points[1].y(), 2)),
                    #                     math.sqrt(math.pow(self.points[2].x() - self.points[1].x(), 2) +
                    #                               math.pow(self.points[2].y() - self.points[1].y(), 2)))
                    # rectangle = self.getCircleRectFromLine(self.points[0:2])
                    # line_path.addEllipse(rectangle)
                    # painter.drawEllipse(QtCore.QPointF(0, 0),
                    #                     math.sqrt(math.pow(self.points[0].x() - self.points[1].x(), 2) +
                    #                               math.pow(self.points[0].y() - self.points[1].y(), 2)),
                    #                     math.sqrt(math.pow(self.points[2].x() - self.points[1].x(), 2) +
                    #                               math.pow(self.points[2].y() - self.points[1].y(), 2))
                    #                     )
                    # painter.resetTransform()
                    painter.translate(self.points[0])
                    angle = math.atan((self.points[1].y()-self.points[0].y()) /
                                      (self.points[1].x()-self.points[0].x()+np.finfo(float).eps))
                    angle = angle * 180 / math.pi
                    painter.rotate(angle)
                    # line_path.addEllipse(QtCore.QPointF(0, 0),
                    #                      math.sqrt(math.pow(self.points[0].x() - self.points[1].x(), 2) +
                    #                                math.pow(self.points[0].y()-self.points[1].y(), 2)),
                    #                      math.sqrt(math.pow(self.points[2].x() - self.points[1].x(), 2) +
                    #                                math.pow(self.points[2].y() - self.points[1].y(), 2)))
                    painter.drawEllipse(QtCore.QPointF(0, 0),
                                        math.sqrt(math.pow(self.points[0].x() - self.points[1].x(), 2) +
                                                  math.pow(self.points[0].y() - self.points[1].y(), 2)),
                                        math.sqrt(math.pow(self.points[2].x() - self.points[1].x(), 2) +
                                                  math.pow(self.points[2].y() - self.points[1].y(), 2))
                                        )
                    painter.resetTransform()
                    painter.scale(self.scale, self.scale)
                    painter.translate(self.offset)
                    # painter.rotate(angle)
                    # painter.translate(QtCore.QPointF(-self.points[0].x(), -self.points[0].y()))
                for i in range(len(self.points)):  # 把关键点绘制出来
                    self.drawVertex(vrtx_path, i)
            elif self.shape_type == "livewire":  # 画椭圆也是这样，暂时的
                line_path.moveTo(self.points[0])
                for i, p in enumerate(self.points): # 从最近点开始绘制到p点的直线
                    line_path.lineTo(p)
                # line_path.moveTo(self.points[0])
                # # Uncommenting the following line will draw 2 paths
                # # for the 1st vertex, and make it non-filled, which
                # # may be desirable.
                # # self.drawVertex(vrtx_path, 0)
                #
                # for i, p in enumerate(self.points):
                #     line_path.lineTo(p)
                #     self.drawVertex(vrtx_path, i)
                # if self.isClosed():
                #     line_path.lineTo(self.points[0])
                # for i in range(len(self.points)):  # 把关键点绘制出来
                #     self.drawVertex(vrtx_path, i)
            elif self.shape_type == "linestrip":
                line_path.moveTo(self.points[0])
                for i, p in enumerate(self.points):
                    line_path.lineTo(p)
                    self.drawVertex(vrtx_path, i)
            else:
                line_path.moveTo(self.points[0])
                # Uncommenting the following line will draw 2 paths
                # for the 1st vertex, and make it non-filled, which
                # may be desirable.
                # self.drawVertex(vrtx_path, 0)

                for i, p in enumerate(self.points):
                    line_path.lineTo(p)
                    self.drawVertex(vrtx_path, i)
                if self.isClosed():
                    line_path.lineTo(self.points[0])
            painter.drawPath(line_path)
            if self.shape_type != "livewire":
                painter.drawPath(vrtx_path)
                painter.fillPath(vrtx_path, self._vertex_fill_color)
            if self.fill:
                color = (
                    self.select_fill_color
                    if self.selected
                    else self.fill_color
                )
                painter.fillPath(line_path, color)

    def drawVertex(self, path, i):  # 绘制顶点（vertex为顶点）
        d = self.point_size / self.scale
        shape = self.point_type
        point = self.points[i]
        if i == self._highlightIndex:
            size, shape = self._highlightSettings[self._highlightMode]
            d *= size
        if self._highlightIndex is not None:
            self._vertex_fill_color = self.hvertex_fill_color
        else:
            self._vertex_fill_color = self.vertex_fill_color
        if shape == self.P_SQUARE:
            path.addRect(point.x() - d / 2, point.y() - d / 2, d, d)
        elif shape == self.P_ROUND:
            path.addEllipse(point, d / 2.0, d / 2.0)
        else:
            assert False, "unsupported vertex shape"

    def nearestVertex(self, point, epsilon):
        min_distance = float("inf")
        min_i = None
        for i, p in enumerate(self.points):
            dist = labelme.utils.distance(p - point)
            if dist <= epsilon and dist < min_distance:
                min_distance = dist
                min_i = i
        return min_i

    def nearestEdge(self, point, epsilon):
        min_distance = float("inf")
        post_i = None
        for i in range(len(self.points)):
            line = [self.points[i - 1], self.points[i]]
            dist = labelme.utils.distancetoline(point, line)
            if dist <= epsilon and dist < min_distance:
                min_distance = dist
                post_i = i
        return post_i

    def containsPoint(self, point):
        return self.makePath().contains(point)

    def getCircleRectFromLine(self, line):  # 这是画圆操作，line即是point
        """Computes parameters to draw with `QPainterPath::addEllipse`"""
        if len(line) != 2:
            return None
        (c, point) = line
        r = line[0] - line[1]  # 求取半径sqrt((x1-x2)2,(y1-y2)2)
        d = math.sqrt(math.pow(r.x(), 2) + math.pow(r.y(), 2))  # 下面的x和y表示左上角的坐标
        rectangle = QtCore.QRectF(c.x() - d, c.y() - d, 2 * d, 2 * d)  #QRectF(qreal x, qreal y, qreal width, qreal height)
        return rectangle

    def getEllipseRectFromLine(self, line):  # 这是画椭圆操作，line即是point
        """Computes parameters to draw with `QPainterPath::addEllipse`"""
        if len(line) != 2:  # 椭圆不能用RectF因为还要考虑旋转角度
            return None
        (c, point) = line
        r = line[0] - line[1]  # 求取半径sqrt((x1-x2)2,(y1-y2)2)
        d = math.sqrt(math.pow(r.x(), 2) + math.pow(r.y(), 2))  # 下面的x和y表示左上角的坐标
        rectangle = QtCore.QRectF(c.x() - d, c.y() - d, 2 * d, 2 * d)  #QRectF(qreal x, qreal y, qreal width, qreal height)
        return rectangle

    def getParabolaRectFromLine(self, line):  # 这是画抛物线操作，line即是point
        """Computes parameters to draw with `QPainterPath::addEllipse`"""
        if len(line) != 2:
            return None
        (c, point) = line
        r = line[0] - line[1]  # 求取半径sqrt((x1-x2)2,(y1-y2)2)
        d = math.sqrt(math.pow(r.x(), 2) + math.pow(r.y(), 2))  # 下面的x和y表示左上角的坐标
        rectangle = QtCore.QRectF(c.x() - d, c.y() - d, 2 * d, 2 * d)  #QRectF(qreal x, qreal y, qreal width, qreal height)
        return rectangle

    def makePath(self):
        if self.shape_type == "rectangle":
            path = QtGui.QPainterPath()
            if len(self.points) == 2:
                rectangle = self.getRectFromLine(*self.points)
                path.addRect(rectangle)
        elif self.shape_type == "circle":
            path = QtGui.QPainterPath()
            if len(self.points) == 2:
                rectangle = self.getCircleRectFromLine(self.points)
                path.addEllipse(rectangle)
        else:
            path = QtGui.QPainterPath(self.points[0])
            for p in self.points[1:]:
                path.lineTo(p)
        return path

    def boundingRect(self):
        return self.makePath().boundingRect()

    def moveBy(self, offset):
        self.points = [p + offset for p in self.points]

    def moveVertexBy(self, i, offset):
        self.points[i] = self.points[i] + offset

    def highlightVertex(self, i, action):
        self._highlightIndex = i
        self._highlightMode = action

    def highlightClear(self):
        self._highlightIndex = None

    def copy(self):
        return copy.deepcopy(self)

    def __len__(self):
        return len(self.points)

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        self.points[key] = value
