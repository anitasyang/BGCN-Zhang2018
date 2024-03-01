#! /bin/bash

list=("citeseer" "cora" "pubmed")

for dataset in "${list[@]}"
do
    echo "Running $dataset"
    for ((i=1; i<=50; i++))
    do
        echo "num iter: $i"
        # Generate a random integer between 1 and 500
        random_int=$((1 + RANDOM % 500))
        echo "Partition seed: $random_int"
        python3 BGCN_main.py --dataset $dataset --no_dropout --random_partition t --save_log t --data_partition_seed $random_int
        python3 BGCN_main.py --dataset $dataset --random_partition t --save_log t --data_partition_seed $random_int
    done
done
