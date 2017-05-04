import sys
import subprocess
from subprocess import Popen, PIPE
import re
import struct

import numpy as np
from numpy import linalg as la

import matplotlib.pyplot as plt

# sample_sizes = [10, 50, 100, 150, 200]
sample_sizes = [40,60,80,100,120,140,160,180,200]
num_tests = 10

pair_file_strings = []
bottleneck_distance = [[-1 for i in range(num_tests)] for i in sample_sizes]
bottleneck_average = [0 for i in sample_sizes]

file_dir = "bottleneck_plot_files/"

j = 0
for size in sample_sizes:
    for i in range(num_tests):
        dest_string = file_dir+"torus_"+str(size)+"_"+str(i)
        cmd_string = "python3 torus.py "+str(size)+" 0.5 0.1;"
        cmd_string += "./torus torus;"
        cmd_string += "mv data/torus "+dest_string+";"
        # cmd_string += "mv torus.txt torus_pairs.txt "+dest_string
        cmd_string += "cp torus.txt torus_pairs.txt "+dest_string
        pair_file_string = dest_string+"/pairs_filt.txt"
        pair_file_strings += [pair_file_string]
        # cmd_string += "; cat "+ pair_file_string
        # try:
        #     subprocess.run(cmd_string, stderr=subprocess.STDOUT, shell=True, check=True)
        # except subprocess.CalledProcessError as err:
        #     print(err)
        try:
            p = Popen(['./bottleneck_dist', pair_file_string, "torus_pairs.txt"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, err = p.communicate(b"input data that is passed to subprocess' stdin")
            output_string = output.decode()
            distance = float(output_string)
            bottleneck_distance[j][i] = distance
            bottleneck_average[j] += distance
        except ValueError as valerr:
            # errors[0] = True
            print(str(err)+" "+str(valerr))
            # print(sample_strings[i]+" "+sample_strings[j])
            # print(output_string)
    bottleneck_average[j] = bottleneck_average[j]/num_tests
    j += 1

print(bottleneck_distance)
print(bottleneck_average)

X = []
Y = []
for i in range(len(sample_sizes)):
    X += [np.log(np.log(sample_sizes[i])/sample_sizes[i])]
    Y += [np.log(bottleneck_average[i])]

fig = plt.figure(figsize=(8, 8))
ax1 = fig.add_subplot(111)
ax1.scatter(X, Y)
plt.show()
