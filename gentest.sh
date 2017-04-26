#!/bin/bash
size=50
if [ "$#" -eq 3 ]; then
    size=$1
    R=$2
    r=$3
else
    R=$1
    r=$2
fi
./gensample.sh $size $R $r
echo
./testsample.sh $R $r
