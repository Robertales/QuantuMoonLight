#!C:\Users\Gennaro\Miniconda3\envs\python\python.exe
#print("Content-Type: text/html\n")

import sys
import utils
import numpy as np
import PrototypeSelectionProblem as ps
import mysql.connector
from mysql.connector import errorcode

#dbpath= 'Iris.csv'

def callPS(databasePath):


    x_train, x_test, number_of_features, number_of_classes, number_of_total_instances=utils.prepareData(databasePath)

    number_of_solutions=500
    number_of_total_qubits=14
    # Da controllare
    #number_of_reduced_training_instances = number_of_total_qubits - math.ceil(math.log(number_of_classes,2)) - math.ceil(math.log(number_of_features,2))
    number_of_reduced_training_instances=500
    chromosomeToEvaluate,fitness=ps.runGeneticAlgorithXPS(number_of_solutions, x_train,number_of_reduced_training_instances )

    print(chromosomeToEvaluate)
    np.savetxt('C:/xampp/htdocs/quantumKNN/python/reducedTrainingPS.csv', x_train[chromosomeToEvaluate,:], delimiter=",", fmt='%s')


############# Parameters to be given in input########################
# separator is , in the file of the dataset

#databasePath = dbpath

#path='trainingDataset.csv'

#callPS(dbpath)

"""""


"""""
