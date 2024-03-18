'''
Copyright (C) 2019. Huawei Technologies Co., Ltd and McGill University. All rights reserved.
This program is free software; you can redistribute it and/or modify
it under the terms of the MIT License.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
MIT License for more details.
'''
# import tensorflow as tf
import tensorflow.compat.v1 as tf 
import numpy as np
from src.GNN_models import GnnModel
from src.data_partition import data_partition_fix, data_partition_random
import random
from src.utils import save_log_func
import argparse
import os
import os.path as osp
import csv
from src.flags import flags

code_path = os.path.abspath('')
FLAGS = flags()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default='citeseer', help='which dataset to use')
    parser.add_argument('--label_n_per_class', type=int, default=10, help='trial index')
    parser.add_argument('--data_partition_seed', type=int, default=101,
                        help='The seed to use split the data for trial.')
    parser.add_argument('--trial_index', type=int, default=0, help='trial index')
    parser.add_argument('--model_name', type=str, default='BGCN', help='which model we use for training (GCN or BGCN)')
    parser.add_argument('--save_log', type=lambda s: s.lower() in ['true', 't', 'yes', '1'], default=False,
                        help='Save log or not')
    parser.add_argument('--random_partition', type=lambda s: s.lower() in ['true', 't', 'yes', '1'], default=True,
                        help='Save log or not')
    parser.add_argument('--no_dropout', action='store_true', help='no dropout')
    parser.add_argument('--gpu', type=int, default=0, help='which gpu to use')

    args = parser.parse_args()
    data_partition_seed = args.data_partition_seed
    trial_index = args.trial_index
    dataset = args.dataset
    model_name = args.model_name
    save_log = args.save_log
    random_partition = args.random_partition
    label_n_per_class = args.label_n_per_class
    gpu = args.gpu

    if args.no_dropout:
        FLAGS.dropout = 0.0

    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu)

    print("Dataset: {}".format(dataset))
    print("Model: {}".format(model_name))
    print("Trial index: {}".format(trial_index))
    print("Data partition seed: {}".format(data_partition_seed))
    if save_log:
        file_name = dataset + '_' + model_name + '_softmax_trail_' + str(trial_index) + '_random_seed_' + str(
            data_partition_seed) + '.txt'
        if args.no_dropout:
            file_name = file_name.replace('.txt', '_no_dropout.txt')        
        print("Save log mode activated, training log will be saved to /log/" + file_name)

    # ==================================Set random seed for result reproduce===============================

    tf.set_random_seed(data_partition_seed)
    np.random.seed(data_partition_seed)
    random.seed(data_partition_seed)

    # =============================================Save log=================================================

    if save_log:
        save_log_func(code_path, dataset, model_name, trial_index, data_partition_seed, no_dropout=args.no_dropout)

    # =============================Load data=================================================

    dataset_dir = code_path + '' + '/data'
    if not random_partition:
        adj, features, y_train, y_val, y_test, train_mask, val_mask, test_mask, labels = data_partition_fix(
            dataset_dir=dataset_dir, dataset_name=dataset, label_n_per_class=label_n_per_class)
    elif random_partition:
        print("Random partition")
        adj, features, y_train, y_val, y_test, train_mask, val_mask, test_mask, labels = data_partition_random(
            dataset_dir=dataset_dir, dataset_name=dataset, label_n_per_class=label_n_per_class)
    else:
        "Wrong input data format"

    # ==================================Train Model===========================================
    GNN_Model = GnnModel(FLAGS, features, labels, adj, y_train, y_val, y_test, train_mask, val_mask,
                         test_mask, checkpt_name='model_1', model_name=model_name)
    GNN_Model.model_initialization()

    acc_sample_graph, avg_test_variance_on_true_label, \
        avg_test_entropy_on_true_label, test_mean, test_variance = GNN_Model.train()

    fn = f'{args.dataset}'
    if args.no_dropout:
        fn += '_no_dropout'
    fn += '.csv'
    
    # save mean and variance
    if save_log:
        # Directory to save mean and variance of predictions
        dir = code_path + '/pred'
        if not osp.exists(dir):
            os.makedirs(dir)
        mean_fn = osp.join(dir, file_name.replace('.txt', '_mean.npy'))
        variance_fn = osp.join(dir, file_name.replace('.txt', '_variance.npy'))

        np.save(mean_fn, test_mean)
        np.save(variance_fn, test_variance)

    with open(fn, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([acc_sample_graph, avg_test_variance_on_true_label, avg_test_entropy_on_true_label])
