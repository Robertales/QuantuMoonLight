import csv
import math
import time
import traceback

import pandas as pd
from qiskit import QuantumCircuit
from qiskit.algorithms.optimizers import COBYLA, SLSQP, ADAM, GradientDescent, L_BFGS_B
from qiskit.circuit.library import ZFeatureMap, ZZFeatureMap, RealAmplitudes
from qiskit.utils import algorithm_globals, QuantumInstance
from qiskit_machine_learning.algorithms import PegasosQSVC, NeuralNetworkClassifier, NeuralNetworkRegressor, VQR
from qiskit_machine_learning.kernels import QuantumKernel
from qiskit_machine_learning.neural_networks import CircuitQNN, two_layer_qnn
from sklearn.metrics import precision_score, recall_score, accuracy_score, mean_squared_error, mean_absolute_error
import numpy as np

from app.source.utils import utils
from app.source.utils.utils import createFeatureList, numberOfColumns


class myNeuralNetworkRegressor:
    def classify(pathTrain, pathTest, path_predict, backend, num_qubits, optimizer, loss, max_iter):

        print(pathTrain, pathTest, path_predict)
        data_train = pd.read_csv(pathTrain)
        data_train = data_train.drop(columns='Id') #QSVM richiede l'id e Pegasos no
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

        test_features = test_features.to_numpy() #Pegasos.fit accetta numpy array e non dataframe
        train_features = train_features.to_numpy()

        result = {}

        quantum_instance = QuantumInstance(backend)

        feature_map = ZFeatureMap(num_qubits)

        # construct ansatz
        ansatz = RealAmplitudes(num_qubits, reps=1)

        vqr = VQR(
            feature_map=feature_map,
            ansatz=ansatz,
            optimizer=L_BFGS_B(maxiter=int(max_iter)),
            loss=loss,
            quantum_instance=quantum_instance
        )
        try:
            # training
            print("Running...")
            start = time.time()
            vqr.fit(train_features, train_labels)
            training_time = time.time() - start
            print("Train effettuato in " + str(training_time))

            # test
            start_time = time.time()
            test_prediction = vqr.predict(test_features)
            testing_time = time.time() - start_time
            print("Test effettuato in " + str(testing_time))

            score = vqr.score(test_features, test_labels)
            mse = mean_squared_error(test_labels, test_prediction)
            mae = mean_absolute_error(test_labels, test_prediction)
            rmse = math.sqrt(mse)
            result["regression_score"] = score
            result["mse"] = mse
            result["mae"] = mae
            result["rmse"] = rmse

            # prediction
            start_time = time.time()
            if utils.numberOfColumns(path_predict) == 1:
                prediction_data = prediction_data.reshape(-1, 1)
            if utils.numberOfRows(path_predict) == 1:
                prediction_data = prediction_data.reshape(1, -1)
            predicted_labels = vqr.predict(prediction_data)
            prediction_time = time.time() - start_time
            total_time = time.time() - start
            print("Prediction effettuata in " + str(prediction_time))
            print("Total time: " + str(total_time))
            result["predicted_labels"] = np.array(predicted_labels)

            result["total_time"] = str(testing_time + training_time)[0:6]
            result["training_time"] = str(training_time)[0:6]
        except Exception as e:
            print(e)
            result["error"] = 1
            result["exception"] = e
        return result
