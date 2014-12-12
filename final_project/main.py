from sklearn import svm
import matplotlib.pyplot as plt
from sys import argv
import time
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from operator import add

import stl_to_ptcloud as stp
import components as comp
import perimeter as perim

# PRINTER SETTINGS
filament_width = 1.75 # in mm
extruder_width = 0.35 # in mm
ext_fil_ratio = filament_width / extruder_width
layer_height = 0.35 # in mm
offset = [30., 30.] # in mm
scale = .75
resolution_rescale = 1

# SOFTWARE SETTINGS
NU = 0.1
GAMMA = 0.1
KERNEL = 'rbf'

if __name__ == '__main__':
    # step 1: get the point cloud, find its bounding box all dimensions
    f_name = argv[1]
    if f_name[-4:].lower() == '.stl':
        pts = stp.get_pts(f_name)
    elif f_name[-4:].lower() == '.ptc':
        pts = []
        with open(f_name) as f:
            fr = f.readline()
            while fr:
                pts.append(map(float, fr.split(',')))
                fr = f.readline()
    else:
        print 'Error, unrecognized file format, please use .stl or .ptc'
        quit()
    x_vals = [x[0] for x in pts]
    y_vals = [x[1] for x in pts]
    z_vals = [x[2] for x in pts]
    x_axis = [x * float(extruder_width / resolution_rescale) for x in range(int(min(x_vals)/extruder_width*resolution_rescale), int(max(x_vals)/extruder_width*resolution_rescale)+1)]
    y_axis = [y * float(extruder_width / resolution_rescale) for y in range(int(min(y_vals)/extruder_width*resolution_rescale), int(max(y_vals)/extruder_width*resolution_rescale)+1)]
    xy_grid = [[x,y] for x in x_axis for y in y_axis]
    z_axis = [z * float(layer_height) for z in range(int(min(z_vals)/layer_height), int(max(z_vals)/layer_height))]

    # step 2: construct an SVM around the point cloud
    clf = svm.OneClassSVM(nu=NU, kernel=KERNEL, gamma=GAMMA)
    clf.fit(pts)

    # step 3: write g-code
    out_name = f_name[:-4] + '.gcode'
    open(out_name, 'w').close()
    comp.write_prelude(out_name)
    e = 1.0
    for z in z_axis:
        with open(out_name, 'a') as out:
            out.write('G1 Z%.5f\n' % z)
        M = clf.decision_function([x + [z] for x in xy_grid])
        M = M.reshape([len(x_axis), len(y_axis)])
        M = [[M[i][j] > 0 for i in range(len(M))] for j in range(len(M[0]))]
        outline = perim.grid(M)
        if len(outline.perimeters) > 0:
            e = comp.write_perims(out_name, reduce(add, outline.perimeters),
                                  e, ext_fil_ratio, offset, scale)



