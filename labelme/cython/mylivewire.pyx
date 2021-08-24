cdef extern from "livewire.cpp":
    # C is include here so that it doesn't need to be compiled externally
    pass

cdef extern from "livewire.h":
    void calcLWP(int *, double *, unsigned int , unsigned int )
    void calcIdealAnchor(double *, unsigned int , unsigned int , int *, int)
    void calcLiveWireP(double *, unsigned int , unsigned int , int *, int *, int *, int *,double , int );
    int calcLWPath(int *, double *, unsigned int, unsigned int, int *, int *, int *, int *, int *);

import numpy as np
# import cv2
# cdef class mylivewire:
def button_even(imgF, cPoint):
    img = imgF.reshape(imgF.shape[0] * imgF.shape[1])
    if not img.flags['C_CONTIGUOUS']:
        img = np.ascontiguousarray(img)  # Makes a contiguous copy of the numpy array.
    cdef int[::1] cPoint_memivew = cPoint
    cdef double[::1] img_memview = img
    iPX = np.zeros(imgF.shape, np.int32)
    iPY = np.zeros(imgF.shape, np.int32)
    lE = np.zeros(imgF.shape, np.int32)
    iPX = iPX.reshape(imgF.shape[0] * imgF.shape[1])
    iPY = iPY.reshape(imgF.shape[0] * imgF.shape[1])
    lE = lE.reshape(imgF.shape[0] * imgF.shape[1])
    if not iPX.flags['C_CONTIGUOUS']:
        iPX = np.ascontiguousarray(iPX)
    if not iPY.flags['C_CONTIGUOUS']:
        iPY = np.ascontiguousarray(iPY)
    if not lE.flags['C_CONTIGUOUS']:
        lE = np.ascontiguousarray(lE)
    cdef int[::1] iPX_memivew = iPX
    cdef int[::1] iPY_memivew = iPY
    cdef int[::1] lE_memivew = lE
    cdef double dRadius = 120
    cdef int max_lenght = 10000
    calcLWP(&cPoint_memivew[0], &img_memview[0], imgF.shape[0], imgF.shape[1])
    calcLiveWireP(&img_memview[0], imgF.shape[0], imgF.shape[1], &cPoint_memivew[0], &iPX_memivew[0],
                  &iPY_memivew[0],&lE_memivew[0], dRadius, max_lenght)
    return cPoint, iPX, iPY
def move_event(imgF, cPoint, mPoint, iPX, iPY, pathx, pathy):
    img = imgF.reshape(imgF.shape[0] * imgF.shape[1])
    if not img.flags['C_CONTIGUOUS']:
        img = np.ascontiguousarray(img) # Makes a contiguous copy of the numpy array.
    pathx = np.zeros(10000, np.int32)
    pathy = np.zeros(10000, np.int32)
    if not iPX.flags['C_CONTIGUOUS']:
        iPX = np.ascontiguousarray(iPX)
    if not iPY.flags['C_CONTIGUOUS']:
        iPY = np.ascontiguousarray(iPY)
    if not pathx.flags['C_CONTIGUOUS']:
        pathx = np.ascontiguousarray(pathx)
    if not pathy.flags['C_CONTIGUOUS']:
        pathy = np.ascontiguousarray(pathy)
    cdef int[::1] iPX_memivew = iPX
    cdef int[::1] iPY_memivew = iPY
    cdef int[::1] pathx_memivew = pathx
    cdef int[::1] pathy_memivew = pathy
    cdef double[::1] img_memview = img
    cdef int[::1] cPoint_memivew = cPoint
    cdef int[::1] mPoint_memivew = mPoint
    cdef double dRadius = 120
    cdef int max_lenght = 10000
    cdef int num_point = 0
    calcLWP(&mPoint_memivew[0], &img_memview[0], imgF.shape[0], imgF.shape[1])
    num_point = calcLWPath(&mPoint_memivew[0], &img_memview[0], imgF.shape[0], imgF.shape[1], &iPX_memivew[0],
                           &iPY_memivew[0],&pathx_memivew[0], &pathy_memivew[0], &cPoint_memivew[0])

    return num_point, mPoint, pathx, pathy
# def mylivewire(imgF, cPoint, mPoint, path): # 'arr' is a one-dimensional numpy array
#     img = imgF.reshape(imgF.shape[0] * imgF.shape[1])
#     iPX = np.zeros(imgF.shape, np.int32)
#     iPY = np.zeros(imgF.shape, np.int32)
#     lE = np.zeros(imgF.shape, np.int32)
#     if not img.flags['C_CONTIGUOUS']:
#         img = np.ascontiguousarray(img) # Makes a contiguous copy of the numpy array.
#     iPX = iPX.reshape(imgF.shape[0] * imgF.shape[1])
#     iPY = iPY.reshape(imgF.shape[0] * imgF.shape[1])
#     lE = lE.reshape(imgF.shape[0] * imgF.shape[1])
#     path = np.zeros(2000, np.int32)
#     if not iPX.flags['C_CONTIGUOUS']:
#         iPX = np.ascontiguousarray(iPX)
#     if not iPY.flags['C_CONTIGUOUS']:
#         iPY = np.ascontiguousarray(iPY)
#     if not lE.flags['C_CONTIGUOUS']:
#         lE = np.ascontiguousarray(lE)
#     if not path.flags['C_CONTIGUOUS']:
#         path = np.ascontiguousarray(path)
#     cdef int[::1] iPX_memivew = iPX
#     cdef int[::1] iPY_memivew = iPY
#     cdef int[::1] lE_memivew = lE
#     cdef int[::1] path_memivew = path
#     cdef double[::1] img_memview = img
#     cdef int[::1] cPoint_memivew = cPoint
#     cdef int[::1] mPoint_memivew = mPoint
#     cdef double dRadius = 120
#     cdef int max_lenght = 10000
#     cdef int num_point = 0
#     calcLWP(&cPoint_memivew[0], &img_memview[0], imgF.shape[0], imgF.shape[1])
#     calcLiveWireP(&img_memview[0], imgF.shape[0], imgF.shape[1], &cPoint_memivew[0], &iPX_memivew[0], &iPY_memivew[0],
#                   &lE_memivew[0], dRadius, max_lenght)
#     num_point = calcLWPath(&mPoint_memivew[0], &img_memview[0], imgF.shape[0], imgF.shape[1], &iPX_memivew[0],
#                            &iPY_memivew[0],&path_memivew[0], &cPoint_memivew[0])
#
#     return num_point, cPoint, mPoint, path