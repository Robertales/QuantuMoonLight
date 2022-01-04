from flask import request

from app import app
import numpy as np
import pandas as pd
import os
import pathlib
from app.source.utils import utils, addAttribute, aggId, aggIdTesting, addClass
from app.source.preprocessingDataset import PrototypeSelectionProblem as ps, callPS, featureExtractionPCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from app.source.validazioneDataset import train_testSplit


def preprocessing(userpath: str, prototypeSelection: bool, featureExtraction: bool, numRawsPS: int, numColsFE: int):
    """

    :param userpath: strings that points to the location di file to be preprocessed is stored in
    :param prototypeSelection: boolean flag that indicated whether the user wants to execute a prototype Selection or not
    :param featureExtraction:boolean flag that indicated whether the user wants to execute a feature Extraction or not
    :param numRawsPS: number of rows the prototype selection should reduce the dataset to
    :param numColsFE:number of columns the feature extraction should reduce the dataset to
    :return: ancora non deciso
    """
    numCols = utils.numberOfColumns(userpath)
    features = utils.createFeatureList(numCols - 1)
    features1 = features.copy()
    features1.append("labels")
    featuresPCA = utils.createFeatureList(numColsFE)
    print("\n")

    # PS with GA
    if prototypeSelection and not featureExtraction:
        print("I'm doing Prototype Selection ...")

        callPS.callPS('Data_training.csv')  # crea 'reducedTrainingPS.csv'
        addAttribute.addAttribute(
            'reducedTrainingPS.csv')  # modifica 'featureDataset.csv' con le istanze create da 'reducedTrainingPS.csv'
        aggId.addId('featureDataset.csv')
        aggIdTesting.aggIdTesting()

    # FE with PCA
    elif featureExtraction and not prototypeSelection:
        print("I'm doing Feature Extraction ...")

        featureExtractionPCA.featureExtractionPCA2('Data_training.csv', features1)  # do pca of training
        featureExtractionPCA.featureExtractionPCA2('Data_testing.csv', features1)  # do pca of testing
        addClass.addClassPCAtraining('Data_training.csv')  # add class to pca dataset training
        addClass.addClassPCAtesting('Data_testing.csv')  # add class to pca dataset training

    # FE and PS:
    elif prototypeSelection and featureExtraction:
        print("I'm doing Protype Selection and feature extraction ")

        # ps
        callPS.callPS('Data_training.csv')
        addAttribute.addAttribute_to_ps('reducedTrainingPS.csv')

        # pca
        featureExtractionPCA.featureExtractionPCA2('reducedTrainingPS_attribute.csv',
                                                   features1)  # do pca of PS training
        featureExtractionPCA.featureExtractionPCA2('Data_testing.csv', features1)  # do pca of testing
        addClass.addClassPCAtraining('Data_training.csv')  # add class to pca dataset training
        addClass.addClassPCAtesting('Data_testing.csv')  # add class to pca dataset training

    return "Preprocessing fatto"


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
