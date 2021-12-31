import matplotlib.pyplot as plt
import numpy as np
import csv
import pathlib
import pandas as pd
from qiskit import BasicAer, IBMQ
from qiskit.aqua.components.multiclass_extensions import AllPairs
from qiskit.circuit.library import ZZFeatureMap
from qiskit.aqua import QuantumInstance, aqua_globals
from qiskit.aqua.algorithms import QSVM
from qiskit.aqua.utils import split_dataset_to_data_and_labels, map_label_to_class_name
from qiskit.ml.datasets import iris
from app.source.classificazioneDataset.datasetLoader import LoadDataset
from sklearn.metrics import confusion_matrix, recall_score, precision_score
import winsound

token = 'add your token here'

def myQSVM(train,test,features,token,qubit=2):
    import time
    start_time = time.time()

    IBMQ.enable_account(token)
    provider = IBMQ.get_provider(hub='ibm-q')

    #backend = provider.get_backend('ibmq_quito')  # Specifying Real Quantum device
    #backend = provider.get_backend('ibmq_manila')  # Specifying Real Quantum device
    backend = provider.get_backend('ibmq_qasm_simulator')  # Specifying Simulator Quantum device

    seed = 8192
    shots = 1024
    aqua_globals.random_seed = seed

    feature_dim = qubit  # number of quibits
    # creating dataset
    training_input, test_input = LoadDataset(train, test, features, label='labels')

    #take a prediction value from csv
   # predizione=np.array([[0.3621
    # 859211670321,-1.411125025971791],[-2.501000087750893,0.6440884977209455],[2.532876452783644,-1.151269502578352]], np.int64)
    pathDoPrediction = pathlib.Path(__file__).cwd()
    pathDoPrediction = pathDoPrediction/'app/source/classificazioneDataset/doPrediction1.csv'
    predizione= np.array(list(csv.reader(open(pathDoPrediction.__str__(), "r"), delimiter=","))).astype("float")
    pathGroundTruth = pathlib.Path(__file__).cwd()
    pathGroundTruth = pathGroundTruth/'app/source/classificazioneDataset/ground_truth.csv'
    dataset = pd.read_csv(pathGroundTruth.__str__())
    y = dataset['labels']
    ground_truth=np.array(y)


    feature_map = ZZFeatureMap(feature_dimension=feature_dim, reps=2, entanglement='linear')
    print(feature_map)

    #qsvm = QSVM(feature_map, training_input, test_input, predizione, multiclass_extension=AllPairs())
    qsvm = QSVM(feature_map, training_input, test_input, predizione, multiclass_extension=AllPairs())

    quantum_instance = QuantumInstance(backend, shots=shots, seed_simulator=seed, seed_transpiler=seed)

    print('Running....\n')
    result = qsvm.run(quantum_instance)
    # data = np.array([[1.453], [1.023], [0.135], [0.266]])  # Unlabelled data
    # prediction = qsvm.predict(data, quantum_instance)  # Predict using unlabelled data
    #print(f'Testing success ratio: {result["testing_accuracy"]}')
    print('Prediction from datapoints set:')

    for k, v in result.items():
        print("{} : {}".format(k, v))

    print("ground truth :", ground_truth)
    predicted_labels = result["predicted_labels"]
    predicted_classes = result["predicted_classes"]


    #print('recall: ', recall_score(ground_truth,predicted_labels))
    #print('precision: ', precision_score(ground_truth, predicted_labels))

    #print(f'  accuracy: {100 * np.count_nonzero(predicted_labels == ground_truth)/len(predicted_labels)}%')


    # print('Prediction from input data where 0 = Non-Smoker and 1 = Smoker\n')
    # print(prediction)

    # The kernel matrix that was built from the training sample of the dataset.
    #kernel_matrix = result['kernel_matrix_training']
    #img = plt.imshow(np.asmatrix(kernel_matrix),interpolation='nearest',origin='upper',cmap='bone_r')
    print("--- %s seconds ---" % (time.time() - start_time))
    f =2500
    d = 5000 #1000ms =1sec
    #winsound.Beep(f,d)


