# Labelme-improved
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT) 

This repo is improved from labelme with python-qt version:
https://github.com/wkentaro/labelme

## Requirments
```bash
pip install -r requirements.txt
```
or for a local installation
```bash
pip install --user -r requirements.txt
```
or install labelme and cython by
```bash
pip install labelme==4.5.7
pip install opencv-python==4.5.2.52
pip install cython
```

## How To Use
```
 Run __main__.py in PyCharm or VS code
```
or
```
 python yourpath/labelmelocal/__main__.py
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
You need to modify the 'label_name_to_value' in shape.py and the path in jsontodataset.py
```
python jsontodataset.py --json_file yourjosnpath --out youroutputpath
```


## Citation
If you find our repo useful for your research, please consider citing our paper:

```

```
