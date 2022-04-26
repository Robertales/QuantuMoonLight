import time
import pandas as pd
from qiskit.circuit.library import ZFeatureMap
from qiskit.utils import algorithm_globals, QuantumInstance
from qiskit_machine_learning.algorithms import PegasosQSVC
from qiskit_machine_learning.kernels import QuantumKernel


class myPegasosQSVC:
    def classify(self, pathTrain, pathTest, path_predict, backend, num_qubits):
        data_train = pd.read_csv(pathTrain)
        train_features = data_train.drop(columns='labels')
        train_labels = data_train["labels"].values
        data_test = pd.read_csv(pathTest)
        test_features = data_test.drop(columns='labels')
        test_labels = data_test["labels"].values
        prediction_data = pd.read_csv(path_predict)

        result = {}

        tau = 100
        C = 1000
        algorithm_globals.random_seed = 12345
        feature_map = ZFeatureMap(feature_dimension=num_qubits, reps=1)
        qkernel = QuantumKernel(feature_map=feature_map, quantum_instance=QuantumInstance(backend))
        qsvc = PegasosQSVC(quantum_kernel=qkernel, C=C, num_steps=tau)

        # training
        print("Running...")
        start_time = time.time()
        qsvc.fit(train_features, train_labels)
        total_time = time.time() - start_time
        print("Train effettuato in " + str(total_time))

        # testing
        start_time = time.time()
        score = qsvc.score(test_features, test_labels)
        print("Score: ", score)
        total_time = time.time() - start_time
        print("Test effettuato in " + str(total_time))

        # prediction
        start_time = time.time()
        predicted_labels = qsvc.predict(prediction_data)
        total_time = time.time() - start_time
        print("Prediction effettuata in " + str(total_time))
        result["predicted_labels"] = predicted_labels

        return result
