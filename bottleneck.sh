#!/bin/bash

# echo "$1, $2"
# ./bottleneck_dist "data/$1_0/0pair.txt" "data/$2_0/0pair.txt"
# ./bottleneck_dist "data/$1_0/1pair.txt" "data/$2_0/1pair.txt"
# ./bottleneck_dist "data/$1_0/2pair.txt" "data/$2_0/2pair.txt"
# # ./bottleneck_dist "data/$1_0/3pair.txt" "data/$2_0/3pair.txt"
# # ./bottleneck_dist "data/$1_0/4pair.txt" "data/$2_0/4pair.txt"
# # ./bottleneck_dist "data/$1_0/5pair.txt" "data/$2_0/5pair.txt"
# echo
# echo "$1, $3"
# ./bottleneck_dist "data/$1_0/0pair.txt" "data/$3_0/0pair.txt"
# ./bottleneck_dist "data/$1_0/1pair.txt" "data/$3_0/1pair.txt"
# ./bottleneck_dist "data/$1_0/2pair.txt" "data/$3_0/2pair.txt"
# # ./bottleneck_dist "data/$1_0/3pair.txt" "data/$3_0/3pair.txt"
# # ./bottleneck_dist "data/$1_0/4pair.txt" "data/$3_0/4pair.txt"
# # ./bottleneck_dist "data/$1_0/5pair.txt" "data/$3_0/5pair.txt"
# echo
# echo "$2, $3"
# ./bottleneck_dist "data/$2_0/0pair.txt" "data/$3_0/0pair.txt"
# ./bottleneck_dist "data/$2_0/1pair.txt" "data/$3_0/1pair.txt"
# ./bottleneck_dist "data/$2_0/2pair.txt" "data/$3_0/2pair.txt"
# # ./bottleneck_dist "data/$2_0/3pair.txt" "data/$3_0/3pair.txt"
# # ./bottleneck_dist "data/$2_0/4pair.txt" "data/$3_0/4pair.txt"
# # ./bottleneck_dist "data/$2_0/5pair.txt" "data/$3_0/5pair.txt"
# echo

echo "$1, $2"
./bottleneck_dist "data/$1_0/pairs.txt" "data/$2_0/pairs.txt"
echo
echo "$1, $3"
./bottleneck_dist "data/$1_0/pairs.txt" "data/$3_0/pairs.txt"
echo
echo "$2, $3"
./bottleneck_dist "data/$2_0/pairs.txt" "data/$3_0/pairs.txt"
echo
