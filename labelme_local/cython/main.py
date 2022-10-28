# from C_fun import multiply_by_10
# from multiply_by_10 import multiply_by_10
# import numpy as np
# a = np.ones(5, dtype=np.double)
# list1 = [1, 0]
# list1 = np.array(list1)
# # print(multiply_by_10(a))
# a, sum, list2 = multiply_by_10(a, list1)
# print(a)
# print(sum)
# print(list2)
# b = np.ones(10, dtype=np.double)
# b = b[::2]  # b is not contiguous.
#
# print(multiply_by_10(b, list1))  # but our function still works as expected.

# from random import random
from time import time
# from fast_tanh import fast_tanh
#
# data = [random() for i in range(1000000)]    # 生成随机数据
#
# start_time = time()              # 计算并统计时间
# result = list(map(fast_tanh, data))
# end_time = time()
# print(end_time - start_time)     # 输出运行时间
import cv2
import numpy as np
# img = cv2.imread("lena.png", 0)
# def calcImgGrad(img):
#     x = cv2.Sobel(img, cv2.CV_32F, 1, 0)
#     y = cv2.Sobel(img, cv2.CV_32F, 0, 1)
#     mag, _ = cv2.cartToPolar(x, y)
#     _, max_val, _, _ = cv2.minMaxLoc(mag)
#     return 1.0 - mag / max_val
#
# def calcCanny(img):
#     param = 9
#     imgb = cv2.bilateralFilter(img, param, param * 2, param / 2.0)
#     vMean = cv2.mean(imgb)
#     vMedian = vMean[0]
#     sigma = 0.3
#     lower = max(0.0, (1.0 - sigma) * vMedian)
#     upper = min(255.0, (1.0 + sigma) * vMedian)
#     ret = cv2.Canny(imgb, lower, upper, apertureSize=3)
#     ret = ret.astype(np.float32) / 255
#
#     return ret
# def calcLiveWireCostFcn(img):
#     imgG = calcImgGrad(img)
#     imgE = calcCanny(img)
#     pG = 0.8
#     pE = 0.2
#     return pG*imgG + pE*imgE
# start_time = time()              # 计算并统计时间
# imgF = calcLiveWireCostFcn(img)
# from mylivewire import button_even
# from mylivewire import move_event
# cPoint, mPoint = [100, 200], [150, 180]
# cPoint, mPoint = np.array(cPoint), np.array(mPoint)
# path = [100, 200]
# path = np.array(path)
# # print(img[196:204, 96:104])
# imgF = imgF.astype(np.double)
# cPoint, iPX, iPY = button_even(imgF, cPoint)
# num_point, mPoint, path = move_event(imgF, cPoint, mPoint, iPX, iPY, path)
# # num_point, cPoint, mPoint, path = mylivewire(imgF, cPoint, mPoint, path)
# end_time = time()
# num_point = int(num_point / 2)
# for i in range(num_point-1):
#     cv2.line(img, pt1=(path[2*i], path[2*i+1]), pt2=(path[2*(i+1)], path[2*(i+1)+1]), color=255)
# print(end_time - start_time)     # 输出运行时间
# print(num_point)
# print(cPoint)
# print(mPoint)
# print(path)
# cv2.imshow("mag", img)
# cv2.waitKey()

from lwclass import lwclass


lw = lwclass("back10166.png")
# lw.img = cv2.resize(lw.img, (300, 400))
# lw.imgF = lw.calcLiveWireCostFcn(cv2.cvtColor(lw.img, cv2.COLOR_RGB2GRAY))
# lw.imgF = lw.imgF.astype(np.double)
img = cv2.imread("back10166.png", 0)
def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        lw.cPoint[0], lw.cPoint[1] = x, y
        lw.cPointx_list.append(x)
        lw.cPointy_list.append(y)
        if lw.isPath:
            lw.path_allx = np.concatenate((lw.path_allx, lw.pathx_arr), axis=0)
            lw.path_ally = np.concatenate((lw.path_ally, lw.pathy_arr), axis=0)
            lw.num_list.append(lw.num_point)
        lw.button()
        # tempx = lw.iPX.reshape(lw.imgF.shape[0], lw.imgF.shape[1])
        # tempy = lw.iPY.reshape(lw.imgF.shape[0], lw.imgF.shape[1])
        # temp = np.sqrt(np.power(tempx, 2) + np.power(tempy, 2))
        # # temp = (temp - temp.min) / (temp.max - temp.min)
        # cv2.imshow("iP", temp)
        # cv2.waitKey()
    elif event == cv2.EVENT_RBUTTONDOWN:
        if lw.isPath:
            if len(lw.num_list) >= 1:
                num = lw.num_list[-1]
                del lw.num_list[-1]
                lw.cPoint[0], lw.cPoint[1] = lw.path_allx[lw.path_allx.size-num], lw.path_ally[lw.path_allx.size-num]
                lw.path_allx = lw.path_allx[:(lw.path_allx.size-num)]
                lw.path_ally = lw.path_ally[:(lw.path_ally.size-num)]
                lw.button()
    elif event == cv2.EVENT_LBUTTONDBLCLK:
        if lw.isPath:
            lw.isPath = False
            lw.path_allx = np.concatenate((lw.path_allx, lw.pathx_arr), axis=0)
            lw.path_ally = np.concatenate((lw.path_ally, lw.pathy_arr), axis=0)
            lw.path_allx = np.concatenate((lw.path_allx, np.array([lw.path_allx[0]])), axis=0)
            lw.path_ally = np.concatenate((lw.path_ally, np.array([lw.path_ally[0]])), axis=0)
            lw.num_list.append(lw.num_point)
            imgOUT = lw.img.copy()
            if lw.path_allx.size != 0:
                for i in range(lw.path_allx.size - 1):
                    cv2.line(imgOUT, pt1=(lw.path_allx[i], lw.path_ally[i]),
                             pt2=(lw.path_allx[i + 1], lw.path_ally[i + 1]), color=(0, 255, 0))
            cv2.imshow('img', imgOUT)
    else:
        if lw.isPath:
            lw.mPoint[0], lw.mPoint[1] = x, y
            lw.move()
            imgOUT = lw.img.copy()
            if lw.path_allx.size != 0:
                for i in range(lw.path_allx.size-1):
                    cv2.line(imgOUT, pt1=(lw.path_allx[i], lw.path_ally[i]),
                             pt2=(lw.path_allx[i + 1], lw.path_ally[i + 1]), color=(0, 255, 0))
            for i in range(lw.num_point-1):
                cv2.line(imgOUT, pt1=(lw.pathx_arr[i], lw.pathy_arr[i]),
                         pt2=(lw.pathx_arr[i+1], lw.pathy_arr[i+1]), color=(255, 0, 0))
            cv2.imshow('img', imgOUT)


def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        #画圆函数，参数分别表示原图、坐标、半径、颜色、线宽(若为-1表示填充)
        cv2.circle(img, (x, y), 20, 255, -1)

if __name__ == '__main__':
    cv2.namedWindow('img')
    cv2.imshow('img', lw.img)
    # 新建鼠标事件
    cv2.setMouseCallback('img', on_mouse)
    while (1):
        # cv2.imshow('img', lw.img)
        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()