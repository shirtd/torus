#!/bin/bash
echo
if [ "$#" -eq 0 ]; then
    echo "$ python3 torus.py"
    python3 torus.py
else
    echo "$ python3 torus.py $1"
    python3 torus.py $1
fi
echo
if [ "$#" -eq 1 ]; then
    echo "$ ./torus torus 2"
    ./torus torus 2
else
    echo "$ ./torus torus $2"
    ./torus torus $2
fi
echo
echo "$ python3 plotone.py torus 10 10"
python3 plotone.py torus 10 10
echo
echo "$ ./movie torus"
./movie torus
