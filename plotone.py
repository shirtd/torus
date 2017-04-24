#!/anaconda/bin/python3

import numpy as np
from numpy import linalg as la
from numpy import genfromtxt
from numpy import sqrt

import math
import re

import matplotlib as mpl
import matplotlib.pyplot as plt
# import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

import sys
import time

class Vertex:
    def __init__(self, x, y, z, index):
        self.i = index
        self.x = x
        self.y = y
        self.z = z

class Edge:
    def __init__(self, u, v, filtration):
        self.u = u
        self.v = v
        self.filtration = filtration

class Simplex:
    def __init__(self, faces, vertices, index, dim, filtration):
        self.faces = faces
        self.vertices = vertices
        self.index = index
        self.dim = dim
        self.filtration = filtration

class Pair:
    def __init__(self, birth, death, birth_norm, death_norm):
        self.birth = birth
        self.death = death
        self.birth_norm = birth_norm
        self.death_norm = death_norm

MIN_PERS = 15
SCALE = 1

# options
VERTEX = True
EDGE = True
FACE = True
EDGE_PERS = True
FACE_PERS = True
VOL_PERS = True
STEREO = True
BARCODE = False
BANDD = False

fig = plt.figure(figsize=(16, 8))
ax1 = fig.add_subplot(121, projection='3d')
pax = fig.add_subplot(122)

def init_plot():
    ax1.cla()
    ax1.set_xlim([-1.0,1.0])
    ax1.set_ylim([-1.0,1.0])
    ax1.set_zlim([-1.0,1.0])
    ax1.elev = 30.0

    pax.cla()
    pax.set_xlim([-0.1,1.0])
    pax.set_ylim([-0.1,1.0])
    clr = [0,0,0,0.2]
    pax.plot([-1,1],[-1,1],color=clr)

init_plot()

def drawvertex(u):
    if VERTEX:
        clr = [0,0,1,1]
        ax1.scatter([u.x], [u.y], [u.z],color=clr)

def drawedge(e):
    if EDGE:
        clr = [0,1,0,1]
        ax1.plot([e.u.x,e.v.x],[e.u.y,e.v.y],[e.u.z,e.v.z], color=clr)

def drawface(s):
    if FACE and (s.dim == 2):
        u = s.vertices[0]
        v = s.vertices[1]
        w = s.vertices[2]
        clr = [1,0,0,0.01]
        e_clr = [0,1,0,0.02]
        ax1.plot_trisurf([u.x, v.x, w.x], [u.y, v.y, w.y], [u.z, v.z, w.z],
                        color=clr,edgecolor=e_clr, shade=False)

def pers(pairs, a_last, a):
    i = 0
    features = 0
    noise = 0
    del_pair = []
    for pair in pairs:
        birth = pair.birth
        death = pair.death
        birth_norm = pair.birth_norm
        death_norm = pair.death_norm
        # if (death.time - birth.time > 0):
        #     pairs_time += [(birth.time,death.time)]
        if (death.index - birth.index < MIN_PERS):
            noise += 1
        elif (a_last < death.filtration) and (death.filtration <= a):
            features += 1
            if (death.dim == 1) and EDGE_PERS:
                if BARCODE:
                    # pax.plot([T[birth],T[death]],[i,i],color=colors[itop[birth]])
                    pax.plot([birth_norm,death_norm],[death_norm,death_norm])
                else :
                    # pax.scatter(birth,death,color=colors[itop[birth]],marker='x')
                    clr = [0,1,0,1]
                    pax.scatter(birth_norm,death_norm,marker='x',color=clr,s=(5*death.dim)**2)
                    if BANDD:
                        pax.plot([birth_norm,death_norm],[death_norm,birth_norm])
                i += 1
            elif (death.dim == 2) and FACE_PERS:
                if BARCODE:
                    # pax.plot([T[birth],T[death]],[i,i],color=colors[itop[birth]])
                    pax.plot([birth_norm,death_norm],[death_norm,death_norm])
                else :
                    # pax.scatter(birth,death,color=colors[itop[birth]],marker='x')
                    clr = [1,0,0,0.5]
                    pax.scatter(birth_norm,death_norm,marker='^',color=clr,s=(5*death.dim)**2)
                    if BANDD:
                        pax.plot([birth_norm,death_norm],[death_norm,birth_norm])
                i += 1
            elif (death.dim == 3) and VOL_PERS:
                if BARCODE:
                    # pax.plot([T[birth],T[death]],[i,i],color=colors[itop[birth]])
                    pax.plot([birth_norm,death_norm],[death_norm,death_norm])
                else :
                    clr = [0,0,1,0.25]
                    # pax.scatter(birth,death,color=colors[itop[birth]],marker='x')
                    pax.scatter(birth_norm,death_norm,marker='o',color=clr,s=(5*death.dim)**2)
                    if BANDD:
                        pax.plot([birth_norm,death_norm],[death_norm,birth_norm])
                i += 1
            elif (death.dim > 3):
                if BARCODE:
                    # pax.plot([T[birth],T[death]],[i,i],color=colors[itop[birth]])
                    pax.plot([birth_norm,death_norm],[death_norm,death_norm])
                else :
                    clr = [0,1,0,0.1]
                    # pax.scatter(birth,death,color=colors[itop[birth]],marker='x')
                    pax.scatter(birth_norm,death_norm,marker='o',color=clr,s=(5*death.dim)**2)
                    if BANDD:
                        pax.plot([birth_norm,death_norm],[death_norm,birth_norm])
                i += 1
            del_pair += [pair]

    return features, noise, del_pair

# def run(dir_name, name, count, a):
def import_file(dir_name):
    # print("running directory "+ dir_name)
    vertices = []
    file_name = dir_name+"vertices.txt"
    data_string = genfromtxt(file_name, delimiter='\t', dtype=str)
    for row_string in data_string:
        for member in row_string:
            n = re.sub(r"\([^)]*\)", "", member)
            m = re.search(r'\(([^]]*)\)', member)
            if (n == "index"):
                index = int(m.group(1));
                # print(n + " " + str(index))
            elif (n == "point"):
                point = [float(x) for x in m.group(1).split(',')]
                # print(n + " " + str(point))
            else:
                print("ERROR(vertices)@"+member)
        vertex = Vertex(SCALE*point[0], SCALE*point[1], SCALE*point[2], index)
        vertices += [vertex]
        # drawvertex(vertex)

    nvertices = len(vertices)
    print(str(nvertices) + " vertices")

    edges = []
    file_name = dir_name+"edges.txt"
    data_string = genfromtxt(file_name, delimiter='\t', dtype=str)
    for row_string in data_string:
        for member in row_string:
            n = re.sub(r"\([^)]*\)", "", member)
            m = re.search(r'\(([^]]*)\)', member)
            if (n == "u"):
                u = vertices[int(m.group(1))];
                # print(n + " " + str(u))
            elif (n == "v"):
                v = vertices[int(m.group(1))];
                # print(n + " " + str(v))
            elif (n == "filtration"):
                flt = float(m.group(1))
                # print(n + " " + str(v))
            else:
                print("ERROR(edges)@"+member)
        edge = Edge(u, v, flt)
        edges += [edge]
        # if (edge.filtration <= a):
        #     drawedge(edge)

    nedges = len(edges)
    print(str(nedges) + " edges")

    simplices = []
    file_name = dir_name+"simplices.txt"
    data_string = genfromtxt(file_name, delimiter='\t', dtype=str)
    for row_string in data_string:
        for member in row_string:
            n = re.sub(r"\([^)]*\)", "", member)
            m = re.search(r'\(([^]]*)\)', member)
            if (n == "index"):
                index = int(m.group(1));
                # print(n + " " + str(index))
            elif (n == "dim"):
                dim = int(m.group(1))
                # print(n + " " + str(time))
            elif (n == "faces"):
                if (m.group(1) != ""):
                    faces = [int(i) for i in m.group(1).split(',')]
                else: faces = []
                    # print(n + " " + str(point))
            elif (n == "vertices"):
                verts = [vertices[int(i)] for i in m.group(1).split(',')]
                # print(n + " " + str(point))
            elif (n == "filtration"):
                filtration = float(m.group(1))
                # print(n + " " + str(time))
            else:
                print("ERROR(simplices)@"+member)
        sim = Simplex(faces, verts, index, dim, filtration)
        simplices += [sim]
        # if (sim.filtration <= a):
        #     if (sim.dim == 2):
        #         drawface(sim)

    nsimplices = len(simplices)
    print(str(nsimplices) + " simplices")

    pairs = []
    file_name = dir_name+"pairs.txt"
    data_string = genfromtxt(file_name, delimiter='\t', dtype=str)
    for row_string in data_string:
        for member in row_string:
            n = re.sub(r"\([^)]*\)", "", member)
            m = re.search(r'\(([^]]*)\)', member)
            if (n == "birth"):
                birth = simplices[int(m.group(1))];
                birth_norm = birth.index/nsimplices
                # print(n + " " + str(u))
            elif (n == "death"):
                death = simplices[int(m.group(1))];
                death_norm = death.index/nsimplices
                # print(n + " " + str(v))
            else:
                print("ERROR(pairs)@"+member)
        # pcs = [birth.pcs[i]+death.pcs[i] for i in range(min(len(birth.pcs),len(death.pcs)))]
        pair = Pair(birth,death,birth_norm,death_norm)
        pairs += [pair]

    npairs = len(pairs)
    print(str(npairs) + " pairs")
    return vertices, edges, simplices, pairs

def draw(name, vertices, edges, simplices, pairs, count, a_last, a):
    nvertices = len(vertices)
    nedges = len(edges)
    nsimplices = len(simplices)
    npairs = len(pairs)

    del_edge = []
    del_simplex = []

    if EDGE:
        for e in edges:
            if (a_last < e.filtration) and (e.filtration <= a):
                drawedge(e)
                del_edge += [e]

    if FACE:
        for s in simplices:
            if (s.dim == 2):
                if (a_last < s.filtration) and (s.filtration <= a):
                    drawface(s)
                    del_simplex += [s]
            elif s.dim < 2:
                del_simplex += [s]

    if (nsimplices > 0):
        kgt = (nsimplices - nedges - nvertices)/nsimplices
    else:
        kgt = 0.0

    features, noise, del_pair = pers(pairs, a_last, a)

    noise_ratio = 1
    if (len(pairs) > 0):
        noise_ratio = noise/len(pairs)

    a_text = pax.text(1.02, 1-0.40, "  _a = "+str(a),
            horizontalalignment='left',
            verticalalignment='top',
            transform=pax.transAxes)
    noise_text = pax.text(1.02, 1-0.46, "noise ~ "+str(round(100*noise_ratio))+'%',
            horizontalalignment='left',
            verticalalignment='top',
            transform=pax.transAxes)
    kgt_text = pax.text(1.02, 1-0.5, "   kgt ~ "+str(round(100*kgt))+'%',
            horizontalalignment='left',
            verticalalignment='top',
            transform=pax.transAxes)

    # png_path = dir_name+"plot"+".png"
    png_path = "data/"+str(name)+"-"
    if (count < 10):
        png_path += "00000"
    elif (count < 100):
        png_path += "0000"
    elif (count < 1000):
        png_path += "000"
    elif (count < 10000):
        png_path += "00"
    elif (count < 100000):
        png_path += "0"

    png_path += str(count)+".png"
    print("saving "+png_path)
    plt.savefig(png_path)

    a_text.remove()
    noise_text.remove()
    kgt_text.remove()
    # f = open("data/stats.txt","a+")
    # f.write(dir_name+"\t"+png_path+"\t"+str(kgt)+"\t"+str(noise_ratio)+"\n")
    # f.close()

    # plt.show()
    # init_plot()

    return del_edge, del_simplex, del_pair

dirname = "data/orus_0/"
name = 'orus'
count = 0
_a = 0
if (len(sys.argv) == 2):
    dirname = sys.argv[1]
elif (len(sys.argv) == 2):
    dirname = sys.argv[1]
    _a = float(sys.argv[2])
elif (len(sys.argv) == 3):
    dirname = sys.argv[1]
    _a = float(sys.argv[2])
    count = int(sys.argv[3])

vertices, edges, simplices, pairs = import_file(dirname)
for v in vertices:
    drawvertex(v)

reso = 20
start_time = time.time()
for i in range(reso-3):
    a_last = (i-1)/reso
    a_cur = i/reso
    # draw(name, vertices, edges, simplices, pairs, i-1, a_last, a_cur)
    del_edge, del_simplex, del_pair = draw(name, vertices, edges, simplices, pairs, i, a_last, a_cur)
    for e in del_edge:
        edges.remove(e)
    for s in del_simplex:
        simplices.remove(s)
    for p in del_pair:
        pairs.remove(p)
print("--- %s seconds ---" % (time.time() - start_time))
