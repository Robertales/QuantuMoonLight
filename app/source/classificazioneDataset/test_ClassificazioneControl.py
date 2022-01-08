import pathlib
import unittest
from os.path import exists

from flask_login import current_user
from app.models import User
from app import app
from app.source.utils import utils
from pathlib import Path

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
        numCols = utils.numberOfColumns(pathTrain)
        features = utils.createFeatureList(numCols - 1)
        token = '43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2'
        backend = "ibmq_qasm_simulator"

        #fileTrain = open(pathTrain, "r")
        #fileTest = open(pathTest, "r")
        #filePrediction = open(pathPrediction, "r")

        response = tester.post(
            '/classificazioneControl',
            data=dict(pathTrain=pathTrain, pathTest=pathTest,
                      userpathToPredict=pathPrediction, features=features,
                      token=token, backend=backend))
        statuscode = response.status_code
        result = response.get_data()
        self.assertEqual(statuscode, 200)
        self.assertTrue(exists("upload_dataset" / "classifiedFile.csv")
)
