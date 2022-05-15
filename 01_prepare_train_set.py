import pandas as pd
import os
import pickle
import numpy as np

from training_cofig import *


def convert_norm_idx(time_str):
    time_list = time_str.split(":")
    hh, mm = int(time_list[0]), int(time_list[1])
    interval_idx = (hh * 60 + mm) // 15
    return interval_idx / 96


def generate_train_set(filepath):
    df = pd.read_csv(filepath, index_col=0)
    norm_idx = df["time"].map(convert_norm_idx)
    norm_power = df["power in kW"] / df["power in kW"].max()
    train_data = np.stack([norm_idx.to_numpy(), norm_power.to_numpy()], axis=1)[:-7 * 24 * 4]
    X_train = np.stack(
        [train_data[i: i + INPUT_LENGTH] for i in range(train_data.shape[0] - INPUT_LENGTH - OUTPUT_LENGTH)],
        axis=0
    )
    Y_train = np.stack(
        [train_data[i + INPUT_LENGTH: i + INPUT_LENGTH + OUTPUT_LENGTH][:, 1] for i in range(train_data.shape[0] - INPUT_LENGTH - OUTPUT_LENGTH)],
        axis=0
    )
    test_data = np.stack([norm_idx.to_numpy(), norm_power.to_numpy()], axis=1)[-7 * 24 * 4 - INPUT_LENGTH:]
    X_test = np.stack(
        [test_data[i: i + INPUT_LENGTH] for i in range(test_data.shape[0] - INPUT_LENGTH - OUTPUT_LENGTH)], axis=0)
    Y_test = np.stack(
        [test_data[i + INPUT_LENGTH: i + INPUT_LENGTH + OUTPUT_LENGTH][:, 1] for i in range(test_data.shape[0] - INPUT_LENGTH - OUTPUT_LENGTH)],
        axis=0
    )
    return {"X_train": X_train, "Y_train": Y_train, "X_test": X_test, "Y_test": Y_test}


def retrieve_all_file(path, handler):
    items = os.listdir(path)
    for item in items:
        item_abpath = os.path.join(path, item)
        if os.path.isdir(item_abpath):
            retrieve_all_file(item_abpath, handler)
        elif item[-3:] == "csv":
            data_dict = handler(os.path.join(path, item))
            with open(os.path.join(path, item[:-3] + "pkl"), "wb") as f:
                pickle.dump(data_dict, f)


if __name__ == '__main__':
    retrieve_all_file("raw_data", generate_train_set)
