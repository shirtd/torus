#!/anaconda/bin/python3

import numpy as np
from numpy import linalg as la
from numpy import genfromtxt
from numpy import sqrt

import math
from math import pi
from math import sin
from math import cos

import re

import math
import re

# import wave
# import pyaudio
# import soundfile as sf

from random import randrange, uniform

PLOT = False
WRITE = True

sample = []
X = []
Y = []
Z = []
nsamples = 300
for i in range(nsamples):
    u = uniform(0,2*pi)
    v = uniform(0,2*pi)
    sample += [(u,v)]
    # print("("+str(u)+", "+str(v)+")")
    x = (0.6 + 0.16*cos(u))*cos(v)
    y = (0.6 + 0.16*cos(u))*sin(v)
    z = 0.16*sin(u)
    X += [x]
    Y += [y]
    Z += [z]

if WRITE:
    # pairs_file = "torus"+str(1000)+".txt"
    file_name = "torus.txt"
    with open(file_name,'w') as torus_file:
        for i in range(nsamples):
            torus_file.write(str(X[i])+" "+str(Y[i])+" "+str(Z[i])+"\n")

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
