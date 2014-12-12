from sys import argv

def get_pts(f_name):
    pts = []
    with open(f_name) as f:
        line = f.readline().split()
        while line:
            if 'vertex' in line:
                pt = [float(line[1]), float(line[2]), float(line[3])]
                if not pt in pts:
                    pts.append(pt)
            line = f.readline().split()
    return pts

def write_pts(f_name,pts):
    if f_name[-4:] in ['.stl', '.STL']:
        out_name = f_name[:-4] + '.ptc'
    else:
        out_name = 'out.ptc'

    with open(out_name, 'w') as f:
        for pt in pts:
            f.write(str(pt[0]) + ',' + str(pt[1]) + ',' + str(pt[2]) + '\n')


if __name__ == '__main__':
    f_name = argv[1]
    write_pts(f_name,get_pts(f_name))

