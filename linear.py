import numpy as np
from numpy import linalg as la
from numpy import genfromtxt
import sys
import random

from scipy import linspace, polyval, polyfit, sqrt, stats, randn
from pylab import plot, title, show , legend

file_X = sys.argv[1]
file_Y = sys.argv[2]
TEST = False
if (len(sys.argv) >= 5):
    TEST = True
    file_test_X = sys.argv[3]
    file_test_Y = sys.argv[4]
# if (len(sys.argv) == 6):
#     title = sys.argv[5]

def grad_descent(w0, X, y):
    a = 1                   # initial step size
    w = [ w0 ]              # weights
    d = [ grad(w0,X,y) ]    # gradients
    k = 0                   # iteration count
    while True:
        # print("\tE(w["+str(k)+"]) = "+ str(E(w[k], X, y)))
        w += [ w[k] + a*d[k]*(-1) ]                         # compute wk+1 = wk - a*dk
        d += [ grad(w[k+1],X,y) ]                           # compute grad E(wk+1)
        if terminate(w, d, k, X, y):
            break                                           # terminate
        else:
            k = k + 1
            a = a_inexact(w[k-1],w[k],d[k-1],d[k])  # Barzilai-Borwein method
    print(str(k) + ' iterations.')
    return w.pop()

# termination condition(s)
def terminate(w, d, k, X, y):
    MAX_ITERATIONS = 100000
    e = 10**(-200)                                      # termination epsilon
    return ((abs(E(w[k+1], X, y) - E(w[k], X, y)) < e)  # if    |E(wk+1) - E(wk)| < e,
            or (la.norm(w[k+1] - w[k]) < e)             #       ||wk+1 - wk|| < e,
            or (la.norm(d[k+1]) < e)                    #    or ||grad E(wk+1)|| < e
            or (k >= MAX_ITERATIONS))
# E(w) = (y - Xw).T(y - Xw)
def E(w, X, y):
    return (y - X.dot(w)).dot(y - X.dot(w))

# grad E(w) = -2*X.T(y - Xw)
def grad(w, X, y):
    return -2*X.T.dot(y - X.dot(w))

# inexact line search (Barzilai-Borwein)
def a_inexact(w0, w1, d0, d1):
    return ((w1 - w0).T.dot(d1 - d0))/(la.norm(d1 - d0)**2)

# DATA IMPORT

data_string = genfromtxt(file_X, delimiter=',', dtype=str)
rows_X = data_string.shape[0]
cols_X = data_string.shape[1]

data_string_Y = genfromtxt(file_Y, delimiter=',', dtype=str)
rows_Y = data_string_Y.shape[0]

n = rows_X
m = cols_X

print('\nn = '+ str(n))
print('m = '+ str(m))
print('Y has '+str(rows_Y)+" features")

X = data_string.astype(np.float)
Y = data_string_Y.astype(np.float)
# data_matrix_T = data_matrix.T
# X = X.T

# print("\nX:")
# print(X)
print("\nY.T:")
print(Y.T)

w0 = [1 for i in range(m)]
print('\nw0: '+ str(w0))

# y = Y[i]
y = Y
print('\nrunning gradient descent...')
w = grad_descent(w0, X, y)
print('\nw:'+str(w))
print('\nE(w): '+str(E(w, X, y)))
Xw = X.dot(w)
print('\n\ty:\tXw:')
for i in range(n):
    print('\t'+ str(y[i])+'\t'+ str(Xw[i]))

if not TEST:
    ntests = 10
    tests = []
    sumsq = 0
    for i in range(ntests):
        tests += [random.randint(0,n-1)]
    for t in tests:
        T = X[t]
        print("\ntesting row "+str(t))
        R = T.dot(w)
        print("\tY["+str(t)+"] = "+str(Y[t]))
        print("\tX["+str(t)+"].dot(w) = "+str(R))
        sumsq += (Y[t] - R)**2
    print("\nsum of squares = "+str(sumsq))
else:
    print("testing file "+file_test_X+" against "+file_test_Y)
    test_data_string = genfromtxt(file_test_X, delimiter=',', dtype=str)
    test_data_string_Y = genfromtxt(file_test_Y, delimiter=',', dtype=str)
    T = test_data_string.astype(np.float)
    T_Y = test_data_string_Y.astype(np.float)
    Y_est = np.array([],dtype=float)
    sumsq = 0
    for t in range(len(T)):
        print("\ntesting row "+str(t))
        R = abs(T[t].dot(w))
        Y_est = np.append(Y_est, [R])
        print("\tY["+str(t)+"] = "+str(T_Y[t]))
        print("\tX["+str(t)+"].dot(w) = "+str(R))
        sumsq += (Y[t] - R)**2
    print("\nsum of squares = "+str(sumsq))

    print(n)
    print(len(Y_est))
    print(len(T_Y))

    t=linspace(0,n,n)
    xn = T_Y
    (ar,br)=polyfit(t,T_Y,1)
    xr=polyval([ar,br],t)
    # xr=polyval([ar,br],t)
    #compute the mean square error
    # err=sqrt(sum((xr-xn)**2)/n)

    # print('Linear regression using polyfit')
    # print('parameters: a=%.2f b=%.2f \nregression: a=%.2f b=%.2f, ms error= %.3f' % (a,b,ar,br,err))

    #matplotlib ploting
    title('estimated major radius (k=100, N=6)')
    # plot(t,x,'g.--')
    plot(t,xn,'g.--')
    plot(t,Y_est,'r.-')
    # plot(t,Y_est,'k.')
    # legend(['actual','regression','estimate'])
    legend(['actual','estimate'])

    show()
