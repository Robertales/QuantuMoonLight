import csv
import time
import pandas as pd
from qiskit import QuantumCircuit
from qiskit.algorithms.optimizers import COBYLA, SLSQP, ADAM, GradientDescent
from qiskit.circuit.library import ZFeatureMap, ZZFeatureMap, RealAmplitudes
from qiskit.utils import algorithm_globals, QuantumInstance
from qiskit_machine_learning.algorithms import PegasosQSVC, NeuralNetworkClassifier, NeuralNetworkRegressor
from qiskit_machine_learning.kernels import QuantumKernel
from qiskit_machine_learning.neural_networks import CircuitQNN
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

        print("Train features: ", train_features)
        print("Test features: ", test_features)
        print("Train labels: ", train_labels)
        print("Test labels: ", test_labels)
        print(prediction_data)

        result = {}

        quantum_instance = QuantumInstance(backend)

        feature_map = ZZFeatureMap(num_qubits)

        # construct ansatz
        ansatz = RealAmplitudes(num_qubits, reps=1)

        # construct quantum circuit
        qc = QuantumCircuit(num_qubits)
        qc.append(feature_map, range(num_qubits))
        qc.append(ansatz, range(num_qubits))
        qc.decompose().draw(output="mpl")

        # parity maps bitstrings to 0 or 1
        def parity(x):
            return "{:b}".format(x).count("1") % 2

        output_shape = len(np.unique(train_labels))  # corresponds to the number of classes, possible outcomes of the (parity) mapping.
        # construct QNN
        circuit_qnn = CircuitQNN(
            circuit=qc,
            input_params=feature_map.parameters,
            weight_params=ansatz.parameters,
            interpret=parity,
            output_shape=output_shape,
            quantum_instance=quantum_instance,
        )
        # construct classifier
        def callback():
            return

        circuit_regressor = []
        if optimizer == "COBYLA":
            circuit_regressor = NeuralNetworkRegressor(
                neural_network=circuit_qnn, optimizer=COBYLA(maxiter=int(max_iter)), loss=loss, callback=callback
            )
        elif optimizer == "SLSQP":
            circuit_regressor = NeuralNetworkRegressor(
                neural_network=circuit_qnn, optimizer=SLSQP(maxiter=int(max_iter)), loss=loss, callback=callback
            )
        elif optimizer == "ADAM":
            circuit_regressor = NeuralNetworkRegressor(
                neural_network=circuit_qnn, optimizer=ADAM(maxiter=int(max_iter)), loss=loss, callback=callback
            )
        elif optimizer == "GradientDescent":
            circuit_regressor = NeuralNetworkRegressor(
                neural_network=circuit_qnn, optimizer=GradientDescent(maxiter=int(max_iter)), loss=loss,
                callback=callback
            )

        # training
        print("Running...")
        start_time = time.time()
        circuit_regressor.fit(train_features, train_labels)
        training_time = time.time() - start_time
        print("Train effettuato in " + str(training_time))

        # test
        start_time = time.time()
        score = circuit_regressor.score(test_features, test_labels)
        test_prediction = circuit_regressor.predict(test_features)
        testing_time = time.time() - start_time
        result["regression_score"] = score
        mse = mean_squared_error(test_labels, test_prediction)
        mae = mean_absolute_error(test_labels, test_prediction)
        result["mse"] = mse
        result["mae"] = mae

        # prediction
        start_time = time.time()
        predicted_labels = circuit_regressor.predict(prediction_data)
        total_time = time.time() - start_time
        print("Prediction effettuata in " + str(total_time))
        result["predicted_labels"] = np.array(predicted_labels)

        result["total_time"] = str(testing_time + training_time)[0:6]
        result["training_time"] = str(training_time)[0:6]

        return result
