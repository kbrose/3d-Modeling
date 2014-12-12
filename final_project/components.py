import sys
import ast
import math

def distance(p0, p1):
        p0 = map(float, p0)
        p1 = map(float, p1)
        return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def make_gcode(component, e, out_name, offset, ext_fil_ratio):
    with open(out_name, 'a') as out:
        prev = component[0]
        out.write("G1 X%.4f Y%.4f F7800.00\n" % (prev[0] + offset[0], prev[1] + offset[1]))
        out.write("G1 E%.4f F1800.00\n" % e)
        for coords in component[1:]:
            e += distance(prev, coords) / float(ext_fil_ratio)
            out.write("G1 X%.4f Y%.4f E%.4f\n" % (coords[0] + offset[0], coords[1] + offset[1], e))
            prev = coords
        out.write("G1 F1800.000 E0.12842\n")
    return e

def write_prelude(out_name):
    with open(out_name, 'a') as out:    
        prelude ="""G21 ; set units to millimeters
        M107
        M104 S200 ; set temperature
        M212 Z-.4
        G28 ; home all axes
        G28 X0 Y0
        G29
        G1 Z5 F5000 ; lift nozzle
        M109 S200 ; wait for temperature to be reached
        G90 ; use absolute coordinates
        G92 E0
        M82 ; use absolute distances for extrusion
        G1 F1800.000 E-1.00000
        G92 E0
        M106 S255
        G1 F1800.000 E13.34921
        G92 E0
        G1 Z0.210 F7800.000\n"""
        out.write(prelude)

def write_postlude(out_name):
    with open(out_name, 'a') as out:
        end = """G92 E0
        G1 F1800.000 E0.12842
        G92 E0
        M107
        M104 S0 ; turn off temperature
        G28 X0  ; home X axis
        M84     ; disable motors
        """
        out.write(end)

def write_perims(out_name, perims, e, ext_fil_ratio, offset=[50.,50.]):
    hist = -1
    component = []
    for i in perims:
        i = map(tuple, i)
        i[0] = (i[0][0], i[0][1])
        i[1] = (i[1][0], i[1][1])
        if hist == -1:
          hist = i[0]
        component.append(i[0])
        # component.append(i[1])
        if i[1] == hist:
            # print 'here'
            # print i, hist, i[0], i[1], i[1] == hist
            component.append(i[1])
            e = make_gcode(component, e, out_name, offset, ext_fil_ratio)
            component = []
            hist = -1
    return e

if __name__ == '__main__':
    f = open(sys.argv[1], 'r')
    out = open('out.gcode', 'w')

    a = ast.literal_eval(f.readline())

    hist = -1
    component = []

    write_prelude('out.gcode')

    e = 1.0
    for i in a:
        i = map(tuple, i)
        i[0] = (4.5*i[0][0], 4.5*i[0][1])
        i[1] = (4.5*i[1][0], 4.5*i[1][1])
        if hist == -1:
          hist = i[0]
        component.append(i[0])
        # component.append(i[1])
        if i[1] == hist:
            # print 'here'
            # print i, hist, i[0], i[1], i[1] == hist
            component.append(i[1])
            e = make_gcode(component, e)
            component = []
            hist = -1

    write_postlude('out.gcode')
