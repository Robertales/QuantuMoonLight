import os
import pathlib
import unittest
from os.path import exists

from app import app
from app.source.classificazioneDataset import ClassifyControl
from app.source.utils import utils


class TestClassifyControl(unittest.TestCase):

    def test_classify_control(self):
        """
        Test the input coming from the form and the status code returned, and check if the classification result
        file is created
        """
        path_train = (
            pathlib.Path(__file__).cwd()
            / "testingFiles"
            / "DataSetTrainPreprocessato.csv"
        )
        path_test = (
            pathlib.Path(__file__).cwd()
            / "testingFiles"
            / "DataSetTestPreprocessato.csv"
        )
        path_prediction = (
            pathlib.Path(__file__).cwd() / "testingFiles" / "doPrediction.csv"
        )
        features = utils.createFeatureList(2)
        token = "43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2"
        backend = "ibmq_qasm_simulator"
        email = "quantumoonlight@gmail.com"

        response = app.test_client(self).post(
            "/classify_control",
            data=dict(
                pathTrain=path_train,
                pathTest=path_test,
                email=email,
                userpathToPredict=path_prediction,
                features=features,
                token=token,
                backend=backend,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(200, statuscode)

    def test_classification_thread(self):
        """
                Test the classify function with correct parameters and input files, and check if the classification result
                file is created
                """
        path_train = (
                pathlib.Path(__file__).cwd()
                / "testingFiles"
                / "DataSetTrainPreprocessato.csv"
        )
        path_test = (
                pathlib.Path(__file__).cwd()
                / "testingFiles"
                / "DataSetTestPreprocessato.csv"
        )
        path_prediction = (
                pathlib.Path(__file__).cwd() / "testingFiles" / "doPrediction.csv"
        )
        features = utils.createFeatureList(2)
        token = "43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2"
        backend_selected = "ibmq_qasm_simulator"
        email = "quantumoonlight@gmail.com"

        result = ClassifyControl.classification_thread(path_train, path_test, path_prediction, features, token, backend_selected, email)

        self.assertNotEqual(result, 1)
        self.assertTrue(
            exists(
                pathlib.Path(__file__).parent
                / "testingFiles"
                / "classifiedFile.csv"
            )
        )

    def test_classify(self):
        """
        Test the classify function with correct parameters and input files, and check if the classification result
        file is created
        """
        path_train = (
            pathlib.Path(__file__).cwd()
            / "testingFiles"
            / "DataSetTrainPreprocessato.csv"
        )
        path_test = (
            pathlib.Path(__file__).cwd()
            / "testingFiles"
            / "DataSetTestPreprocessato.csv"
        )
        path_prediction = (
            pathlib.Path(__file__).cwd() / "testingFiles" / "doPrediction.csv"
        )
        features = utils.createFeatureList(2)
        token = "43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2"
        backend_selected = "ibmq_qasm_simulator"

        result = ClassifyControl.classify(
            path_train,
            path_test,
            path_prediction,
            features,
            token,
            backend_selected,
        )

        self.assertNotEqual(result, 1)
        self.assertTrue(
            exists(
                pathlib.Path(__file__).parent
                / "testingFiles"
                / "classifiedFile.csv"
            )
        )

    def test_classify_ibmFail(self):
        """
        Test the classify function with not valid train and test datasets, to make the IBM backend fail on purpose
        """
        path_train = (
            pathlib.Path(__file__).cwd()
            / "testingFiles"
            / "DataSetTrainPreprocessato.csv"
        )
        path_test = (
            pathlib.Path(__file__).cwd()
            / "testingFiles"
            / "DataSetTestPreprocessato.csv"
        )
        path_prediction = (
            pathlib.Path(__file__).cwd() / "testingFiles" / "bupa.csv"
        )
        features = utils.createFeatureList(2)
        token = "43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2"
        backend_selected = "ibmq_qasm_simulator"

        result = ClassifyControl.classify(
            path_train,
            path_test,
            path_prediction,
            features,
            token,
            backend_selected,
        )
        self.assertEqual(result, 1)
        self.assertFalse(
            exists(
                pathlib.Path(__file__).parent
                / "testingFiles"
                / "classifiedFile.csv"
            )
        )

    def test_getClassifiedDataset(self):
        """
        Test the function that send the email, with fixed parameters as input
        """
        result = {
            "testing_accuracy": 0.55687446747,
            "test_success_ratio": 0.4765984595,
            "total_time": str(90.7),
            "no_backend": True
        }
        open(
            pathlib.Path(__file__).parent
            / "testingFiles"
            / "classifiedFile.csv",
            "w",
        )
        user_path_to_predict = (
            pathlib.Path(__file__).cwd() / "testingFiles" / "doPrediction.csv"
        )

        value = ClassifyControl.get_classified_dataset(
            result, user_path_to_predict, "quantumoonlight@gmail.com"
        )
        self.assertEqual(value, 1)

    def tearDown(self):
        if os.path.exists(
            pathlib.Path(__file__).parent
            / "testingFiles"
            / "classifiedFile.csv"
        ):
            os.remove(
                pathlib.Path(__file__).parent
                / "testingFiles"
                / "classifiedFile.csv"
            )
