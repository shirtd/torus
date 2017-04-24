#!/bin/bash

rm -r build
mkdir build
cd build
cmake ..
make
cp torus ..
cd ..
