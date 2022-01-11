import numpy as np
import os
import pandas as pd
import pathlib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


def callFeatureExtraction(
    path: pathlib.Path,
    output: pathlib.Path,
    features: list,
    n_components=2,
):
    """
    This function executes the Feature Extraction on the given dataset

    :param path: path to the location of the dataset that is going to be reduced with FE
    :param output: path to the location of the dataset preprocessed with FE
    :param features: list that specify the labels of the dataset input
    :param n_components: number of new columns
    :return: string that points to the location of the dataset preprocessed with FE
    :rtype: str
    """
    dataPath = path.parent
    print("Into callFeatureExtraction...")
    f = pd.read_csv(path)
    keep_col = features
    new_f = f[keep_col]
    new_f.to_csv(dataPath / "tempPCA.csv", index=False)

    dataset = pd.read_csv(dataPath / "tempPCA.csv")

    X = dataset.drop("labels", 1)

    y = dataset["labels"]
    # print(dataset.head())
    # print(y)

    # Splitting the dataset into the Training set and Test set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0
    )
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    pca = PCA(n_components)
    X_train = pca.fit_transform(X_train)
    X_test = pca.transform(X_test)

    explained_variance = pca.explained_variance_ratio_
    # print(explained_variance)

    z = np.concatenate((X_train, X_test))

    # write csv data

    # nuovo salvataggio, da testare
    pathFileYourPCA = pathlib.Path(__file__).parent
    pathFileYourPCA = pathFileYourPCA / output
    # print("pathFileYourPCA :", pathFileYourPCA)
    np.savetxt(pathFileYourPCA.__str__(), z, delimiter=",", fmt="%s")

    os.remove(dataPath / "tempPCA.csv")

    return pathFileYourPCA.__str__()


def extractFeatureForPrediction(
    path: pathlib.Path, output: pathlib.Path, n_components=2
):
    """
    This function executes the Feature Extraction on the doPrediction

    :param path: path to the location of the dataset that is going to be reduced with FE
    :param output: path to the location of the dataset preprocessed with FE
    :param n_components: number of new columns
    :return: string that points to the location of the dataset preprocessed with FE
    :rtype: str
    """
    dataPath = path.parent
    print("Into extractFeatureForPrediction...")
    f = pd.read_csv(path)
    f.to_csv(dataPath / "tempPCA.csv", index=False)
    dataset = pd.read_csv((dataPath / "tempPCA.csv").__str__())
    X = dataset.drop("labels", 1)
    y = dataset["labels"]

    # Splitting the dataset into the Training set and Test set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0
    )
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    pca = PCA(n_components)
    X_train = pca.fit_transform(X_train)
    X_test = pca.transform(X_test)

    z = np.concatenate((X_train, X_test))

    # salvataggio
    pathFileYourPCA = pathlib.Path(__file__).parent
    pathFileYourPCA = pathFileYourPCA / output
    # print("pathFileYourPCA :", pathFileYourPCA)
    np.savetxt(pathFileYourPCA.__str__(), z, delimiter=",", fmt="%s")

    os.remove(dataPath / "tempPCA.csv")

    return pathFileYourPCA.__str__()
