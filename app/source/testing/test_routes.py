import os
import pathlib
import unittest
from os.path import exists
from app import app
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


class TestRoutes(unittest.TestCase):
    def testSmista_NoOp(self):
        tester = app.test_client(self)

        path = pathlib.Path(__file__).parent
        pathtrain = path / "testingFiles" / "bupaTrain.csv"
        pathtest = path / "testingFiles" / "bupaTest.csv"
        pathpred = path / "testingFiles" / "bupaToPredict.csv"

        response = tester.post(
            "/formcontrol",
            data=dict(
                dataset_train=open(pathtrain.__str__(), "rb"),
                dataset_test=open(pathtest.__str__(), "rb"),
                dataset_prediction=open(pathpred.__str__(), "rb"),
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def testSmista_AutoSplitDefault(self):
        tester = app.test_client(self)

        path = pathlib.Path(__file__).parent
        pathtrain = path / "testingFiles" / "bupaTrain.csv"
        pathtest = path / "testingFiles" / "bupaTest.csv"
        pathpred = path / "testingFiles" / "bupaToPredict.csv"
        autosplit = "doAutosplit"

        response = tester.post(
            "/formcontrol",
            data=dict(
                dataset_train=open(pathtrain.__str__(), "rb"),
                dataset_test=open(pathtest.__str__(), "rb"),
                dataset_prediction=open(pathpred.__str__(), "rb"),
                splitDataset=autosplit,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertFalse(exists(path / "Data_training.csv"))
        self.assertFalse(exists(path / "Data_testing.csv"))
        self.assertFalse(exists(path / "featureDataset.csv"))

    def testSmista_kFold(self):
        tester = app.test_client(self)

        path = pathlib.Path(__file__).parent
        pathtrain = path / "testingFiles" / "bupaTrain.csv"
        pathtest = path / "testingFiles" / "bupaTest.csv"
        pathpred = path / "testingFiles" / "bupaToPredict.csv"
        autosplit = "doAutosplit"
        kFold = "doKfold"
        # Advanced option
        k = 10

        response = tester.post(
            "/formcontrol",
            data=dict(
                dataset_train=open(pathtrain.__str__(), "rb"),
                dataset_test=open(pathtest.__str__(), "rb"),
                dataset_prediction=open(pathpred.__str__(), "rb"),
                splitDataset=autosplit,
                kFold=kFold,
                kFoldValue=k,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        for x in range(k):
            StringaTrain = "training_fold_{}.csv".format(x + 1)
            StringaTest = "testing_fold_{}.csv".format(x + 1)
            self.assertTrue(exists(path / StringaTrain))
            self.assertTrue(exists(path / StringaTest))

    def testSmista_QSVM_noFE(self):
        # DA CONTROLLARE! problemi con classificazione
        tester = app.test_client(self)

        path = pathlib.Path(__file__).parent
        pathtrain = path / "testingFiles" / "bupaTrain.csv"
        pathtest = path / "testingFiles" / "bupaTest.csv"
        pathpred = path / "testingFiles" / "bupaToPredict.csv"
        doQSVM = "doQSVM"
        response = tester.post(
            "/formcontrol",
            data=dict(
                dataset_train=open(pathtrain.__str__(), "rb"),
                dataset_test=open(pathtest.__str__(), "rb"),
                dataset_prediction=open(pathpred.__str__(), "rb"),
                doQSVM=doQSVM,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def testSmista_QSVM_FE(self):
        # DA CONTROLLARE! problemi con classificazione
        tester = app.test_client(self)

        path = pathlib.Path(__file__).parent
        pathtrain = path / "testingFiles" / "bupaTrain.csv"
        pathtest = path / "testingFiles" / "bupaTest.csv"
        pathpred = path / "testingFiles" / "bupaToPredict.csv"
        featureExtraction = "reduceFE"
        doQSVM = "doQSVM"
        # Advanced option
        numColsFE = 2

        response = tester.post(
            "/formcontrol",
            data=dict(
                dataset_train=open(pathtrain.__str__(), "rb"),
                dataset_test=open(pathtest.__str__(), "rb"),
                dataset_prediction=open(pathpred.__str__(), "rb"),
                reduceFE=featureExtraction,
                doQSVM=doQSVM,
                nrColumns=numColsFE,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def testSmista_failUpload(self):
        # DA CONTROLLARE! l'esecuzione non si ferma dopo il tentativo di upload
        tester = app.test_client(self)

        path = pathlib.Path(__file__).parent
        pathtrain = path / "testingFiles" / "bupaFail.fail"
        pathtest = path / "testingFiles" / "bupaFail.fail"
        pathpred = path / "testingFiles" / "bupaFail.fail"
        featureExtraction = "reduceFE"
        doQSVM = "doQSVM"
        # Advanced option
        numColsFE = 2

        response = tester.post(
            "/formcontrol",
            data=dict(
                dataset_train=open(pathtrain.__str__(), "rb"),
                dataset_test=open(pathtest.__str__(), "rb"),
                dataset_prediction=open(pathpred.__str__(), "rb"),
                reduceFE=featureExtraction,
                doQSVM=doQSVM,
                nrColumns=numColsFE,
            ),
        )
        statuscode = response.status_code
        print(statuscode)
        self.assertEqual(statuscode, 400)

    def tearDown(self):
        directory = pathlib.Path(__file__).parents[0]
        allFiles = os.listdir(directory)
        csvFiles = [file for file in allFiles if file.endswith(".csv")]
        for file in csvFiles:
            path = os.path.join(directory, file)
            os.remove(path)
