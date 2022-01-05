from app import app
import time
import csv
import pathlib
import numpy as np
import pandas as pd
from qiskit import IBMQ
from qiskit.providers.ibmq import least_busy
from qiskit.aqua import QuantumInstance, aqua_globals
from qiskit.aqua.algorithms import QSVM
from qiskit.aqua.components.multiclass_extensions import AllPairs
from qiskit.circuit.library import ZZFeatureMap
import smtplib
from flask import session
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from sklearn.metrics import recall_score, precision_score
from flask_login import current_user


def classify(pathTrain, pathTest, features, token, qubit, backendSelected):
    start_time = time.time()
    noBackend=False

    try:
        IBMQ.enable_account(token)
    except:
        print("token non valido")
        return 0

    provider = IBMQ.get_provider(hub='ibm-q')

    try:
        if backendSelected:
            print("backend selected:" + str(backendSelected))
            backend = provider.get_backend(backendSelected)  # Specifying Quantum System
        else:
            backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= qubit and not x.configuration().simulator and x.status().operational == True))
            print("least busy backend: ", backend)
    except:
        noBackend=True
        backend = provider.get_backend('ibmq_qasm_simulator')
        print("backend selected: simulator")


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
    try:
        result = qsvm.run(quantum_instance)
    except:
        print("errore su server ibm")
        result= 1
        return result

    totalTime = time.time() - start_time
    result["totalTime"]=str(totalTime)[0:6]

    print('Prediction from datapoints set:')
    for k, v in result.items():
        print("{} : {}".format(k, v))
    print("ground truth :", ground_truth)

    predicted_labels = result["predicted_labels"]
    predicted_classes = result["predicted_classes"]
    #print('recall: ', recall_score(ground_truth,predicted_labels))
    #print('precision: ', precision_score(ground_truth, predicted_labels))
    #print(f'  accuracy: {100 * np.count_nonzero(predicted_labels == ground_truth)/len(predicted_labels)}%')

    classifiedFile = open("upload_dataset\\classifiedFile.csv", "w")
    predictionFile = open("app\\source\\classificazioneDataset\\doPrediction1.csv", "r")
    rows = predictionFile.readlines()

    for j in range(1,qubit):
        classifiedFile.write("feature"+str(j)+",")
    classifiedFile.write("label\n")
    i = 0
    for row in rows:
        classifiedFile.write(row.rstrip("\n") + "," + str(predicted_labels[i])+"\n")
        i += 1

    if noBackend:
        result["noBackend"]=True
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

def getClassifiedDataset(result):
    """

    :type result: dict
    """
    msg = MIMEMultipart()
    #assert isinstance(current_user, User)
    #user = current_user
    #dataset=session["currentDataset"]
    msg['From'] = "quantumoonlight@gmail.com"
    msg['To'] = "quantumoonlight@gmail.com"
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "Classification Result of " #+ dataset.name + " " + dataset.upload_date

    if result==1:
        msg.attach(MIMEText("IBM Server error, please check status on https://quantum-computing.ibm.com/services?services=systems \n\n"))
    else:
        msg.attach(MIMEText("This is your classification:\n\n"))
        accuracy = result.get("testing_accuracy")
        successRatio = result.get("test_success_ratio")
        msg.attach(MIMEText("Testing accuracy: " + "{:.2%}".format(accuracy) + "\n"))
        msg.attach(MIMEText("Success ratio: " + "{:.2%}".format(successRatio) + "\n"))
        msg.attach(MIMEText("Total time elapsed:" + result.get("totalTime") + "s"))

        file = "upload_dataset\\classifiedFile.csv"
        attach_file = open(file, "rb")
        payload = MIMEBase('application', "octet-stream")
        payload.set_payload(attach_file.read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', 'attachment', filename="ClassifiedDataset.csv")
        msg.attach(payload)

    server=smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login("quantumoonlight@gmail.com", "Quantum123?")
    server.send_message( msg)
    server.close()

