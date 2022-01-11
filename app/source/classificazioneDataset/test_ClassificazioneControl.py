import os
import pathlib
import unittest
from os.path import exists

from flask_login import current_user
from app.models import User
from app import app
from app.source.utils import utils
from pathlib import Path
from app.source.classificazioneDataset import ClassificazioneControl


class TestClassificazioneControl(unittest.TestCase):
    # def setUp(self):

    def test_ClassificazioneControl(self):
        pathTrain = pathlib.Path(__file__).cwd(
        ) / "testingFiles" / "DataSetTrainPreprocessato.csv"
        pathTest = pathlib.Path(__file__).cwd() / \
            "testingFiles" / "DataSetTestPreprocessato.csv"
        pathPrediction = pathlib.Path(__file__).cwd(
        ) / "testingFiles" / "doPrediction.csv"
        features = utils.createFeatureList(2)
        token = '43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2'
        backend = "ibmq_qasm_simulator"
        email = "quantumoonlight@gmail.com"

        response = app.test_client(self).post(
            '/classificazioneControl',
            data=dict(pathTrain=pathTrain, pathTest=pathTest, email=email,
                      userpathToPredict=pathPrediction, features=features,
                      token=token, backend=backend))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(exists(pathlib.Path(__file__).parent /
                        "testingFiles" / "classifiedFile.csv"))

    def test_classify(self):
        pathTrain = pathlib.Path(__file__).cwd(
        ) / "testingFiles" / "DataSetTrainPreprocessato.csv"
        pathTest = pathlib.Path(__file__).cwd() / \
            "testingFiles" / "DataSetTestPreprocessato.csv"
        pathPrediction = pathlib.Path(__file__).cwd(
        ) / "testingFiles" / "doPrediction.csv"
        features = utils.createFeatureList(2)
        token = '43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2'
        backendSelected = "ibmq_qasm_simulator"

        result = ClassificazioneControl.classify(
            pathTrain, pathTest, pathPrediction, features, token, backendSelected)
        self.assertNotEqual(result, 0)
        self.assertNotEqual(result, 1)
        self.assertTrue(exists(pathlib.Path(__file__).parent /
                        "testingFiles" / "classifiedFile.csv"))

    def test_classify_tokenFail(self):
        pathTrain = pathlib.Path(__file__).cwd(
        ) / "testingFiles" / "DataSetTrainPreprocessato.csv"
        pathTest = pathlib.Path(__file__).cwd() / \
            "testingFiles" / "DataSetTestPreprocessato.csv"
        pathPrediction = pathlib.Path(__file__).cwd(
        ) / "testingFiles" / "doPrediction.csv"
        features = utils.createFeatureList(2)
        token = 't0kenN0tV4l1d'
        backendSelected = "ibmq_qasm_simulator"

        result = ClassificazioneControl.classify(
            pathTrain, pathTest, pathPrediction, features, token, backendSelected)
        self.assertEqual(result, 0)
        self.assertNotEqual(result, 1)
        self.assertFalse(exists(pathlib.Path(__file__).parent /
                         "testingFiles" / "classifiedFile.csv"))

    def test_classify_ibmFail(self):
        pathTrain = pathlib.Path(__file__).cwd(
        ) / "testingFiles" / "DataSetTrainPreprocessato.csv"
        pathTest = pathlib.Path(__file__).cwd() / \
            "testingFiles" / "DataSetTestPreprocessato.csv"
        pathPrediction = pathlib.Path(
            __file__).cwd() / "testingFiles" / "bupa.csv"
        features = utils.createFeatureList(2)
        token = '43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2'
        backendSelected = "ibmq_qasm_simulator"

        result = ClassificazioneControl.classify(
            pathTrain, pathTest, pathPrediction, features, token, backendSelected)
        self.assertEqual(result, 1)
        self.assertNotEqual(result, 0)
        self.assertFalse(exists(pathlib.Path(__file__).parent /
                         "testingFiles" / "classifiedFile.csv"))

    def test_getClassifiedDataset(self):
        result = {"testing_accuracy": 0.55687446747,
                  "test_success_ratio": 0.4765984595, "totalTime": str(90.7)}
        open(pathlib.Path(__file__).parent /
             "testingFiles" / "classifiedFile.csv", "w")
        userpathtopredict = pathlib.Path(
            __file__).cwd() / "testingFiles" / "doPrediction.csv"

        value = ClassificazioneControl.getClassifiedDataset(
            result, userpathtopredict, "quantumoonlight@gmail.com")
        self.assertEqual(value, 1)

    def tearDown(self):
        if(os.path.exists(pathlib.Path(__file__).parent / "testingFiles" / "classifiedFile.csv")):
            os.remove(pathlib.Path(__file__).parent /
                      "testingFiles" / "classifiedFile.csv")
