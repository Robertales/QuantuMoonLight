import os
import pathlib
import unittest
from os.path import exists
from app.models import User
from app import app


class TestPreprocessingControl(unittest.TestCase):
    def setUp(self):
        # path del dataset a disposizione del testing
        pathOrigin = pathlib.Path(__file__).parents[0] / "testingFiles"
        # path della cartella dove scrivere i files che verranno letti dai test
        pathMock = pathlib.Path(__file__).parents[0]

        f = open((pathMock / "Data_testing.csv").__str__(), "a+")
        g = open((pathOrigin / "Data_testing.csv").__str__(), "r")
        contents = g.read()
        f.write(contents)
        f.close()
        g.close()

        f = open((pathMock / "Data_training.csv").__str__(), "a+")
        g = open((pathOrigin / "Data_training.csv").__str__(), "r")
        contents = g.read()
        f.write(contents)
        f.close()
        g.close()

        f = open((pathMock / "bupa.csv").__str__(), "a+")
        g = open((pathOrigin / "bupa.csv").__str__(), "r")
        contents = g.read()
        f.write(contents)
        f.close()
        g.close()

        f = open((pathMock / "bupaToPredict.csv").__str__(), "a+")
        g = open((pathOrigin / "bupaToPredict.csv").__str__(), "r")
        contents = g.read()
        f.write(contents)
        f.close()
        g.close()

        self.assertTrue(exists(pathMock / "Data_training.csv"))
        self.assertTrue(exists(pathMock / "Data_training.csv"))
        self.assertTrue(exists(pathMock / "bupa.csv"))
        self.assertTrue(exists(pathMock / "bupaToPredict.csv"))

    def test_PreprocessingControl_onlyQSVM(self):
        """
        Tests when the user wants to execute classification but no Preprocessing.
        Check if exists the two dataset to classify
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "bupa.csv"
        userpathToPredict = (
            pathlib.Path(__file__).parents[0] / "bupaToPredict.csv"
        )
        prototypeSelection = None
        featureExtraction = None
        numRowsPS = 10
        numColsFE = 2
        doQSVM = True

        response = tester.post(
            "/preprocessingControl",
            data=dict(
                userpath=userpath,
                userpathToPredict=userpathToPredict,
                prototypeSelection=prototypeSelection,
                featureExtraction=featureExtraction,
                numRawsPS=numRowsPS,
                numColsFE=numColsFE,
                doQSVM=doQSVM,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

        pathMock = pathlib.Path(__file__).parents[0]
        self.assertTrue(exists(pathMock / "DataSetTrainPreprocessato.csv"))
        self.assertTrue(exists(pathMock / "DataSetTestPreprocessato.csv"))

    def test_PreprocessingControl_onlyPS(self):
        """
        Test when the user wants to execute only Prototype Selection on the training dataset.
        Check if exist the two dataset to classify and the reduced Train
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "bupa.csv"
        userpathToPredict = None
        prototypeSelection = True
        featureExtraction = None
        numRowsPS = 10
        numColsFE = 2
        doQSVM = None

        response = tester.post(
            "/preprocessingControl",
            data=dict(
                userpath=userpath,
                userpathToPredict=userpathToPredict,
                prototypeSelection=prototypeSelection,
                featureExtraction=featureExtraction,
                numRawsPS=numRowsPS,
                numColsFE=numColsFE,
                doQSVM=doQSVM,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

        pathMock = pathlib.Path(__file__).parents[0]
        self.assertTrue(exists(pathMock / "DataSetTrainPreprocessato.csv"))
        self.assertTrue(exists(pathMock / "DataSetTestPreprocessato.csv"))
        self.assertTrue(exists(pathMock / "reducedTrainingPS.csv"))

    def test_PreprocessingControl_failPS(self):
        """
        Test when the user wants to execute only Prototype Selection on the training dataset,
        but try to reduce the rows whit more rows then the original DataSet
        Check if the two dataset are not created
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "bupa.csv"
        userpathToPredict = None
        prototypeSelection = True
        featureExtraction = None
        numRowsPS = 100000
        numColsFE = 2
        doQSVM = None

        response = tester.post(
            "/preprocessingControl",
            data=dict(
                userpath=userpath,
                userpathToPredict=userpathToPredict,
                prototypeSelection=prototypeSelection,
                featureExtraction=featureExtraction,
                numRawsPS=numRowsPS,
                numColsFE=numColsFE,
                doQSVM=doQSVM,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

        pathData = pathlib.Path(__file__).parents[0]
        self.assertFalse(exists(pathData / "DataSetTrainPreprocessato.csv"))
        self.assertFalse(exists(pathData / "DataSetTestPreprocessato.csv"))
        self.assertFalse(exists(pathData / "reducedTrainingPS.csv"))

    def test_PreprocessingControl_onlyFE(self):
        """
        Test when the user wants to execute only Feature Extraction on the training and testing dataset.
        Check if exist the two dataset to classify and the reduced Train and Test
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "bupa.csv"
        userpathToPredict = None
        prototypeSelection = None
        featureExtraction = True
        numRowsPS = 10
        numColsFE = 2
        doQSVM = None

        response = tester.post(
            "/preprocessingControl",
            data=dict(
                userpath=userpath,
                userpathToPredict=userpathToPredict,
                prototypeSelection=prototypeSelection,
                featureExtraction=featureExtraction,
                numRawsPS=numRowsPS,
                numColsFE=numColsFE,
                doQSVM=doQSVM,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

        pathData = pathlib.Path(__file__).parents[0]
        self.assertTrue(exists(pathData / "DataSetTrainPreprocessato.csv"))
        self.assertTrue(exists(pathData / "DataSetTestPreprocessato.csv"))
        self.assertTrue(exists(pathData / "yourPCA_Train.csv"))
        self.assertTrue(exists(pathData / "yourPCA_Test.csv"))

    def test_PreprocessingControl_failFE(self):
        """
        Test when the user wants to execute only Feature Extraction on the training and testing dataset,
        but try to reduce the columns whit more columns then the original DataSet
        Check if the two dataset are not created
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "bupa.csv"
        userpathToPredict = None
        prototypeSelection = None
        featureExtraction = True
        numRowsPS = 10
        numColsFE = 15
        doQSVM = None

        response = tester.post(
            "/preprocessingControl",
            data=dict(
                userpath=userpath,
                userpathToPredict=userpathToPredict,
                prototypeSelection=prototypeSelection,
                featureExtraction=featureExtraction,
                numRawsPS=numRowsPS,
                numColsFE=numColsFE,
                doQSVM=doQSVM,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

        pathData = pathlib.Path(__file__).parents[0]
        self.assertFalse(exists(pathData / "DataSetTrainPreprocessato.csv"))
        self.assertFalse(exists(pathData / "DataSetTestPreprocessato.csv"))
        self.assertFalse(exists(pathData / "yourPCA_Train.csv"))
        self.assertFalse(exists(pathData / "yourPCA_Test.csv"))

    def test_PreprocessingControl_FE_PS(self):
        """
        Test when the user wants to execute Feature Extraction on the training and testing dataset
        and Prototype Selection on the training dataset.
        Check if exist the two dataset to classify and the reduced Train and Test
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "bupa.csv"
        userpathToPredict = None
        prototypeSelection = True
        featureExtraction = True
        numRawsPS = 10
        numColsFE = 2
        doQSVM = None

        response = tester.post(
            "/preprocessingControl",
            data=dict(
                userpath=userpath,
                userpathToPredict=userpathToPredict,
                prototypeSelection=prototypeSelection,
                featureExtraction=featureExtraction,
                numRawsPS=numRawsPS,
                numColsFE=numColsFE,
                doQSVM=doQSVM,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

        pathData = pathlib.Path(__file__).parents[0]
        self.assertTrue(exists(pathData / "DataSetTrainPreprocessato.csv"))
        self.assertTrue(exists(pathData / "DataSetTestPreprocessato.csv"))
        self.assertTrue(exists(pathData / "reducedTrainingPS.csv"))
        self.assertTrue(exists(pathData / "yourPCA_Train.csv"))
        self.assertTrue(exists(pathData / "yourPCA_Test.csv"))

    def test_PreprocessingControl_FE_QSVM(self):
        """
        Test when the user wants to execute Feature Extraction on the training and testing dataset
        and classification.
        Check if exist the two dataset to classify, the reduced Train and Test
        and the reduced dataset to predict
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "bupa.csv"
        userpathToPredict = (
            pathlib.Path(__file__).parents[0] / "bupaToPredict.csv"
        )
        prototypeSelection = None
        featureExtraction = True
        numRawsPS = 10
        numColsFE = 2
        doQSVM = True

        response = tester.post(
            "/preprocessingControl",
            data=dict(
                userpath=userpath,
                userpathToPredict=userpathToPredict,
                prototypeSelection=prototypeSelection,
                featureExtraction=featureExtraction,
                numRawsPS=numRawsPS,
                numColsFE=numColsFE,
                doQSVM=doQSVM,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

        pathData = pathlib.Path(__file__).parents[0]
        self.assertTrue(exists(pathData / "DataSetTrainPreprocessato.csv"))
        self.assertTrue(exists(pathData / "DataSetTestPreprocessato.csv"))
        self.assertTrue(exists(pathData / "yourPCA_Train.csv"))
        self.assertTrue(exists(pathData / "yourPCA_Test.csv"))
        self.assertTrue(exists(pathData / "doPredictionFE.csv"))

    def tearDown(self):
        """
        Remove all the files created
        """
        directory = pathlib.Path(__file__).parents[0]
        allFiles = os.listdir(directory)
        csvFiles = [file for file in allFiles if file.endswith(".csv")]
        for file in csvFiles:
            path = os.path.join(directory, file)
            os.remove(path)
