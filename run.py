import subprocess

program = "./tdsa-igl"
wav = "wavs/kida.wav"
dim = 4

print("\nfile: " + wav)
print(" > dim = "+ str(dim))

errors1 = 0;
print("\nSTARTING ALPHA BY EPSILON")
subprocess.run('date +"%T"', shell=True, check=True)
for e in range(200):
    print("\n > STARTING e = " + str(e))
    subprocess.run('date +"%T"', shell=True, check=True)
    for a in range(e,200):
        _e = 5*e/1000
        _a = 5*a/1000
        string = program+" "+wav+" "+str(_e)+" "+str(_a)+" "+str(dim);
        print("\n  : > RUNNING "+program+" "+wav+" "+str(_e)+" "+str(_a)+" "+str(dim))
        try:
            out = subprocess.run(string, stderr=subprocess.STDOUT, shell=True, check=True)
        except subprocess.CalledProcessError:
            errors1 += 1
            print("\n -------- ERROR -------- ")
            print(out)
            print(" _______________________ \n")
        print("  :  _ DONE ("+str(_e)+", "+str(_a)+")")
    print("\n  _ DONE e = " + str(e))
    subprocess.run('date +"%T"', shell=True, check=True)
print("\nDONE alpha/epsilon ("+ str(errors1) + "errors )")

errors2 = 0;
print("\nSTARTING EPSILON BY ALPHA")
subprocess.run('date +"%T"', shell=True, check=True)
for a in range(200):
    print("\n > STARTING a = " + str(a))
    subprocess.run('date +"%T"', shell=True, check=True)
    for e in range(a):
        _e = 5*e/1000
        _a = 5*a/1000
        string = program+" "+wav+" "+str(_e)+" "+str(_a)+" "+str(dim);
        print("\n  : > RUNNING "+program+" "+wav+" "+str(_e)+" "+str(_a)+" "+str(dim))
        try:
            out = subprocess.run(string, stderr=subprocess.STDOUT, shell=True, check=True)
        except subprocess.CalledProcessError:
            errors2 += 1
            print("\n -------- ERROR -------- ")
            print(out)
            print(" _______________________ \n")
        print("  :  _ DONE ("+str(_e)+", "+str(_a)+")")
    print("\n  _ DONE a = " + str(a))
    subprocess.run('date +"%T"', shell=True, check=True)
print("\nDONE epsilon/alpha ("+ str(errors2) + "errors )")
errors = errors1 + errors2
print("DONE ("+str(errors)+" total)")
subprocess.run('date +"%T"', shell=True, check=True)
