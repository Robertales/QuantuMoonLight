from app import app
import numpy as np
import pandas as pd
import os
import pathlib
from app.source.utils import utils
from app.source.preprocessingDataset import PrototypeSelectionProblem as ps
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


@app.route('/Preprocessing/', methods=['GET', 'POST'])
def preprocessing():
    return "sei in Preprocessing";


def featureExtraction(path, features, n_components=2):
    f = pd.read_csv(path)
    keep_col = features
    new_f = f[keep_col]
    new_f.to_csv("tempPCA.csv", index=False)

    dataset = pd.read_csv('tempPCA.csv')

    X = dataset.drop('labels', 1)

    y = dataset['labels']
    print(dataset.head())
    print(y)

    # Splitting the dataset into the Training set and Test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    pca = PCA(n_components)
    X_train = pca.fit_transform(X_train)
    X_test = pca.transform(X_test)

    explained_variance = pca.explained_variance_ratio_
    print(explained_variance)

    z = np.concatenate((X_train, X_test))

    # write csv data
    if not os.path.exists('C:/xampp/htdocs/quantumKNN/python/yourPCA.csv'):
        np.savetxt('C:/xampp/htdocs/quantumKNN/python/yourPCA.csv', z, delimiter=",", fmt='%s')
    else:
        np.savetxt('C:/xampp/htdocs/quantumKNN/python/yourPCA1.csv', z, delimiter=",", fmt='%s')
    # print(z)
    return z

    # nuovo salvataggio, da testare
    # pathFileYourPCA = pathlib.Path(__file__).parents[3]
    # pathFileYourPCA = pathFileYourPCA / 'yourPCA.csv'
    # np.savetxt(pathFileYourPCA.__str__(), z, delimiter=",", fmt='%s')
    # return pathFileYourPCA.__str__()


def prototypeSelection(path, number_of_reduced_training_instances=10):
    x_train, x_test, number_of_features, number_of_classes, number_of_total_instances = utils.prepareData(path)

    number_of_solutions = 500
    chromosomeToEvaluate, fitness = ps.runGeneticAlgorithXPS(number_of_solutions, x_train,
                                                             number_of_reduced_training_instances)

    print(chromosomeToEvaluate)
    pathFileReducedTrainingPS = pathlib.Path(__file__).parents[3]
    pathFileReducedTrainingPS = pathFileReducedTrainingPS / 'reducedTrainingPS.csv'

    np.savetxt(pathFileReducedTrainingPS.__str__(), x_train[chromosomeToEvaluate, :], delimiter=",", fmt='%s')
    return pathFileReducedTrainingPS.__str__()


def prototypeSelectionAI(path):
    return path


def featureExtractionAI(path, features):
    return path
