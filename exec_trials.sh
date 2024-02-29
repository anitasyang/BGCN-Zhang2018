#! /bin/bash

list=("cora" "citeseer" "pubmed")

for dataset in "${list[@]}"
do
    echo "Running $dataset"
    for ((i=1; i<=50; i++))
    do
        echo "num iter: $i"
        python3 BGCN_main.py --dataset $dataset --no_dropout
        python3 BGCN_main.py --dataset $dataset
    done
done
