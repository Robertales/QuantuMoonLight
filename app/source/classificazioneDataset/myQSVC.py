import csv
import time

import numpy
import pandas as pd
from matplotlib import pyplot as plt
from qiskit.circuit.library import ZFeatureMap
from qiskit.utils import algorithm_globals, QuantumInstance
from qiskit_machine_learning.algorithms import PegasosQSVC, QSVC
from qiskit_machine_learning.datasets import ad_hoc_data
from qiskit_machine_learning.kernels import QuantumKernel
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score
import numpy as np

from app.source.utils import utils
from app.source.utils.utils import createFeatureList, numberOfColumns


class myQSVC:
    def classify(pathTrain, pathTest, path_predict, backend, num_qubits):

        print(pathTrain, pathTest, path_predict)
        data_train = pd.read_csv(pathTrain)
        data_train = data_train.drop(columns='Id')  # QSVM richiede l'id e Pegasos no
        train_features = data_train.drop(columns='labels')
        train_labels = data_train["labels"].values
        data_test = pd.read_csv(pathTest)
        data_test = data_test.drop(columns='Id')
        test_features = data_test.drop(columns='labels')
        test_labels = data_test["labels"].values

        toAdd = ""
        num_col = utils.numberOfColumns(path_predict)
        for j in range(1, num_col + 1):
            if j == num_col:
                toAdd += "feature" + str(j) + "\n"
                continue
            toAdd += "feature" + str(j) + ","

        with open(path_predict, "r") as f:
            contents = f.readlines()

        contents.insert(0, toAdd)

        with open(path_predict, "w") as f:
            contents = "".join(contents)
            f.write(contents)

        prediction_data = np.genfromtxt(path_predict, delimiter=',')
        prediction_data = np.delete(prediction_data, 0, axis=0)

        test_features = test_features.to_numpy()  # Pegasos.fit accetta numpy array e non dataframe
        train_features = train_features.to_numpy()

        result = {}
        algorithm_globals.random_seed = 12345

        feature_map = ZFeatureMap(feature_dimension=num_qubits, reps=1)
        qkernel = QuantumKernel(feature_map=feature_map, quantum_instance=QuantumInstance(backend))
        qsvc = QSVC(quantum_kernel=qkernel)

        # training
        print("Running...")
        start_time = time.time()
        qsvc.fit(train_features, train_labels)
        training_time = time.time() - start_time
        print("Train effettuato in " + str(training_time))

        # test
        start_time = time.time()
        test_prediction = qsvc.predict(test_features)
        testing_time = time.time() - start_time
        accuracy = accuracy_score(test_labels, test_prediction)
        precision = precision_score(test_labels, test_prediction, average="weighted", zero_division=0)
        recall = recall_score(test_labels, test_prediction, average="weighted")
        f1 = f1_score(test_labels, test_prediction, average="weighted")
        result["f1"] = f1
        result["testing_precision"] = precision
        result["testing_recall"] = recall
        result["testing_accuracy"] = accuracy

        # prediction
        start_time = time.time()
        predicted_labels = qsvc.predict(prediction_data)
        total_time = time.time() - start_time
        print("Prediction effettuata in " + str(total_time))
        result["predicted_labels"] = np.array(predicted_labels)

        result["total_time"] = str(testing_time + training_time)[0:6]
        result["training_time"] = str(training_time)[0:6]

        labels = np.unique(train_labels)
        occurrences = {}
        for i in train_labels.data:
            if i in occurrences:
                occurrences[i] += 1
            else:
                occurrences[i] = 1
        sizes = occurrences.values()

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()

        return result
