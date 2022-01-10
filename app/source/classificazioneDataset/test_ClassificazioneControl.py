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
    def setUp(self):
       current_user = User(email="boscoverde27@gmail.com", password="prosopagnosia", username="Antonio de Curtis",
                         name="Antonio", surname="De Curtis", token="43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2")
       self.assertTrue(current_user.is_authenticated)


    def test_ClassificazioneControl(self):
        tester = app.test_client(self)
        pathTrain = pathlib.Path(__file__).cwd() / "testingFiles" / "DataSetTrainPreprocessato.csv"
        pathTest = pathlib.Path(__file__).cwd() / "testingFiles" / "DataSetTestPreprocessato.csv"
        pathPrediction = pathlib.Path(__file__).cwd() / "testingFiles" / "doPrediction.csv"
        features = utils.createFeatureList(2)
        token = '43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2'
        backend = "ibmq_qasm_simulator"

        response = tester.post(
            '/classificazioneControl',
            data=dict(pathTrain=pathTrain, pathTest=pathTest,
                      pathPrediction=pathPrediction, features=features,
                      token=token, backend=backend))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(exists(pathlib.Path(__file__).parents[3] / "upload_dataset" / "classifiedFile.csv"))


    def test_classify(self):
        #tester = app.test_client(self)
        pathTrain = pathlib.Path(__file__).cwd() / "testingFiles" / "DataSetTrainPreprocessato.csv"
        pathTest = pathlib.Path(__file__).cwd() / "testingFiles" / "DataSetTestPreprocessato.csv"
        pathPrediction = pathlib.Path(__file__).cwd() / "testingFiles" / "doPrediction.csv"
        features = utils.createFeatureList(2)
        token = '43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2'
        backendSelected = "ibmq_qasm_simulator"

        result = ClassificazioneControl.classify(pathTrain, pathTest, pathPrediction, features, token, backendSelected)
        self.assertNotEqual(result, 0)
        self.assertNotEqual(result, 1)
        #self.assertTrue(isinstance(result, dict))
        self.assertTrue(exists(pathlib.Path(__file__).parents[3] / "upload_dataset" / "classifiedFile.csv"))


    def test_classify_tokenFail(self):
        #tester = app.test_client(self)
        pathTrain = pathlib.Path(__file__).cwd() / "testingFiles" / "DataSetTrainPreprocessato.csv"
        pathTest = pathlib.Path(__file__).cwd() / "testingFiles" / "DataSetTestPreprocessato.csv"
        pathPrediction = pathlib.Path(__file__).cwd() / "testingFiles" / "doPrediction.csv"
        features = utils.createFeatureList(2)
        token = 't0kenN0tV4l1d'
        backendSelected = "ibmq_qasm_simulator"

        result = ClassificazioneControl.classify(pathTrain, pathTest, pathPrediction, features, token, backendSelected)
        self.assertEqual(result, 0)
        self.assertNotEqual(result, 1)


    def test_classify_ibmFail(self):
        #tester = app.test_client(self)
        pathTrain = pathlib.Path(__file__).cwd() / "testingFiles" / "DataSetTrainPreprocessato.csv"
        pathTest = pathlib.Path(__file__).cwd() / "testingFiles" / "DataSetTestPreprocessato.csv"
        pathPrediction = pathlib.Path(__file__).cwd() / "testingFiles" / "bupa.csv"
        features = utils.createFeatureList(2)
        token = '43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2'
        backendSelected = "ibmq_qasm_simulator"

        result = ClassificazioneControl.classify(pathTrain, pathTest, pathPrediction, features, token, backendSelected)
        self.assertEqual(result, 1)
        self.assertNotEqual(result, 0)
        self.assertFalse(exists(pathlib.Path(__file__).parents[3] / "upload_dataset" / "classifiedFile.csv"))


    def test_getClassifiedDataset(self):
        result={}
        result["testing_accuracy"]=0.55687446747
        result["test_success_ratio"] =0.4765984595
        result["totalTime"]=str(90.7)
        open( pathlib.Path(__file__).parents[3] / "upload_dataset" / "classifiedFile.csv", "w")

        value = ClassificazioneControl.getClassifiedDataset(result)
        self.assertEqual(value, 1)


    def tearDown(self):
        if(os.path.exists(pathlib.Path(__file__).parents[3] / "upload_dataset" / "classifiedFile.csv")):
            os.remove(pathlib.Path(__file__).parents[3] / "upload_dataset" / "classifiedFile.csv")








