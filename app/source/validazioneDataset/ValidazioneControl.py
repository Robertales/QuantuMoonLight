import pathlib

from flask import request

from app import app
import pandas as pd
from sklearn.model_selection import train_test_split

from app.source.utils import addAttribute
from app.source.validazioneDataset import train_testSplit


def valida(userpath, autosplit, kFold):
    # VALIDAZIONE FATTA BELLLA
    if autosplit:
        addAttribute.addAttribute(userpath)  # copia il dataset dell'utente (con il suo path preso dal DB),
        # con  l'aggiunta degli attributi in 'featureDataset.csv'
        train_testSplit.splitDataset('featureDataset.csv')  # crea 'Data_training.csv' e 'Data_testing.csv'
    if kFold:
        kFoldValidation(userpath)


def simpleSplit(filepath, test_size=20):
    data = pd.read_csv(filepath)
    X = data

    X_train, X_test = train_test_split(X, test_size)

    print("\nX_train:\n")
    print(X_train.head())
    print(X_train.shape)

    print("\nX_test:\n")
    print(X_test.head())
    print(X_test.shape)

    return X_train.to_csv('Data_training.csv', index=False), X_test.to_csv('Data_testing.csv', index=False)


def kFoldValidation(filepath, k=10):
    from app.source.validazioneDataset.kFoldValidation import cross_fold_validation
    return cross_fold_validation(filepath, k)
