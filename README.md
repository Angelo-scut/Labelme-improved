# Labelme-improved
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT) 

This repo is improved from labelme with python-qt version:
https://github.com/wkentaro/labelme

## Requirments
python==3.7.10
```bash
pip install -r requirements.txt
```
or for a local installation
```bash
pip install --user -r requirements.txt
```
or install labelme and cython by(recommended)
```bash
pip install labelme==4.5.7
pip install opencv-python==4.5.2.52
pip install cython
```
## Compile C++ wrapper
### Linux
```bash
cd labelme_local/cython
python setup.py build_ext --inplace
cd ..
```

## How To Use
```
 Run __main__.py in PyCharm or VS code
```
or
```
 python yourpath/labelmelocal/__main__.py
```
For those who have no environment, please download the exe file from:

link：https://pan.baidu.com/s/1RSzxIWLKEdBMIIEK4O7AVQ 

passward：1hl5
```
 labelme_local/dict/__main__/__main__.exe
```
## Main Features
- Added an ellipse annotation tool that can be tilted at any angle
- Added magnetic annotation tool (Just like PhotoShop)

### Ellipse Anotation Tool 
- The first point is the center of the ellipse, the distances from the second and third points to the center are the 
short and long axes, respectively, and the inclination is arctan(OA/OB)

### Magnetic Annotation Tool
Two modes: polygonal and piecewise curve.

06.24 update:Added the function of temporarily canceling the magnetic index by pressing the Q key, and pressing Q again 
can restore it
#### Polygonal Mode
- The last click point can be enclosed in a polygon with the first click point. The right mouse button can undo a section 
of the annotation.
#### Piecewise Curve mode
- Double-click anywhere to complete the annotation.The right mouse button can undo a section of the annotation.

## Json2Dataset
You can modify the jsontodataset.py for personal dataset style. Otherwise, the dataset style will be same as the orignal labelme.
```
python jsontodataset.py --json_file yourjosnpath --out youroutputpath
```


## Citation
If you find our repo useful for your research, please consider citing our paper:

```

```
