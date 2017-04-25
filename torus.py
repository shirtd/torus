#!/anaconda/bin/python3

import numpy as np
from numpy import linalg as la
from numpy import genfromtxt
from numpy import sqrt

import math
from math import pi
from math import sin
from math import cos

from random import randrange, uniform

import sys

PLOT = False
WRITE = True

sample = []
X = []
Y = []
Z = []
nsamples = 50

R = 0.6
r = 0.16

if (len(sys.argv) > 1):
    nsamples = int(sys.argv[1])
if (len(sys.argv) > 2):
    R = float(sys.argv[2])
if (len(sys.argv) > 3):
    r = float(sys.argv[3])

d = R - r
d = round(d*10000)/10000
print(str(nsamples)+" samples")
print("R = "+str(R))
print("r = "+str(r))
print("d = "+str(d))

for i in range(nsamples):
    u = uniform(0,2*pi)
    v = uniform(0,2*pi)
    sample += [(u,v)]
    # print("("+str(u)+", "+str(v)+")")
    x = (R + r*cos(u))*cos(v)
    y = (R + r*cos(u))*sin(v)
    z = r*sin(u)
    X += [x]
    Y += [y]
    Z += [z]

if WRITE:
    # pairs_file = "torus"+str(1000)+".txt"
    file_name = "torus.txt"
    with open(file_name,'w') as torus_file:
        for i in range(nsamples):
            torus_file.write(str(X[i])+" "+str(Y[i])+" "+str(Z[i])+"\n")
    file_name = "torus_pairs.txt"
    with open(file_name,'w') as pair_file:
        pair_file.write("0.0 "+str(2*r)+"\n")
        pair_file.write("0.0 "+str(2*d)+"\n")

if PLOT:
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.cm as cm

    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(111, projection='3d')

    ax1.set_xlim([-1.0,1.0])
    ax1.set_ylim([-1.0,1.0])
    ax1.set_zlim([-1.0,1.0])

    ax1.scatter(X, Y, Z, s=2)

    plt.show()
