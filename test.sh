#!/bin/bash

rm -r build
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Debug ..
make
cp torus ..
cd ..
valgrind --leak-check=full ./torus
# valgrind --leak-check=full --show-leak-kinds=all ./torus
