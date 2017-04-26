
import sys
import subprocess
from subprocess import Popen, PIPE
import re
import struct

import numpy as np
from numpy import linalg as la

GENERATE = False
RESET = True
TEST = True
SAVE = True

size = 100
reso = 10

if (len(sys.argv) > 1):
    for i in range(1,len(sys.argv)):
        if (str(sys.argv[i]).lower() == "generate"):
            GENERATE = True
        elif (str(sys.argv[i]).lower() == "reset"):
            RESET = True
        elif (str(sys.argv[i]).lower() == "test"):
            GENERATE = True
        elif (str(sys.argv[i]).lower() == "save"):
            RESET = True
        elif (str(sys.argv[i]).lower() == "nogenerate"):
            GENERATE = False
        elif (str(sys.argv[i]).lower() == "noreset"):
            RESET = False
        elif (str(sys.argv[i]).lower() == "notest"):
            GENERATE = False
        elif (str(sys.argv[i]).lower() == "nosave"):
            RESET = False
        elif (str(sys.argv[i]).lower() == "-s"):
            size = int(sys.argv[i+1])
        elif (str(sys.argv[i]).lower() == "-r"):
            reso = int(sys.argv[i+1])

print()
if GENERATE: print("GENERATE ON")
if RESET: print(" > RESET ON")
if TEST: print("TEST ON")
if SAVE: print(" > SAVE ON")
print()

print("sample size: "+str(size))
print("resolution: "+str(reso))

Rs = [i/reso for i in range(2,reso)]
rs = [[] for i in range(len(Rs))]
Rs_array = np.array([],dtype=np.float)
rs_array = np.array([],dtype=np.float)
cmd_strings = [[] for i in range(len(Rs))]
name_strings = [[] for i in range(len(Rs))]
# sample_strings = [[] for i in range(len(Rs))]
# data_strings = [[] for i in range(len(Rs))]
sample_strings = []
data_strings = []

n = 0
for i in range(len(Rs)):
    k = 1
    r = k/reso
    while ((Rs[i] - r < 1.0) and (r < Rs[i]*0.8)):
        Rs_array = np.append(Rs_array,[Rs[i]])
        rs_array = np.append(rs_array, [r])
        rs[i] += [r]
        cmd_strings[i] += ["./gentest.sh "+str(size)+" "+str(Rs[i])+" "+str(r)]
        name_strings[i] += ["torus_"+str(Rs[i])+"_"+str(r)]
        # sample_strings[i] += ["samples/torus_pairs_"+str(Rs[i])+"_"+str(r)+".txt"]
        # data_strings[i] += ["samples/data/torus_"+str(Rs[i])+"_"+str(r)+"/pairs_filt.txt"]
        sample_strings += ["samples/torus_pairs_"+str(Rs[i])+"_"+str(r)+".txt"]
        data_strings += ["samples/data/torus_"+str(Rs[i])+"_"+str(r)+"/pairs_filt.txt"]
        k = k+1
        r = k/reso
        n+=1
print(str(n)+" torus samples\n")

# print(Rs_array)
# print(rs_array)

if GENERATE:
    if RESET:
        try:
            subprocess.run("rm -r samples", stderr=subprocess.STDOUT, shell=True, check=True)
        except subprocess.CalledProcessError as err:
            print(err)

    try:
        subprocess.run("mkdir samples", stderr=subprocess.STDOUT, shell=True, check=True)
    except subprocess.CalledProcessError as err:
        print(err)

    count = 0
    for i in range(len(Rs)):
        for j in range(len(rs[i])):
            print("\n["+str(count)+"] "+cmd_strings[i][j])
            try:
                subprocess.run(cmd_strings[i][j], stderr=subprocess.STDOUT, shell=True, check=True)
            except subprocess.CalledProcessError as err:
                print(err)
            count += 1

if TEST:
    sampleXsample = np.array([[-1.0 for i in range(n)] for j in range(n)],dtype=np.float)
    dataXsample = np.asarray([[-1.0 for i in range(n)] for j in range(n)],dtype=np.float)
    dataXdata = np.asarray([[-1.0 for i in range(n)] for j in range(n)],dtype=np.float)
    errors = [False, False, False]

    for i in range(n):
        for j in range(n):
            try:
                p = Popen(['./bottleneck_dist', sample_strings[i], sample_strings[j]], stdin=PIPE, stdout=PIPE, stderr=PIPE)
                output, err = p.communicate(b"input data that is passed to subprocess' stdin")
                output_string = output.decode()
                sampleXsample[i][j] = float(output_string)
            except ValueError as valerr:
                errors[0] = True
                print(str(err)+" "+str(valerr))
                print(sample_strings[i]+" "+sample_strings[j])
                print(output_string)

            try:
                p = Popen(['./bottleneck_dist', data_strings[i], sample_strings[j]], stdin=PIPE, stdout=PIPE, stderr=PIPE)
                output, err = p.communicate(b"input data that is passed to subprocess' stdin")
                output_string = output.decode()
                dataXsample[i][j] = float(output_string)
            except ValueError as valerr:
                errors[1] = True
                print(str(err)+" "+str(valerr))
                print(data_strings[i]+" "+sample_strings[j])
                print(output_string)

            try:
                p = Popen(['./bottleneck_dist', data_strings[i], data_strings[j]], stdin=PIPE, stdout=PIPE, stderr=PIPE)
                output, err = p.communicate(b"input data that is passed to subprocess' stdin")
                output_string = output.decode()
                dataXdata[i][j] = float(output_string)
            except ValueError as valerr:
                errors[2] = True
                print(str(err)+" "+str(valerr))
                print(data_strings[i]+" "+data_strings[j])
                print(output_string)

    if SAVE:
        if not errors[0]:
            print('saving sampleXsample.csv')
            np.savetxt('sampleXsample.csv', sampleXsample, delimiter=',')
        if not errors[1]:
            print('saving dataXsample.csv')
            np.savetxt('dataXsample.csv', dataXsample, delimiter=',')
        if not errors[2]:
            print('saving dataXdata.csv')
            np.savetxt('dataXdata.csv', dataXdata, delimiter=',')
        print('saving major.csv')
        np.savetxt('major.csv', Rs_array, delimiter=',')
        print('saving minor.csv')
        np.savetxt('minor.csv', rs_array, delimiter=',')
