#!/anaconda/bin/python3

# <editor-fold> plotone
# import numpy as np
# from numpy import linalg as la
# from numpy import genfromtxt
# from numpy import sqrt
#
# import math
# import re
#
# import wave
# import pyaudio
# import soundfile as sf
#
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.cm as cm
#
# class Vertex:
#     def __init__(self, x, y, z, index, pcs):
#         self.i = index
#         self.x = x
#         self.y = y
#         self.z = z
#         self.pcs = pcs
#         self.max = 0
#         self.pc = None
#         for i in range(len(self.pcs)):
#             p = self.pcs[i]
#             if p > self.max:
#                 self.max = p
#                 self.pc = i
#
# class Edge:
#     def __init__(self, u, v, time, pcs):
#         self.u = u
#         self.v = v
#         self.time = time
#         self.pcs = pcs
#         self.max = 0
#         self.pc = None
#         for i in range(len(self.pcs)):
#             p = self.pcs[i]
#             if p > self.max:
#                 self.max = p
#                 self.pc = i
#
# class Simplex:
#     def __init__(self, faces, vertices, index, time, dim, pcs):
#         self.faces = faces
#         self.vertices = vertices
#         self.index = index
#         self.time = time
#         # self.time = index
#         self.dim = dim
#         self.pcs = pcs
#         self.max = 0
#         self.pc = None
#         for i in range(len(self.pcs)):
#             p = self.pcs[i]
#             if p > self.max:
#                 self.max = p
#                 self.pc = i
#
# class Pair:
#     def __init__(self, birth, death, pcs):
#         self.birth = birth
#         self.death = death
#         self.pcs = pcs
#         self.max = 0
#         self.pc = None
#         for i in range(len(self.pcs)):
#             p = self.pcs[i]
#             if p > self.max:
#                 self.max = p
#                 self.pc = i
#
# MIN_PERS = 3
# SCALE = 3
#
# # options
# VERTEX = True
# EDGE = True
# FACE = True
# EDGE_PERS = True
# FACE_PERS = True
# VOL_PERS = True
# STEREO = True
# BARCODE = False
# BANDD = False
#
# fig = plt.figure(figsize=(16, 8))
# ax1 = fig.add_subplot(121, projection='3d')
# pax = fig.add_subplot(122)
#
# colors=cm.hsv(np.linspace(0,1,13))
# pitches = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab','A','A#/Bb', 'B', ]
# ptext = [ 0 for i in range(12) ]
#
# def init_plot():
#     ax1.cla()
#     ax1.set_xlim([-1.01,1.01])
#     ax1.set_ylim([-1.01,1.01])
#     ax1.set_zlim([-1.01,1.01])
#
#     pax.cla()
#     # pax.set_xlim([0.0,1.01])
#     # pax.set_ylim([0.0,1.01])
#
# init_plot()
#
# def text():
#     a = None
#     # global ptext
#     # for i in range(12):
#     #     if i == 0 or i == 2 or i == 4 or i == 5 or i == 7 or i == 9 or i == 11:
#     #         space = ' :\t\t: '
#     #     # elif i == 10:
#     #     #     space = ' :: '
#     #     else:
#     #         space = ' :\t: '
#     #     pax.text(1.01, 1-0.25*(i/11), str(i)+': '+pitches[i]+ space + str(ptext[i]),
#     #             horizontalalignment='left',
#     #             verticalalignment='top',
#     #             color=colors[i],
#     #             transform=pax.transAxes)
# text()
#
# def drawvertex(u):
#     if VERTEX:
#         ax1.scatter([u.x], [u.y], [u.z],color=colors[u.pc],s=5)
#
# def drawedge(e):
#     if EDGE:
#         ax1.plot([e.u.x,e.v.x],[e.u.y,e.v.y],[e.u.z,e.v.z],color=colors[e.pc])
#
# def drawface(s):
#     if FACE and (s.dim == 2):
#         u = s.vertices[0]
#         v = s.vertices[1]
#         w = s.vertices[2]
#         clr = colors[s.pc]
#         clr[3] = 0.5
#         ax1.plot_trisurf([u.x, v.x, w.x], [u.y, v.y, w.y], [u.z, v.z, w.z],
#                         color=clr, edgecolor='none', shade=False)
#
# def pers(pairs):
#     pax.cla()
#     # if not BARCODE:
#     #     pax.set_xlim([0,length])
#     #     pax.set_ylim([0,length])
#     pitch_born = [[0,0,0,0] for i in range(12)]
#     i = 0
#     features = 0
#     noise = 0
#     for pair in pairs:
#         birth = pair.birth
#         death = pair.death
#         if (death.index - birth.index < MIN_PERS):
#             noise += 1
#         else:
#             features += 1
#             if (death.dim == 1) and EDGE_PERS:
#                 if BARCODE:
#                     # pax.plot([T[birth],T[death]],[i,i],color=colors[itop[birth]])
#                     pax.plot([birth.time,death.time],[death.time,death.time],color=colors[birth.pc])
#                 else :
#                     # pax.scatter(birth,death,color=colors[itop[birth]],marker='x')
#                     pax.scatter(birth.time,death.time,color=colors[birth.pc],marker='x',s=(8*death.dim)**2)
#                     if BANDD:
#                         pax.plot([birth.time,death.time],[death.time,birth.time],color=colors[birth.pc])
#                 pitch_born[birth.pc][0] += 1
#                 i += 1
#             elif (death.dim == 2) and FACE_PERS:
#                 if BARCODE:
#                     # pax.plot([T[birth],T[death]],[i,i],color=colors[itop[birth]])
#                     pax.plot([birth.time,death.time],[death.time,death.time],color=colors[birth.pc])
#                 else :
#                     # pax.scatter(birth,death,color=colors[itop[birth]],marker='x')
#                     pax.scatter(birth.time,death.time,color=colors[birth.pc],marker='^',s=(8*death.dim)**2)
#                     if BANDD:
#                         pax.plot([birth.time,death.time],[death.time,birth.time],color=colors[birth.pc])
#                 pitch_born[birth.pc][1] += 1
#                 i += 1
#             elif (death.dim == 3) and VOL_PERS:
#                 if BARCODE:
#                     # pax.plot([T[birth],T[death]],[i,i],color=colors[itop[birth]])
#                     pax.plot([birth.time,death.time],[death.time,death.time],color=colors[birth.pc])
#                 else :
#                     # pax.scatter(birth,death,color=colors[itop[birth]],marker='x')
#                     pax.scatter(birth.time,death.time,color=colors[birth.pc],marker='o',s=(8*death.dim)**2)
#                     if BANDD:
#                         pax.plot([birth.time,death.time],[death.time,birth.time],color=colors[birth.pc])
#                 pitch_born[birth.pc][2] += 1
#                 i += 1
#             elif (death.dim > 3):
#                 if BARCODE:
#                     # pax.plot([T[birth],T[death]],[i,i],color=colors[itop[birth]])
#                     pax.plot([birth.time,death.time],[death.time,death.time],color=colors[birth.pc])
#                 else :
#                     # pax.scatter(birth,death,color=colors[itop[birth]],marker='x')
#                     pax.scatter(birth.time,death.time,color=colors[birth.pc],marker='o',s=(8*death.dim)**2)
#                     if BANDD:
#                         pax.plot([birth.time,death.time],[death.time,birth.time],color=colors[birth.pc])
#                 pitch_born[birth.pc][3] += 1
#                 i += 1
#
#     # if (len(pairs) > 0):
#     #     print(str(features)+" features\n -> "+str(100*noise/len(pairs))+'%'+" noise\n")
#     # for i in range(12):
#     #     ptext[i] = pitch_born[i][0]+pitch_born[i][1]+pitch_born[i][2]
#     #     print(pitches[i] + ':\t'+ str(pitch_born[i]) +':\t'+
#     #             str(ptext[i]))
#     # text()
#     return features, noise, pitch_born
#
#
# # <editor-fold> animate
# # # last = 0
# # def animate(i):
# #     global vertices
# #     global _pos
# #     if f.tell() < nsamples:
# #         data = [[[None for i in range(ssize)]for k in range(3)] for j in range(delta//epsilon)]
# #         sumsq = [ [0,0,0] for i in range(delta//epsilon) ]
# #         _pos = f.tell()
# #         fs = f.read(3*delta*ssize)
# #         for j in range(delta//epsilon):
# #             for k in range(3):
# #                 for i in range(ssize):
# #                     pos = i + delta*ssize*k + ssize*j*epsilon
# #                     r = fs[pos][0]+fs[pos][1] if STEREO else fs[pos]
# #                     data[j][k][i] = r
# #                     sumsq[j][k] += r*r
# #                 sumsq[j][k] = sumsq[j][k]**(1.0/nsize)
# #         for j in range(delta//epsilon):
# #             P, mz, mi, mp = process(data[j])
# #             u = Vertex(sumsq[j][0], sumsq[j][1], sumsq[j][2], count, mp)
# #             addvertex(u)
# #             if abs(P[(mp+7)%12]) >= thresh*abs(mz):
# #                 u = Vertex(sumsq[j][0], sumsq[j][1], sumsq[j][2], count, (mp+7)%12)
# #                 addvertex(u)
# #             _pos += 3*epsilon*ssize
# #             l = len(vertices)
# #
# #         if f.tell()//(3*ssize) % window == 0:
# #             pers()
# #             print('\n')
# #             print(f.tell()/len(f))
# #         # else: print('\nDONE')
# #     else:
# #         # f.close()
# #         fb = wave.open(file_name,"rb")
# #
# #         #instantiate PyAudio
# #         p = pyaudio.PyAudio()
# #
# #         #open stream
# #         stream = p.open(format = p.get_format_from_width(fb.getsampwidth()),
# #                         channels = fb.getnchannels(),
# #                         rate = fb.getframerate(),
# #                         output = True)
# #
# #         d = fb.readframes(ssize)
# #         # play stream
# #         pos = 0
# #         # ppos = pax.scatter(0,0,color='black',marker='o')
# #         while len(d) > 0:
# #             stream.write(d)
# #             # del ppos
# #             # ppos = pax.scatter(pos/(60.0*fb.getframerate()),pos/(60.0*fb.getframerate()),color='black',marker='o')
# #             print(pos/(60.0*fb.getframerate()))
# #             d = fb.readframes(ssize)
# #             pos += ssize
# #
# # ani = animation.FuncAnimation(fig, animate)
# # </editor-fold> animate
#
# def run(dir_name, name, count, e, a):
#     # print("running directory "+ dir_name)
#     vertices = []
#     file_name = dir_name+"vertices.txt"
#     data_string = genfromtxt(file_name, delimiter='\t', dtype=str)
#     for row_string in data_string:
#         for member in row_string:
#             n = re.sub(r"\([^)]*\)", "", member)
#             m = re.search(r'\(([^]]*)\)', member)
#             if (n == "index"):
#                 index = int(m.group(1));
#                 # print(n + " " + str(index))
#             elif (n == "time"):
#                 time = float(m.group(1))
#                 # print(n + " " + str(time))
#             elif (n == "point"):
#                 point = [float(x) for x in m.group(1).split(',')]
#                 # print(n + " " + str(point))
#             elif (n == "pcs"):
#                 pcs = [float(x) for x in m.group(1).split(',')]
#                 # print(n + " " + str(pcs))
#             else:
#                 print("ERROR@"+member)
#         vertex = Vertex(SCALE*point[0], SCALE*point[1], 2*(time - 0.5), index, pcs)
#         vertices += [vertex]
#         drawvertex(vertex)
#
#     edges = []
#     file_name = dir_name+"edges.txt"
#     data_string = genfromtxt(file_name, delimiter='\t', dtype=str)
#     for row_string in data_string:
#         for member in row_string:
#             n = re.sub(r"\([^)]*\)", "", member)
#             m = re.search(r'\(([^]]*)\)', member)
#             if (n == "u"):
#                 u = vertices[int(m.group(1))];
#                 # print(n + " " + str(u))
#             elif (n == "v"):
#                 v = vertices[int(m.group(1))];
#                 # print(n + " " + str(v))
#             elif (n == "time"):
#                 time = float(m.group(1))
#                 # print(n + " " + str(time))
#             else:
#                 print("ERROR@"+member)
#         pcs = [u.pcs[i]+v.pcs[i] for i in range(min(len(u.pcs),len(v.pcs)))]
#         edge = Edge(u, v, time, pcs)
#         edges += [edge]
#         drawedge(edge)
#
#     simplices = []
#     file_name = dir_name+"simplices.txt"
#     data_string = genfromtxt(file_name, delimiter='\t', dtype=str)
#     for row_string in data_string:
#         for member in row_string:
#             n = re.sub(r"\([^)]*\)", "", member)
#             m = re.search(r'\(([^]]*)\)', member)
#             if (n == "index"):
#                 index = int(m.group(1));
#                 # print(n + " " + str(index))
#             elif (n == "time"):
#                 time = float(m.group(1))
#                 # print(n + " " + str(time))
#             elif (n == "dim"):
#                 dim = int(m.group(1))
#                 # print(n + " " + str(time))
#             elif (n == "faces"):
#                 if (m.group(1) != ""):
#                     faces = [int(i) for i in m.group(1).split(',')]
#                 else: faces = []
#                     # print(n + " " + str(point))
#             elif (n == "vertices"):
#                 point = [int(i) for i in m.group(1).split(',')]
#                 # print(n + " " + str(point))
#             elif (n == "pcs"):
#                 pcs = [float(x) for x in m.group(1).split(',')]
#                 # print(n + " " + str(pcs))
#             else:
#                 print("ERROR@"+member)
#         simplex = Simplex(faces, vertices, index, time, dim, pcs)
#         simplices += [simplex]
#         if (simplex.dim == 2):
#             drawface(simplex)
#
#     pairs = []
#     file_name = dir_name+"pairs.txt"
#     data_string = genfromtxt(file_name, delimiter='\t', dtype=str)
#     for row_string in data_string:
#         for member in row_string:
#             n = re.sub(r"\([^)]*\)", "", member)
#             m = re.search(r'\(([^]]*)\)', member)
#             if (n == "birth"):
#                 birth = simplices[int(m.group(1))];
#                 # print(n + " " + str(u))
#             elif (n == "death"):
#                 death = simplices[int(m.group(1))];
#                 # print(n + " " + str(v))
#             else:
#                 print("ERROR@"+member)
#         pcs = [birth.pcs[i]+death.pcs[i] for i in range(min(len(birth.pcs),len(death.pcs)))]
#         pair = Pair(birth,death,pcs)
#         pairs += [pair]
#
#     nvertices = len(vertices)
#     nedges = len(edges)
#     nsimplices = len(simplices)
#     npairs = len(pairs)
#     # print(str(nvertices)+" vertices")
#     # print(str(nedges)+" edges")
#     kgt = (nsimplices - nedges - nvertices)/nsimplices
#     # print(str(nsimplices)+" simplices\n -> "+str(100*kgt)+'%'+" (k > 2)-simplices")
#     # print(str(npairs)+" pairs")
#
#     features, noise, pitch_born = pers(pairs)
#     noise_ratio = 1
#     if (len(pairs) > 0):
#         noise_ratio = noise/len(pairs)
#         # print(str(features)+" features\n -> "+
#         #     str(100*noise_ratio)+'%'+" noise")
#
#     # plt.show()
#     # png_path = dir_name+"plot"+".png"
#     png_path = "data/"+str(name)+"-"
#     if (count < 10):
#         png_path += "00000"
#     elif (count < 100):
#         png_path += "0000"
#     elif (count < 1000):
#         png_path += "000"
#     elif (count < 10000):
#         png_path += "00"
#     elif (count < 100000):
#         png_path += "0"
#
#     png_path += str(count)+".png"
#     print("saving "+png_path)
#     plt.savefig(png_path)
#
#     ratio = e/a
#
#     f = open("data/stats.txt","a+")
#     f.write(dir_name+"\t"+png_path+"\t"+str(kgt)+"\t"+str(noise_ratio)+"\t"+str(ratio)+"\n")
#     f.close()
#
#     init_plot()
# </editor-fold> plotone

import sys
import subprocess
sys.path.append('plot-one.py')
from plotone import *

program = "./tdsa-igl"
wav = "715"
# wav = "22"

dim = 10

init_e = 0.005
init_a = 0.05
step_e = 0.005
step_a = 0.05

if (len(sys.argv) == 2):
    wav = sys.argv[1]
elif (len(sys.argv) == 5):
    init_e = float(sys.argv[1])
    step_e = float(sys.argv[2])
    init_a = float(sys.argv[3])
    step_a = float(sys.argv[4])
elif (len(sys.argv) == 6):
    wav = sys.argv[1]
    init_e = float(sys.argv[2])
    step_e = float(sys.argv[3])
    init_a = float(sys.argv[4])
    step_a = float(sys.argv[5])

wav_path = "wavs/"+wav+".wav"

print("\nfile path : " + wav_path)
print(" > dim = "+ str(dim))

build_errors = 0;
run_errors = 0
errors = []
print("\nSTARTING ALPHA BY EPSILON")
# subprocess.run('date +"%T"', shell=True, check=True)

# N = 5000
# STEP = 5
# ITS = 0
# for e in range(1,N//STEP):
#     for a in range(e,N//STEP):
#         ITS += 1
# print(ITS)

count = 0
# for e in range(STEP,N//STEP):
i = 0
_e = 0
while (_e <= 0.2):
# for a in range(1,N):
    _e = init_e + i*step_e
    _e = round(_e*100000)/100000
    print("\n STARTING _e = " + str(_e))
    # print("\n STARTING a = " + str(a))
    # subprocess.run('date +"%T"', shell=True, check=True)
    # _e = STEP*e/(N)
    # _a = STEP*a/N
    j = 0
    _a = 0
    while (_a <= 0.5):
    # for a in range(e,N//STEP//10):
    # for e in range(a):
        _a = init_a + j*step_a
        _a = round(_a*100000)/100000
        # _a = 5*STEP*a/N
        # _e = STEP*e/N
        string = program+" "+wav_path+" "+str(_e)+" "+str(_a)+" "+str(dim);
        print("["+str(count)+"] BUILDING "+program+" "+wav_path+" "+str(_e)+" "+str(_a)+" "+str(dim))
        try:
            subprocess.run(string, stderr=subprocess.STDOUT, shell=True, check=True)
            try:
                e_ = int(_e)
                a_ = int(_a)
                if (e_ == _e) or (_e == 0):
                    _e = e_
                if (a_ == _a) or (_a == 0):
                    _a = a_
                dir_name = "data/"+wav+"_"+str(_e)+"_"+str(_a)+"_0/"
                print(" > RUNNING "+dir_name)
                run(dir_name, wav, count, _e, _a)
            except IOError as err:
                run_errors += 1
                errors += [count]
                print(" ----------------------- ")
                print(" ------ RUN ERROR ------ ")
                print(" ----------------------- ")
                print("IO error: {0}".format(err))
                print("\t "+ str(run_errors) +" run errors\n")
            except IndexError as err:
                run_errors += 1
                errors += [count]
                print(" ----------------------- ")
                print(" ------ RUN ERROR ------ ")
                print(" ----------------------- ")
                print("IO error: {0}".format(err))
                print("\t "+ str(run_errors) +" run errors\n")
        except subprocess.CalledProcessError as err:
            build_errors += 1
            errors += [count]
            print(" -------- ERROR -------- ")
            print(err)
            print(" _______________________")
            print("\t "+ str(build_errors) +" build errors\n")
        print(" "+str(count)+" > DONE ("+str(_e)+", "+str(_a)+")")
        j += 1
        count += 1
        # print("\n ... "+str(100*count/ITS)+'%')
    print(" DONE _e = " + str(_e))
    i += 1
    # print(" DONE a = " + str(a))
    # subprocess.run('date +"%T"', shell=True, check=True)
print("\nDONE alpha/epsilon ("+
# print("\nDONE epsilon/alpha: "+
    str(count)+" iterations ("+
    str(build_errors) + " build errors, "+
    str(run_errors) + " run errors )")
print("errors at "+ str(errors))

for err in errors:
    touch = "touch /data/"+wav
    if (err < 10):
        touch += "00000"
    elif (err < 100):
        touch += "0000"
    elif (err < 1000):
        touch += "000"
    elif (err < 10000):
        touch += "00"
    elif (err < 100000):
        touch += "0"
    touch += str(err) + ".png"

    subprocess.run(touch, stderr=subprocess.STDOUT, shell=True, check=True)

# <editor-fold e/a
# print("\nSTARTING EPSILON BY ALPHA")
# subprocess.run('date +"%T"', shell=True, check=True)
# for a in range(200):
#     print("\n > STARTING a = " + str(a))
#     subprocess.run('date +"%T"', shell=True, check=True)
#     for e in range(a):
#         _e = 5*e/1000
#         _a = 5*a/1000
#         string = program+" "+wav_path+" "+str(_e)+" "+str(_a)+" "+str(dim);
#         print("\n  : > RUNNING "+program+" "+wav_path+" "+str(_e)+" "+str(_a)+" "+str(dim))
#         try:
#             out = subprocess.run(string, stderr=subprocess.STDOUT, shell=True, check=True)
#         except subprocess.CalledProcessError:
#             errors2 += 1
#             print("\n -------- ERROR -------- ")
#             print(out)
#             print(" _______________________ \n")
#         print("  :  _ DONE ("+str(_e)+", "+str(_a)+")")
#     print("\n  _ DONE a = " + str(a))
#     subprocess.run('date +"%T"', shell=True, check=True)
# print("\nDONE epsilon/alpha ("+ str(errors2) + "errors )")
# </editor-fold> e/a

errors = build_errors + run_errors
print("DONE ("+str(errors)+" total)")
subprocess.run('date +"%T"', shell=True, check=True)

# <editor-fold> misc
# DATA IMPORT

# import csv
#
# results = []
# with open('data/715_0.05_0.1_0/vertices.txt', newline='\n') as inputfile:
#     for row in csv.reader(inputfile):
#         row.split("\t")
#         print(row)
        # results.append(row)

# rows = data_string.shape[0]
# cols = data_string.shape[1]-2
#
# N_total = rows
# N = 2*N_total//3
# M = cols
#
# print('\nN = '+ str(N_total))
# print('M = '+ str(M))
#
# data_string = data_string.T
# id_vector = data_string[0].astype(np.int)
#
# y = np.asarray([ 0 if data_string[1][i] == 'B' else 1 for i in range(N_total) ])
# y_train = y[:N]
# y_test = y[N:]
#
# X = data_string[2:].astype(np.float).T
# mx = []
# for x in X:
#     mx += [max(x)]
# mX = max(mx)
# for i in range(N_total):
#     for j in range(M):
#         X[i][j] /= mX
#
# X_train = X[:N]
# X_test = X[N:]
# </editor-fold> misc
