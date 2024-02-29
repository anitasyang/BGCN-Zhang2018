dataset=$1
no_dropout=$2

for ((i=1; i<=50; i++))
do
    if [ "$no_dropout" == "no_dropout" ]
    then
        echo "Running with no dropout"
        python3 BGCN_main.py --dataset $dataset --no_dropout
    else
        python3 BGCN_main.py --dataset $dataset
    fi
done
