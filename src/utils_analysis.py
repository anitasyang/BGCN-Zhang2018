import numpy as np


# def calculate_variance(data):
#     mean = np.mean(data, axis=0)
#     diff = data - mean
#     squared_diff = np.square(diff)
#     variance = np.sum(squared_diff, axis=0) / len(data)
#     return variance


def calculate_entropy(data):
    prob = data / np.sum(data, axis=0)
    log_prob = np.log(prob)
    entropy = -np.sum(prob * log_prob, axis=0)
    return entropy


def calculate_mean_and_variance(data):
    mean = np.mean(data, axis=0)
    diff = data - mean
    squared_diff = np.square(diff)
    variance = np.sum(squared_diff, axis=0) / len(data)
    return mean, variance
