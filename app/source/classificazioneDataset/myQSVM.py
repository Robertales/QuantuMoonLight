import csv
import os
import pathlib
import time
import numpy as np
import pandas as pd
from qiskit.aqua import aqua_globals
from qiskit.aqua.algorithms import QSVM
from qiskit.aqua.components.multiclass_extensions import AllPairs
from qiskit.circuit.library import ZZFeatureMap
from qiskit.utils import QuantumInstance


class myQSVM:

    def classify(path_train, path_test, path_predict, backend, features, num_qubits):
        seed = 8192
        shots = 1024
        result = {}
        aqua_globals.random_seed = seed
        training_input, test_input = myQSVM.load_dataset(
            path_train, path_test, features, label="labels"
        )

        path_do_prediction = pathlib.Path(path_predict).parent
        if os.path.exists(path_do_prediction / "doPredictionFE.csv"):
            path_do_prediction = path_do_prediction / "doPredictionFE.csv"
        else:
            path_do_prediction = path_predict

        file_to_predict = open(path_do_prediction.__str__(), "r")
        print(path_do_prediction)
        prediction = np.array(
            list(csv.reader(file_to_predict, delimiter=","))
        ).astype("float")

        feature_map = ZZFeatureMap(
            feature_dimension=num_qubits, reps=2, entanglement="linear"
        )
        print(feature_map)

        qsvm = QSVM(
            feature_map,
            training_input,
            test_input,
            prediction,
            multiclass_extension=AllPairs(),
        )

        quantum_instance = QuantumInstance(
            backend,
            shots=shots,
            seed_simulator=seed,
            seed_transpiler=seed,
        )

        print("Running....\n")
        start_time = time.time()
        try:
            result = qsvm.run(quantum_instance)
        except Exception as e:
            print("Error on IBM server")
            print(e)
            result["error"] = 1
            return result

        total_time = time.time() - start_time
        result["total_time"] = str(total_time)[0:6]
        result["training_time"] = "--"
        result["testing_precision"] = "--"
        result["testing_recall"] = "--"
        return result

    @staticmethod
    def load_dataset(training_path, testing_path, features, label):
        """
        Loads the data, normalizes it and returns it in the following format:
        {class_0: points_0, class_1:points_1, ...}
        Where points_i corresponds to the points that belong to class_i as a numpy array
        """
        df_train = pd.read_csv(training_path, index_col=0)
        df_test = pd.read_csv(testing_path, index_col=0)

        train, test = df_train, df_test

        train_dict, test_dict = {}, {}
        for category in train[label].unique():
            train_dict[category] = train[train["labels"] == category][
                features
            ].values
            test_dict[category] = test[test["labels"] == category][
                features
            ].values

        return train_dict, test_dict
