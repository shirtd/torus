#!/bin/bash
size=50
echo
if [ "$#" -eq 3 ]; then
    size=$1
    R=$2
    r=$3
else
    R=$1
    r=$2
fi
echo "$ python3 torus.py $size $R $r"
python3 torus.py $size $R $r
cp torus.txt samples/torus_"$R"_"$r".txt
cp torus_pairs.txt samples/torus_pairs_"$R"_"$r".txt
