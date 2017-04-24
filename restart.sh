#!/bin/bash

rm -r data
rm -r build
mkdir build
cd build
cmake ..
make
cp torus ..
cd ..
python3 torus.py
./torus
python3 plotone.py
./movie orus
