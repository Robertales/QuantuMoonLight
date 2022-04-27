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
from flask import request, Response
from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy
from app import app
from app.source.classificazioneDataset.myQSVR import myQSVR
from app.source.classificazioneDataset.myNeuralNetworkClassifier import myNeuralNetworkClassifier
from app.source.classificazioneDataset.myPegasosQSVC import myPegasosQSVC
from app.source.classificazioneDataset.myQSVC import myQSVC
from app.source.classificazioneDataset.myQSVM import myQSVM
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
        model = request.form.get("model")

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
                email,
                model))
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
            email,
            model):
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
            self, path_train, path_test, path_prediction, features, token, backend, model)
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
            model
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

        no_backend = False
        result = {}
        result["error"] = 0
        result["model"] = model
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
                    and backend_selected != "aer_simulator"
                    and backend_selected != "backend"
                    and int(provider.get_backend(backend_selected).configuration().n_qubits) >= qubit
            ):
                print("backend selected:" + str(backend_selected))
                print("backend qubit:" +
                      str(provider.get_backend(backend_selected).configuration().n_qubits))
                backend = provider.get_backend(
                    backend_selected
                )  # Specifying Quantum System
            elif backend_selected == "aer_simulator":
                backend = Aer.get_backend('aer_simulator')
                print("backend selected: aer_simulator")
            else:
                backend = least_busy(
                    provider.backends(
                        filters=lambda x: int(x.configuration().n_qubits) >= qubit
                                          and not x.configuration().simulator
                                          and x.status().operational == True
                    )
                )
                print("least busy backend: ", backend)
                print("backend qubit:" + str(provider.get_backend(backend.name()).configuration().n_qubits))

        except Exception as e:
            # when selected backend has not enough qubit, or no backends has enough
            # qubits, or the user token has no privileges to use the selected
            # backend
            print(e)
            no_backend = True
            backend = Aer.get_backend('aer_simulator')
            print("backend selected: simulator")
            print("backend qubit: 32")

        if model == "QSVM":
            r = myQSVM.classify(path_train, path_test, user_path_to_predict, backend, features, qubit)
            result = {**result, **r}

        elif model == "PegasosQSVC":
            r = myPegasosQSVC.classify(path_train, path_test, user_path_to_predict, backend, qubit)
            result = {**result, **r}

        elif model == "QSVC":
            r = myQSVC.classify(path_train, path_test, user_path_to_predict, backend, qubit)
            result = {**result, **r}

        elif model == "NeuralNetworkClassifier":
            r = myNeuralNetworkClassifier.classify(path_train, path_test, user_path_to_predict, backend, qubit)
            result = {**result, **r}

        elif model == "QSVR":
            r = myQSVR.classify(path_train, path_test, user_path_to_predict, backend, qubit)
            result = {**result, **r}

        elif model == "NeuralNetworkRegressor":
            r = myQSVR.classify(path_train, path_test, user_path_to_predict, backend, qubit)
            result = {**result, **r}

        if result["error"] != 1:
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
            if model != "QSVM":
                rows.pop(0)

            for j in range(1, utils.numberOfColumns(user_path_to_predict) + 1):
                classified_file.write("feature" + str(j) + ",")
            classified_file.write("label\n")
            i = 0
            for row in rows:
                classified_file.write(
                    row.rstrip("\n") + "," +
                    str(predicted_labels[i]) + "\n"
                )
                i += 1
            classified_file.close()
            prediction_file.close()

        result["no_backend"] = no_backend
        return result

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

        if result["error"] == 1:
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

            model = result.get("model")
            if model == "QSVR" or model == "NeuralNetworkRegressor":
                mae = result.get("mae")
                mse = result.get("mse")
                score = result.get("regression_score")
                msg.attach(
                    MIMEText(
                        "<center><h3>" +
                        "Modello: " + result.get("model") +
                        "<br><br> Mean Squared Error: " +
                        "{:.2%}".format(float(mse)) +
                        "<br><br> Mean Absolute Error: " +
                        "{:.2%}".format(float(mae)) +
                        "<br><br> Regression score: " +
                        "{:.2%}".format(float(score)) +
                        "</h3></center>",
                        'html'))
            else:
                accuracy = result.get("testing_accuracy")
                precision = result.get("testing_precision")
                recall = result.get("testing_recall")
                msg.attach(
                    MIMEText(
                        "<center><h3>" +
                        "<br><br>Testing accuracy: " +
                        "{:.2%}".format(accuracy) +
                        "<br><br>Testing precision: " +
                        "{:.2%}".format(precision) +
                        "<br><br>Testing recall: " +
                        "{:.2%}".format(recall) +
                        "</h3></center>", 'html'))

            msg.attach(
                MIMEText(
                    "<center><h3>Training time: " +
                    result.get("training_time") +
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
