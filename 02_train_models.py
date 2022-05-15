import os
import pickle


RESOLUTION = 4  # interval/hour
TEST_DAY = 1


def retrieve_all_file(path, handler):
    items = os.listdir(path)
    for item in items:
        item_abpath = os.path.join(path, item)
        if os.path.isdir(item_abpath):
            retrieve_all_file(item_abpath, handler)
        elif item[-3:] == "pkl":
            with open(item, "rb") as f:
                data_dict = pickle.load(f)
            X_train = data_dict["X_train"]
            Y_train = data_dict["Y_train"]
            X_test = data_dict["X_test"]
            Y_test = data_dict["Y_test"]


if __name__ == '__main__':
    retrieve_all_file("raw_data", generate_train_set)
