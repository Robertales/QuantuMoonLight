import time
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt
from qiskit import QuantumCircuit
from qiskit.algorithms.optimizers import COBYLA, SLSQP, ADAM, GradientDescent
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit.utils import QuantumInstance
from qiskit_machine_learning.algorithms import NeuralNetworkClassifier
from qiskit_machine_learning.neural_networks import CircuitQNN
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score
import numpy as np
from app.source.utils import utils

class myNeuralNetworkClassifier:
    def classify(pathTrain, pathTest, path_predict, backend, num_qubits, optimizer, loss, max_iter):


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

        output_shape = len(
            np.unique(train_labels))  # corresponds to the number of classes, possible outcomes of the (parity) mapping.
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

        circuit_classifier = NeuralNetworkClassifier(
            neural_network=circuit_qnn, optimizer=SLSQP(maxiter=int(max_iter)), loss=str(loss)
        )
        if optimizer == "COBYLA":
            circuit_classifier = NeuralNetworkClassifier(
                neural_network=circuit_qnn, optimizer=COBYLA(maxiter=int(max_iter)), loss=str(loss)
            )

        elif optimizer == "ADAM":
            circuit_classifier = NeuralNetworkClassifier(
                neural_network=circuit_qnn, optimizer=ADAM(maxiter=int(max_iter)), loss=str(loss)
            )
        elif optimizer == "GradientDescent":
            circuit_classifier = NeuralNetworkClassifier(
                neural_network=circuit_qnn, optimizer=GradientDescent(maxiter=int(max_iter)), loss=str(loss)
            )

        try:
            # training
            print("Running...")
            start_time = time.time()
            circuit_classifier.fit(train_features, train_labels)
            training_time = time.time() - start_time
            print("Train effettuato in " + str(training_time))

            # test
            start_time = time.time()
            test_prediction = circuit_classifier.predict(test_features)
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
            predicted_labels = circuit_classifier.predict(prediction_data)
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
            plt.savefig(Path(pathTest).parent / 'graphLabels', dpi=150)

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
            plt.savefig(Path(pathTest).parent / 'graphClassifier', dpi=150)
        except Exception as e:
            print(e)
            result["error"] = 1
            result["exception"] = e
        return result
