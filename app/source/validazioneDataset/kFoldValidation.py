import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import KFold



filename="temp/god_class.csv"
split=10


def cross_fold_validation(filename, split):

    dataset = pd.read_csv(filename)
    X = dataset

    kf= KFold(n_splits=split)
    kf.get_n_splits(X)

    for train_index,test_index in kf.split(X):
        print("TRAIN:", train_index, "TEST:", test_index)

        with open(filename) as csvfile:
            readCSV = list(csv.reader(csvfile, delimiter=','))

            if not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/training/training_fold_1.csv'):
                for number in range(len(train_index)):
                    row_you_want = readCSV[train_index[number]]
                    with open('venv/10-kfolds/training/training_fold_1.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)
            elif not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/training/training_fold_2.csv'):
                for number in range(len(train_index)):
                    row_you_want = readCSV[train_index[number]]
                    with open('venv/10-kfolds/training/training_fold_2.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)
            elif not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/training/training_fold_3.csv'):
                for number in range(len(train_index)):
                    row_you_want = readCSV[train_index[number]]
                    with open('venv/10-kfolds/training/training_fold_3.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)
            elif not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/training/training_fold_4.csv'):
                for number in range(len(train_index)):
                    row_you_want = readCSV[train_index[number]]
                    with open('venv/10-kfolds/training/training_fold_4.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)
            elif not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/training/training_fold_5.csv'):
                for number in range(len(train_index)):
                    row_you_want = readCSV[train_index[number]]
                    with open('venv/10-kfolds/training/training_fold_5.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)

            elif not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/training/training_fold_6.csv'):
                for number in range(len(train_index)):
                    row_you_want = readCSV[train_index[number]]
                    with open('venv/10-kfolds/training/training_fold_6.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)
            elif not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/training/training_fold_7.csv'):
                for number in range(len(train_index)):
                    row_you_want = readCSV[train_index[number]]
                    with open('venv/10-kfolds/training/training_fold_7.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)
            elif not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/training/training_fold_8.csv'):
                for number in range(len(train_index)):
                    row_you_want = readCSV[train_index[number]]
                    with open('venv/10-kfolds/training/training_fold_8.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)

            elif not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/training/training_fold_9.csv'):
                for number in range(len(train_index)):
                    row_you_want = readCSV[train_index[number]]
                    with open('venv/10-kfolds/training/training_fold_9.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)
            elif not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/training/training_fold_10.csv'):
                for number in range(len(train_index)):
                    row_you_want = readCSV[train_index[number]]
                    with open('venv/10-kfolds/training/training_fold_10.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)

            #-------------------------------------------create testing folds

            if not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/testing/testing_fold_1.csv'):
                for number in range(len(test_index)):
                    row_you_want = readCSV[test_index[number]]
                    with open('venv/10-kfolds/testing/testing_fold_1.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)
            elif not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/testing/testing_fold_2.csv'):
                for number in range(len(test_index)):
                    row_you_want = readCSV[test_index[number]]
                    with open('venv/10-kfolds/testing/testing_fold_2.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)
            elif not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/testing/testing_fold_3.csv'):
                for number in range(len(test_index)):
                    row_you_want = readCSV[test_index[number]]
                    with open('venv/10-kfolds/testing/testing_fold_3.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)
            elif not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/testing/testing_fold_4.csv'):
                for number in range(len(test_index)):
                    row_you_want = readCSV[test_index[number]]
                    with open('venv/10-kfolds/testing/testing_fold_4.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)
            elif not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/testing/testing_fold_5.csv'):
                for number in range(len(test_index)):
                    row_you_want = readCSV[test_index[number]]
                    with open('venv/10-kfolds/testing/testing_fold_5.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)

            elif not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/testing/testing_fold_6.csv'):
                for number in range(len(test_index)):
                    row_you_want = readCSV[test_index[number]]
                    with open('venv/10-kfolds/testing/testing_fold_6.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)
            elif not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/testing/testing_fold_7.csv'):
                for number in range(len(test_index)):
                    row_you_want = readCSV[test_index[number]]
                    with open('venv/10-kfolds/testing/testing_fold_7.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)
            elif not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/testing/testing_fold_8.csv'):
                for number in range(len(test_index)):
                    row_you_want = readCSV[test_index[number]]
                    with open('venv/10-kfolds/testing/testing_fold_8.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)
            elif not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/testing/testing_fold_9.csv'):
                for number in range(len(test_index)):
                    row_you_want = readCSV[test_index[number]]
                    with open('venv/10-kfolds/testing/testing_fold_9.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)
            elif not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/testing/testing_fold_10.csv'):
                for number in range(len(test_index)):
                    row_you_want = readCSV[test_index[number]]
                    with open('venv/10-kfolds/testing/testing_fold_10.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)

    return 0

"""""
            if not os.path.exists('C:/xampp/htdocs/quantumKNN/python/venv/10-kfolds/testing/testing_fold_1.csv'):
                for number0 in range(len(test_index)):
                    row_you_want = readCSV[test_index[number0]]
                    with open('venv/10-kfolds/testing/testing_fold_1.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)

            else:
                for number0 in range(len(test_index)):
                    row_you_want = readCSV[test_index[number0]]
                    with open('venv/10-kfolds/testing/testing_fold_2.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(row_you_want)
"""""
print(cross_fold_validation(filename,split))





""""
    X_train, X_test = train_test_split(X, test_size=20)

    print("\nX_train:\n")
    print(X_train.head())
    print(X_train.shape)

    print("\nX_test:\n")
    print(X_test.head())
    print(X_test.shape)
"""""





    #return X_train.to_csv('Data_training.csv', index=False), X_test.to_csv('Data_testing.csv', index=False)

