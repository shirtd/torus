#!/bin/bash
echo
echo "$ python3 torus.py 200 $1 $2"
python3 torus.py 200 $1 $2
cp torus.txt samples/torus_$1_$2.txt
cp torus_pairs.txt samples/torus_pairs_$1_$2.txt
