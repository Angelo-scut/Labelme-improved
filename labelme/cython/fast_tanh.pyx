# distutils: language = c++
# cython: language_level = 3
import pyximport
pyximport.install()

cdef extern from "mytanh.cpp":
    double mytanh(double x)

def fast_tanh(double x):
    return mytanh(x)