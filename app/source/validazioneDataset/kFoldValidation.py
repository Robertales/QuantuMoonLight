import pandas as pd
import csv
import os
from sklearn.model_selection import KFold


def cross_fold_validation(userpath, k):
    """
    This function is a data partitioning strategy so that you can effectively use
    your dataset to build a more generalized project.
    :param userpath: string that points to the location of the dataset that is going to be validated
    :param k: number of groups that a given data sample will be split into
    :return: to be decided
    """
    dataset = pd.read_csv(userpath)

    kf = KFold(n_splits=k)
    kf.get_n_splits(dataset)
    x = 1
    for train_index, test_index in kf.split(dataset):
        print("TRAIN:", train_index)
        print("TEST:", test_index)
        print(x)
        stringaTrain = "training_fold_{}.csv".format(x)
        stringaTest = "testing_fold_{}.csv".format(x)
        x = x + 1

        with open(userpath) as csvfile:
            readCSV = list(csv.reader(csvfile, delimiter=','))

            # create training folds
            for number in range(len(train_index)):
                row_you_want = readCSV[train_index[number]]
                with open(stringaTrain, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(row_you_want)

            # create testing folds
            for number in range(len(test_index)):
                row_you_want = readCSV[test_index[number]]
                with open(stringaTest, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(row_you_want)

    return 0
