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


@app.route('/Preprocessing/', methods=['GET', 'POST'])
def preprocessing():
    print('Request send on ')
    ROOT_DIR = pathlib.Path(__file__).cwd()
    # log.log()
    file = request.files.get('userfile')
    ext_ok = ['txt', 'csv', 'data']
    temp = file.filename
    extension = temp.split('.')[-1]
    print(extension)
    if not ext_ok.__contains__(extension):
        return 'Il file ha un estensione non ammessa!'

    if file is None:
        return 'No Train set uploaded'

    uploaddir = ROOT_DIR / 'upload_dataset/'
    userfile_name = file.filename
    userpath = uploaddir / userfile_name

    if file.content_length > 80000000:
        return 'Il file è troppo grande!'
    prototypeSelection = request.form.get('reduce1')
    featureExtraction = request.form.get('reduce')
    autosplit = request.form.get('test')

    file.save(userpath)
    print("Dataset: ", file.filename)
    numCols = utils.numberOfColumns(userpath)
    # Recupero le impostazioni dell'utente, cioè
    # quali operazioni vuole effettuare e, in caso di QSVM, anche il token
    print("AutoSplit: ", autosplit)
    numRawsPS = 200  # numero di righe dopo la Prototype Selection con GA
    print("Prototype Selection: ", prototypeSelection)
    numColsFE = 2  # numero di colonne dopo la Feature Extraction con PCA
    print("Feature Extraction: ", featureExtraction)

    features = utils.createFeatureList(numCols - 1)
    features1 = features.copy()
    features1.append("labels")
    featuresPCA = utils.createFeatureList(numColsFE)
    print("\n")

    # spilt and PS
    if autosplit and prototypeSelection and not featureExtraction:
        print("I'm doing Prototype Selection ...")
        addAttribute.addAttribute(userpath)  # copia il dataset dell'utente (con il suo path preso dal DB),
        # con  l'aggiunta degli attributi in 'featureDataset.csv'
        train_testSplit.splitDataset('featureDataset.csv')  # crea 'Data_training.csv' e 'Data_testing.csv'
        callPS.callPS('Data_training.csv')  # crea 'reducedTrainingPS.csv'
        addAttribute.addAttribute(
            'reducedTrainingPS.csv')  # modifica 'featureDataset.csv' con le istanze create da 'reducedTrainingPS.csv'
        aggId.addId('featureDataset.csv')
        aggIdTesting.aggIdTesting()

    # split and PCA
    elif autosplit and not prototypeSelection and featureExtraction:
        print("I'm doing Feature Extraction ...")
        addAttribute.addAttribute(file)
        train_testSplit.splitDataset('featureDataset.csv')

        featureExtractionPCA.featureExtractionPCA2('Data_training.csv', features1)  # do pca of training
        featureExtractionPCA.featureExtractionPCA2('Data_testing.csv', features1)  # do pca of testing
        addClass.addClassPCAtraining('Data_training.csv')  # add class to pca dataset training
        addClass.addClassPCAtesting('Data_testing.csv')  # add class to pca dataset training

    # Split PCA and PS:
    elif autosplit and prototypeSelection and featureExtraction:
        print("I'm doing Protype Selection and feature extraction ")
        # ps
        addAttribute.addAttribute(file)
        train_testSplit.splitDataset('featureDataset.csv')
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
