import csv
import os.path
import pathlib
import smtplib
import time
import warnings
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from threading import Thread

import flask
from flask import jsonify
import numpy as np
import pandas as pd
from flask import request, Response
from qiskit import IBMQ
from qiskit.aqua import QuantumInstance, aqua_globals
from qiskit.aqua.algorithms import QSVM
from qiskit.aqua.components.multiclass_extensions import AllPairs
from qiskit.circuit.library import ZZFeatureMap
from qiskit.providers.ibmq import least_busy

from app import app
from app.source.utils import utils

warnings.simplefilter(action="ignore", category=DeprecationWarning)


class ClassificazioneControl:
    @app.route("/classify_control", methods=["POST"])
    # @login_required
    def classify_control():
        """
        The function get the form value and start the async thread that will handle the classification
        :return:
        """
        path_train = request.form.get("pathTrain")
        path_test = request.form.get("pathTest")
        path_prediction = request.form.get("userpathToPredict")
        features = request.form.getlist("features")
        token = request.form.get("token")
        backend = request.form.get("backend")
        email = request.form.get("email")

        thread = Thread(
            target=ClassificazioneControl.classification_thread,
            args=(
                "classificazioneThread",
                path_train,
                path_test,
                path_prediction,
                features,
                token,
                backend,
                email))
        thread.setDaemon(True)
        thread.start()
        flask.g = thread
        return ""

    def classification_thread(
            self,
            path_train,
            path_test,
            path_prediction,
            features,
            token,
            backend,
            email):
        """
        The function is called from classify_control(), anc starts the async thread to run the classification,
        at the end of which the email with the result is sent, through the function get_classified_dataset()

        if result==1 error on IBM server (error reported through email)
        if result["noBackend"]==True selected backend is not active for the token or the are no active by default,
        and simulator is used

        :param path_train: training dataset path
        :param path_test: testing dataset path
        :param path_prediction: prediction dataset path
        :param features: features list used by QSVM
        :param token: user token
        :param backend: backend selected from the form
        :param email: email used to send the classification result
        :return: dict containing classification-related info
        """
        result: dict = ClassificazioneControl.classify(
            self, path_train, path_test, path_prediction, features, token, backend)
        if result != 0:
            ClassificazioneControl.get_classified_dataset(
                self, result, path_prediction, email)
        return result

    def classify(
            self,
            path_train,
            path_test,
            user_path_to_predict,
            features,
            token,
            backend_selected,
    ):
        """
        This function connects to the IBM backend, handles IBM backend errors, executes the QSVM classification,
        and creates the result dataset (classifiedDataset.csv)

        :param path_train: training dataset path
        :param path_test: testing dataset path
        :param user_path_to_predict: prediction dataset path
        :param features: features list used by QSVM
        :param token: user token
        :param backend_selected: backend selected from the form
        :return: dict containing classification-related info
        """

        start_time = time.time()
        no_backend = False
        provider = ""
        try:
            IBMQ.enable_account(token)
            provider = IBMQ.get_provider(hub="ibm-q")
            IBMQ.disable_account()
        except:
            print("Error activating/deactivating IBM account")

        qubit = len(features)

        try:
            if (
                    backend_selected
                    and backend_selected != "backend"
                    and provider.get_backend(backend_selected).configuration().n_qubits
                    >= qubit
            ):
                print("backend selected:" + str(backend_selected))
                print("backend qubit:" +
                      str(provider.get_backend(backend_selected).configuration().n_qubits))
                backend = provider.get_backend(
                    backend_selected
                )  # Specifying Quantum System
            else:
                backend = least_busy(
                    provider.backends(
                        filters=lambda x: x.configuration().n_qubits >= qubit
                                          and not x.configuration().simulator
                                          and x.status().operational
                    )
                )
                print("least busy backend: ", backend)
                print(
                    "backend qubit:"
                    + str(
                        provider.get_backend(backend.name())
                            .configuration()
                            .n_qubits
                    )
                )
        except:
            # when selected backend has not enough qubit, or no backends has enough
            # qubits, or the user token has no privileges to use the selected
            # backend
            no_backend = True
            backend = provider.get_backend("ibmq_qasm_simulator")
            print("backend selected: simulator")
            print("backend qubit:" +
                  str(provider.get_backend(backend.name()).configuration().n_qubits))

        seed = 8192
        shots = 1024
        aqua_globals.random_seed = seed

        training_input, test_input = ClassificazioneControl.load_dataset(
            path_train, path_test, features, label="labels"
        )

        path_do_prediction = pathlib.Path(user_path_to_predict).parent
        if os.path.exists(path_do_prediction / "doPredictionFE.csv"):
            path_do_prediction = path_do_prediction / "doPredictionFE.csv"
        else:
            path_do_prediction = user_path_to_predict
        file_to_predict = open(path_do_prediction.__str__(), "r")
        prediction = np.array(
            list(csv.reader(file_to_predict, delimiter=","))
        ).astype("float")

        feature_map = ZZFeatureMap(
            feature_dimension=qubit, reps=2, entanglement="linear"
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
        try:
            result = qsvm.run(quantum_instance)
        except:
            print("Error on IBM server")
            result = 1
            return result

        total_time = time.time() - start_time
        result["total_time"] = str(total_time)[0:6]

        print("Prediction from datapoints set:")
        for k, v in result.items():
            print("{} : {}".format(k, v))

        predicted_labels = result["predicted_labels"]

        classified_file = open(
            pathlib.Path(user_path_to_predict).parent / "classifiedFile.csv",
            "w",
        )
        prediction_file = open(user_path_to_predict, "r")
        rows = prediction_file.readlines()

        for j in range(1, utils.numberOfColumns(user_path_to_predict) + 1):
            classified_file.write("feature" + str(j) + ",")
        classified_file.write("label\n")
        i = 0
        for row in rows:
            classified_file.write(
                row.rstrip("\n") + "," + str(predicted_labels[i]) + "\n"
            )
            i += 1
        classified_file.close()
        prediction_file.close()
        file_to_predict.close()

        result["no_backend"] = no_backend
        return result

    #def plot(self, classified_dataset):
    #    return classified_dataset

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

    def get_classified_dataset(self, result, userpathToPredict, email):
        """

        :param result: dict used to add details sent through email
        :param userpathToPredict: String to get the directory of the exact dataset of the exact user
        :param email: destination email
        :return: 0 error, 1 done
        """

        msg = MIMEMultipart()
        msg["From"] = "quantumoonlight@gmail.com"
        msg["To"] = "quantumoonlight@gmail.com, " + email
        msg["Date"] = formatdate(localtime=True)
        # + dataset.name + " " + dataset.upload_date
        msg["Subject"] = "Classification Result "

        msg.attach(
            MIMEText(
                '<td><center><img style="width:25%;" src="cid:image"></center></td>',
                'html'))
        img_path = open(
            pathlib.Path(__file__).parents[2] /
            "static" /
            "images" /
            "logos" /
            "Logo_SenzaScritta.png",
            "rb")
        img = MIMEImage(img_path.read())
        img.add_header('Content-ID', '<image>')
        msg.attach(img)

        if result == 1:
            msg.attach(
                MIMEText(
                    "<center><h3>IBM Server error, please check status on https:"
                    "//quantum-computing.ibm.com/services?services=systems</center></h3>",
                    'html'))

        else:
            msg.attach(
                MIMEText(
                    "<center><h1>Classification details:</h1></center>",
                    'html'))
            accuracy = result.get("testing_accuracy")
            success_ratio = result.get("test_success_ratio")
            msg.attach(
                MIMEText(
                    "<center><h3>Testing accuracy: " +
                    "{:.2%}".format(accuracy) +
                    "</h3></center>",
                    'html'))
            msg.attach(
                MIMEText(
                    "<center><h3>Success ratio: " +
                    "{:.2%}".format(success_ratio) +
                    "</h3></center>",
                    'html'))
            msg.attach(
                MIMEText(
                    "<center><h3>Total time elapsed: " +
                    result.get("total_time") +
                    "s</h3></center>",
                    'html'))

            if result["no_backend"]:
                msg.attach(
                    MIMEText(
                        "<center><h5>For this classification, a simulated quantum backend has been used "
                        "due to the following reason:<br></h5>"
                        "<h6>- The selected backend has not enough qubits"
                        " to process all the dataset features<br>"
                        "- There are no backends with enough qubits available at the moment<br>"
                        "- The used token has no privileges to use the selected backend<br>"
                        "</center></h6>", 'html'))

            file = pathlib.Path(userpathToPredict).parent / \
                   "classifiedFile.csv"
            attach_file = open(file, "rb")
            payload = MIMEBase("application", "octet-stream")
            payload.set_payload(attach_file.read())
            encoders.encode_base64(payload)
            payload.add_header(
                "Content-Disposition",
                "attachment",
                filename="ClassifiedDataset.csv",
            )
            msg.attach(payload)
            attach_file.close()

        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.ehlo()
            server.login("quantumoonlight@gmail.com", "Quantum123?")
            server.send_message(msg)
            server.close()
        except:
            return 0
        return 1

    def __init__(self):
        return
