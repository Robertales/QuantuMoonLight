#!C:\Users\Gennaro\Miniconda3\envs\python\python.exe
print("Content-Type: text/html\n")

from openpyxl import Workbook
from openpyxl.utils import get_column_letter

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from sklearn.neighbors import KNeighborsClassifier

def classifier(number_of_training_instances):
    c = KNeighborsClassifier(n_neighbors =number_of_training_instances, weights='distance')
    return c

### fitness for scikit-learn knn pesato #####
def test(x_train, x_test, list_of_instances):
    neigh = classifier(len(list_of_instances))
    neigh.fit(x_train[list_of_instances, :-2], x_train[list_of_instances,-1])
    accuracy=neigh.score(x_test[:, :-2], x_test[:,-1])
    return accuracy


def prepareData(databasePath):

    ##### READ dataset ############################################################

    data = pd.read_csv(databasePath)

    # preprocessing
    # replace categorical data
    # da modificare
    #dictionaryCat = {"class": {"Iris-setosa": 0, "Iris-versicolor": 1, "Iris-virginica": 2}}
    #data.replace(dictionaryCat, inplace=True)

    # print(data.head())

    # detecting classes
    target = data.values[:, -1]
    classes = np.unique(target)
    number_of_classes = len(classes)
    number_of_features = len(data.values[1]) - 1

    # print(str(number_of_classes) + " " + str(number_of_features))

    # split dei dati
    random_state_value = 3
    x_train, x_test = train_test_split(data.values, test_size=0.25, random_state=random_state_value, stratify=target)

    # split dei dati di training
    # x_train ,x_valid = train_test_split(x_train,test_size=0.10)

    number_of_total_instances = len(x_train)

    return x_train, x_test, number_of_features, number_of_classes, number_of_total_instances


def printRunResults(indexR, pop, stats, hof, logbook):
    resultString="Run " + indexR + "\n" + "Number of evaluations " + logbook.select('nevals')[-1] + "\nBest fitness " + hof[0].fitness.values[0] + "\nBest individual " + hof[0]
    return resultString


def writeTxt(fileName, list_values):
    f = open(fileName, "w+")
    for c in list_values:
      f.write(str(c)+"\n")

def writeXls(fileName, generations, evaluations, bestfits, times):
    wb = Workbook()
    ws1 = wb.active

    ws1.cell(column=1, row=1, value="Number of Generations")
    ws1.cell(column=2, row=1, value="Number of Evaluations")
    ws1.cell(column=3, row=1, value="Best Fitness Value")
    ws1.cell(column=4, row=1, value="Time in seconds")


    row = 2
    for g in generations:
        ws1.cell(column=1, row=row, value=g)
        row += 1

    row = 2
    for g in evaluations:
        ws1.cell(column=2, row=row, value=g)
        row += 1

    row = 2
    for g in bestfits:
        ws1.cell(column=3, row=row, value=g)
        row += 1

    row = 2
    for g in times:
        ws1.cell(column=4, row=row, value=g)
        row += 1

    wb.save(filename = fileName)
