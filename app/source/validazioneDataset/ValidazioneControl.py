from app import app
import pandas as pd
from sklearn.model_selection import train_test_split


@app.route('/Validazione/', methods=['GET', 'POST'])
def valida():
    return "sei in Validazione";


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


def kFoldValidation(k, filepath):
    from app.source.validazioneDataset.kFoldValidation import cross_fold_validation
    return cross_fold_validation(filepath, k)
