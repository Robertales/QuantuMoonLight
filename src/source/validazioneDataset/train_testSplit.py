from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


def splitDataset(filename: str):
    """
    This function splits the dataset in training set and testing set in order to be consistent on the comparisons

    :param filename: string that points to the location of the dataset that will be split into
    :return: the dataset training set 'Data_training.csv' and the dataset testing set 'Data_testing.csv'
    :rtype: (str,str)
    """

    data = pd.read_csv(filename)
    X = data

    X_train, X_test = train_test_split(X, test_size=0.20)

    pathData = Path(filename).parent
    print("\nX_train:\n")
    print(X_train.head())
    print(X_train.shape)

    print("\nX_test:\n")
    print(X_test.head())
    print(X_test.shape)

    return X_train.to_csv(
        pathData / "Data_training.csv", index=False
    ), X_test.to_csv(pathData / "Data_testing.csv", index=False)
