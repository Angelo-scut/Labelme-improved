import cv2
import numpy as np
from mylivewire import button_even
from mylivewire import move_event


class lwclass:
    def __init__(self, path):
        self.img = cv2.imread(path, 1)
        self.imgF = self.calcLiveWireCostFcn(cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY))
        self.imgF = self.imgF.astype(np.double)
        if self.imgF.shape[0] > self.imgF.shape[1]:
            self.imgFR = cv2.rotate(self.imgF, cv2.ROTATE_90_CLOCKWISE)
        self.cPoint = np.array([0, 0], dtype=np.int32)
        self.mPoint = np.array([0, 0], dtype=np.int32)
        self.iPX = np.zeros(self.imgF.shape, np.int32)
        self.iPY = np.zeros(self.imgF.shape, np.int32)
        self.pathx_arr = np.zeros(10000, np.int32)
        self.pathy_arr = np.zeros(10000, np.int32)
        self.isPath = False
        self.path_allx = np.array([], dtype=np.int32)
        self.path_ally = np.array([], dtype=np.int32)
        self.num_point = 0
        self.num_list = []
        self.cPointx_list = []
        self.cPointy_list = []

    def initiate(self, path):
        self.img = cv2.imread(path, 1)
        self.imgF = self.calcLiveWireCostFcn(cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY))
        self.imgF = self.imgF.astype(np.double)
        if self.imgF.shape[0] > self.imgF.shape[1]:
            self.imgFR = cv2.rotate(self.imgF, cv2.ROTATE_90_CLOCKWISE)
        self.cPoint = np.array([0, 0], dtype=np.int32)
        self.mPoint = np.array([0, 0], dtype=np.int32)
        self.iPX = np.zeros(self.imgF.shape, np.int32)
        self.iPY = np.zeros(self.imgF.shape, np.int32)
        self.pathx_arr = np.zeros(10000, np.int32)
        self.pathy_arr = np.zeros(10000, np.int32)
        self.isPath = False
        self.path_allx = np.array([], dtype=np.int32)
        self.path_ally = np.array([], dtype=np.int32)
        self.num_point = 0
        self.num_list = []
        self.cPointx_list = []
        self.cPointy_list = []

    def calcImgGrad(self, img):
        x = cv2.Sobel(img, cv2.CV_32F, 1, 0)
        y = cv2.Sobel(img, cv2.CV_32F, 0, 1)
        mag, _ = cv2.cartToPolar(x, y)
        _, max_val, _, _ = cv2.minMaxLoc(mag)
        return 1.0 - mag / max_val

    def calcCanny(self, img):
        param = 9
        imgb = cv2.bilateralFilter(img, param, param * 2, param / 2.0)
        vMean = cv2.mean(imgb)
        vMedian = vMean[0]
        sigma = 0.3
        lower = max(0.0, (1.0 - sigma) * vMedian)
        upper = min(255.0, (1.0 + sigma) * vMedian)
        ret = cv2.Canny(imgb, lower, upper, apertureSize=3)
        ret = ret.astype(np.float32) / 255

        return ret

    def calcLiveWireCostFcn(self, img):
        imgG = self.calcImgGrad(img)
        imgE = self.calcCanny(img)
        pG = 0.8
        pE = 0.2
        return pG * imgG + pE * imgE

    def move(self):
        if self.imgF.shape[0] > self.imgF.shape[1]:
            temp = self.mPoint[1]
            self.mPoint[1] = self.mPoint[0]
            self.mPoint[0] = self.imgF.shape[0] - temp
            self.num_point, self.mPoint, self.pathx_arr, self.pathy_arr = move_event(self.imgFR, self.cPoint,
                                                                                     self.mPoint,
                                                                                     self.iPX, self.iPY, self.pathx_arr,
                                                                                     self.pathy_arr)
            self.pathx_arr = np.concatenate((np.array([self.cPoint[0]]), self.pathx_arr[:self.num_point]), axis=0)
            self.pathy_arr = np.concatenate((np.array([self.cPoint[1]]), self.pathy_arr[:self.num_point]), axis=0)
            self.num_point += 1
        else:
            self.num_point, self.mPoint, self.pathx_arr, self.pathy_arr = move_event(self.imgF, self.cPoint,
                                                                                     self.mPoint,
                                                                                     self.iPX, self.iPY, self.pathx_arr,
                                                                                     self.pathy_arr)
            self.pathx_arr = np.concatenate((np.array([self.cPoint[0]]), self.pathx_arr[:self.num_point]), axis=0)
            self.pathy_arr = np.concatenate((np.array([self.cPoint[1]]), self.pathy_arr[:self.num_point]), axis=0)
            self.num_point += 1

    def button(self):
        if self.imgF.shape[0] > self.imgF.shape[1]:
            temp = self.cPoint[1]
            self.cPoint[1] = self.cPoint[0]
            self.cPoint[0] = self.imgF.shape[0] - temp
            self.cPoint, self.iPX, self.iPY = button_even(self.imgFR, self.cPoint)
            self.isPath = True
        else:
            self.cPoint, self.iPX, self.iPY = button_even(self.imgF, self.cPoint)
            self.isPath = True

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            self.cPoint[0], self.cPoint[1] = x, y
            self.button()
            self.isPath = True
        else:
            if self.isPath:
                self.mPoint[0], self.mPoint[1] = x, y
                self.button()