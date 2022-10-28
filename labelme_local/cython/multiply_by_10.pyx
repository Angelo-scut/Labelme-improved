cdef extern from "C_func_file.cpp":
    # C is include here so that it doesn't need to be compiled externally
    pass

cdef extern from "C_func_file.h":
    int multiply_by_10_in_C(double[:,:], unsigned int, unsigned int,int *)

import numpy as np
import cv2

def multiply_by_10(arr, point): # 'arr' is a one-dimensional numpy array

    if not arr.flags['C_CONTIGUOUS']:
        arr = np.ascontiguousarray(arr) # Makes a contiguous copy of the numpy array.

    cdef double[:1] arr_memview = arr
    cdef int[::1] point_memivew = point
    sum = multiply_by_10_in_C(&arr_memview, arr_memview.shape[0], arr_memview.shape[1], &point_memivew[0])

    return arr, sum, point

def calcImgGrad(img):
    x = cv2.Sobel(img, cv2.CV_32F, 1, 0)
    y = cv2.Sobel(img, cv2.CV_32F, 0, 1)
    mag, _ = cv2.cartToPolar(x, y)
    cdef double max_val
    _, max_val, _, _ = cv2.minMaxLoc(mag)
    return 1.0 - mag / max_val

def calcCanny(img):
    cdef int param = 9
    imgb = cv2.bilateralFilter(img, param, param * 2, param / 2.0)
    vMean = cv2.mean(imgb)
    cdef double vMedian = vMean[0]
    cdef double sigma = 0.3
    cdef double lower = max(0.0, (1.0 - sigma) * vMedian)
    cdef double upper = min(255.0, (1.0 + sigma) * vMedian)
    ret = cv2.Canny(imgb, lower, upper, apertureSize=3)
    ret = ret.astype(np.float32) / 255

    return ret

def calcLiveWireCostFcn(img):
    imgG = calcImgGrad(img)
    imgE = calcCanny(img)
    cdef float pG = 0.8
    cdef float pE = 0.2
    return pG*imgG + pE*imgE

def load_Image(img):
    imgF = calcLiveWireCostFcn(img)
    imgF = imgF.reshape(imgF.shape[0]*imgF.shape[1])
    if not imgF.flags['C_CONTIGUOUS']:
       imgF = np.ascontiguousarray(imgF)  # Makes a contiguous copy of the numpy array.
    cdef float[::1] arr_memview = imgF