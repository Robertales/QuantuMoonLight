from app import app
import time
import csv
import pathlib
import numpy as np
import pandas as pd
from qiskit import IBMQ
from qiskit.aqua import QuantumInstance, aqua_globals
from qiskit.aqua.algorithms import QSVM
from qiskit.aqua.components.multiclass_extensions import AllPairs
from qiskit.circuit.library import ZZFeatureMap

def classify(pathTrain, pathTest, features, token, qubit=2, backend='ibmq_qasm_simulator'):
    start_time = time.time()

    IBMQ.enable_account(token)
    provider = IBMQ.get_provider(hub='ibm-q')
    backend = provider.get_backend(backend)  # Specifying Simulator Quantum device

    seed = 8192
    shots = 1024
    aqua_globals.random_seed = seed

    feature_dim = len(features)  # number of quibits
    # creating dataset
    training_input, test_input = loadDataset(pathTrain, pathTest, features, label='labels')

    pathDoPrediction = pathlib.Path(__file__).cwd()
    pathDoPrediction = pathDoPrediction / 'app/source/classificazioneDataset/doPrediction1.csv'
    predizione = np.array(list(csv.reader(open(pathDoPrediction.__str__(), "r"), delimiter=","))).astype("float")
    pathGroundTruth = pathlib.Path(__file__).cwd()
    pathGroundTruth = pathGroundTruth / 'app/source/classificazioneDataset/ground_truth.csv'
    dataset = pd.read_csv(pathGroundTruth.__str__())
    y = dataset['labels']
    ground_truth = np.array(y)

    feature_map = ZZFeatureMap(feature_dimension=feature_dim, reps=2, entanglement='linear')
    print(feature_map)

    qsvm = QSVM(feature_map, training_input, test_input, predizione, multiclass_extension=AllPairs())

    quantum_instance = QuantumInstance(backend, shots=shots, seed_simulator=seed, seed_transpiler=seed)

    print('Running....\n')
    result = qsvm.run(quantum_instance)

    print('Prediction from datapoints set:')
    for k, v in result.items():
        print("{} : {}".format(k, v))
    print("ground truth :", ground_truth)

    # predicted_labels = result["predicted_labels"]
    # predicted_classes = result["predicted_classes"]
    # print('recall: ', recall_score(ground_truth,predicted_labels))
    # print('precision: ', precision_score(ground_truth, predicted_labels))
    # print(f'  accuracy: {100 * np.count_nonzero(predicted_labels == ground_truth)/len(predicted_labels)}%')

    print("--- %s seconds ---" % (time.time() - start_time))

    return result


def plot(dataset_classificato):
    return dataset_classificato


def loadDataset(training_path, testing_path, features, label, gaussian=True, minmax=False):
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
        train_dict[category] = train[train['labels'] == category][features].values
        test_dict[category] = test[test['labels'] == category][features].values

    return train_dict, test_dict
