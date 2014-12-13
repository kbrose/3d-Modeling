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
ext_fil_ratio = filament_width / extruder_width * 1.35
layer_height = 0.35 # in mm
offset = [30., 30.] # in mm
scale = .3
resolution_rescale = 1.

# SOFTWARE SETTINGS
NU = 0.0005
GAMMA = 0.06
KERNEL = 'rbf'

def main():
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
    x_vals = [scale * x[0] for x in pts]
    min_x = min(x_vals)
    x_vals = [x - min_x for x in x_vals]

    y_vals = [scale * x[1] for x in pts]
    min_y = min(y_vals)
    y_vals = [y - min_y for y in y_vals]

    z_vals = [scale * x[2] * 2 for x in pts]
    min_z = min(z_vals)
    z_vals = [z - min_z for z in z_vals]

    pts = zip(x_vals, y_vals, z_vals)

    x_axis = np.linspace(0, max(x_vals), max(x_vals) / (extruder_width * resolution_rescale)+1).tolist()
    y_axis = np.linspace(0, max(y_vals), max(y_vals) / (extruder_width * resolution_rescale)+1).tolist()
    xy_grid = [[x,y] for x in x_axis for y in y_axis]
    z_axis = np.linspace(0, max(z_vals), max(z_vals) / (layer_height)+1).tolist()

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
            out.write('G1 Z%.4f\n' % z)
        M = clf.decision_function([x + [z] for x in xy_grid])
        M = M.reshape([len(x_axis), len(y_axis)])
        M = [[M[i][j] > 0 for i in range(len(M))] for j in range(len(M[0]))]
        outline = perim.grid(M)
        # outline.showAll()
        # time.sleep(.2)
        if len(outline.perimeters) > 0:
            e = comp.write_perims(out_name, reduce(add, outline.perimeters),
                                  e, ext_fil_ratio, offset)


if __name__ == '__main__':
    main()



