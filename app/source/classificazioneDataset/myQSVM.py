import csv
import os
import pathlib
import time
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from qiskit.aqua import aqua_globals
from qiskit.aqua.algorithms import QSVM
from qiskit.aqua.components.multiclass_extensions import AllPairs
from qiskit.circuit.library import ZZFeatureMap
from qiskit.utils import QuantumInstance
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


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
            predicted_labels = result.get("predicted_labels")
        except Exception as e:
            print("Error on IBM server")
            print(e)
            result["error"] = 1
            return result

        test = pd.read_csv(path_test, index_col=0)
        test_labels = test["labels"]
        test_features = test.drop(columns='labels')
        test_labels = test_labels.to_numpy()
        test_features = test_features.to_numpy()
        print("Test labels: ", test_labels)
        print("Test features: ", test_features)

        total_time = time.time() - start_time
        result["total_time"] = str(total_time)[0:6]

        result["training_time"] = "-1"

        test_prediction = qsvm.predict(test_features, quantum_instance)
        accuracy = accuracy_score(test_labels, test_prediction)
        precision = precision_score(test_labels, test_prediction, average="weighted", zero_division=0)
        recall = recall_score(test_labels, test_prediction, average="weighted")
        f1 = f1_score(test_labels, test_prediction, average="weighted")
        result["f1"] = f1
        result["testing_precision"] = precision
        result["testing_recall"] = recall
        result["testing_accuracy"] = accuracy
        result["predicted_labels"] = predicted_labels

        # Each attribute we'll plot in the radar chart.
        labels = ['Precision', 'Recall', 'Accuracy', 'f1']
        values = [precision * 100, recall * 100, accuracy * 100, f1 * 100]
        # Number of variables we're plotting.
        num_vars = len(labels)
        print(values)
        # Split the circle into even parts and save the angles
        # so we know where to put each axis.
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

        # ax = plt.subplot(polar=True)
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        # Draw the outline of our data.
        ax.plot(angles, values, color='#1aaf6c', linewidth=1)
        # Fill it in.
        ax.fill(angles, values, color='#1aaf6c', alpha=0.25)

        # Fix axis to go in the right order and start at 12 o'clock.
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)

        # Draw axis lines for each angle and label.
        ax.set_thetagrids(np.degrees(angles), labels)

        # Go through labels and adjust alignment based on where
        # it is in the circle.
        for label, angle in zip(ax.get_xticklabels(), angles):
            if angle in (0, np.pi):
                label.set_horizontalalignment('center')
            elif 0 < angle < np.pi:
                label.set_horizontalalignment('left')
            else:
                label.set_horizontalalignment('right')

        # Ensure radar goes from 0 to 100.
        ax.set_ylim(0, 100)
        # You can also set gridlines manually like this:
        # ax.set_rgrids([20, 40, 60, 80, 100])

        # Set position of y-labels (0-100) to be in the middle
        # of the first two axes.
        ax.set_rlabel_position(180 / num_vars)

        # Add some custom styling.
        # Change the color of the tick labels.
        ax.tick_params(colors='#222222')
        # Make the y-axis (0-100) labels smaller.
        ax.tick_params(axis='y', labelsize=8)
        # Change the color of the circular gridlines.
        ax.grid(color='#AAAAAA')
        # Change the color of the outermost gridline (the spine).
        ax.spines['polar'].set_color('#222222')
        # Change the background color inside the circle itself.
        ax.set_facecolor('#FAFAFA')

        # Lastly, give the chart a title and give it some padding
        ax.set_title('QSVC metrics', y=1.08)
        plt.show()
        plt.savefig(pathlib.Path(path_test).parent / 'graphClassifier', dpi=150)

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
