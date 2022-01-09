import os
import pathlib
import unittest
from os.path import exists
from app.models import User
from app import app


class TestPreprocessingControl(unittest.TestCase):

    def setUp(self):
        current_user = User(email="boscoverde27@gmail.com", password="prosopagnosia", username="Antonio de Curtis",
                            name="Antonio", surname="De Curtis",
                            token="43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2")
        self.assertTrue(current_user.is_authenticated)

        # path del dataset a disposizione del testing
        pathOrigin = pathlib.Path(__file__).parents[0] / 'testingFiles'
        # path della cartella dell'utente Totò, dove creare i files
        # al momento è la directory del progetto
        pathMock = pathlib.Path(__file__).parents[0]

        f = open((pathMock / 'Data_testing.csv').__str__(), "a+")
        g = open((pathOrigin / 'Data_testing.csv').__str__(), "r")
        contents = g.read()
        f.write(contents)
        f.close()
        g.close()

        f = open((pathMock / 'Data_training.csv').__str__(), "a+")
        g = open((pathOrigin / 'Data_training.csv').__str__(), "r")
        contents = g.read()
        f.write(contents)
        f.close()
        g.close()

        self.assertTrue(exists(pathMock / "Data_training.csv"))
        self.assertTrue(exists(pathMock / "Data_training.csv"))

    def test_PreprocessingControl_onlyQSVM(self):
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathToPredict = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupaToPredict.csv"
        prototypeSelection = None
        featureExtraction = None
        numRawsPS = 10
        numColsFE = 2
        doQSVM = True

        response = tester.post("/preprocessingControl",
                               data=dict(userpath=userpath, userpathToPredict=userpathToPredict,
                                         prototypeSelection=prototypeSelection,
                                         featureExtraction=featureExtraction,
                                         numRawsPS=numRawsPS, numColsFE=numColsFE, doQSVM=doQSVM))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

        pathMock = pathlib.Path(__file__).parents[0]
        self.assertTrue(exists(pathMock / 'DataSetTrainPreprocessato.csv'))
        self.assertTrue(exists(pathMock / 'DataSetTestPreprocessato.csv'))

    def test_PreprocessingControl_onlyPS(self):
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathToPredict = None
        prototypeSelection = True
        featureExtraction = None
        numRawsPS = 10
        numColsFE = 2
        doQSVM = None

        response = tester.post("/preprocessingControl",
                               data=dict(userpath=userpath, userpathToPredict=userpathToPredict,
                                         prototypeSelection=prototypeSelection,
                                         featureExtraction=featureExtraction,
                                         numRawsPS=numRawsPS, numColsFE=numColsFE, doQSVM=doQSVM))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

        pathMock = pathlib.Path(__file__).parents[0]
        self.assertTrue(exists(pathMock / 'DataSetTrainPreprocessato.csv'))
        self.assertTrue(exists(pathMock / 'DataSetTestPreprocessato.csv'))
        self.assertTrue(exists(pathMock / 'reducedTrainingPS.csv'))

    def test_PreprocessingControl_failPS(self):
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathToPredict = None
        prototypeSelection = True
        featureExtraction = None
        numRawsPS = 100000
        numColsFE = 2
        doQSVM = None

        response = tester.post("/preprocessingControl",
                               data=dict(userpath=userpath, userpathToPredict=userpathToPredict,
                                         prototypeSelection=prototypeSelection,
                                         featureExtraction=featureExtraction,
                                         numRawsPS=numRawsPS, numColsFE=numColsFE, doQSVM=doQSVM))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

        pathData = pathlib.Path(__file__).parents[0]
        self.assertFalse(exists(pathData / 'DataSetTrainPreprocessato.csv'))
        self.assertFalse(exists(pathData / 'DataSetTestPreprocessato.csv'))
        self.assertFalse(exists(pathData / 'reducedTrainingPS.csv'))

    def test_PreprocessingControl_onlyFE(self):
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathToPredict = None
        prototypeSelection = None
        featureExtraction = True
        numRawsPS = 10
        numColsFE = 2
        doQSVM = None

        response = tester.post("/preprocessingControl",
                               data=dict(userpath=userpath, userpathToPredict=userpathToPredict,
                                         prototypeSelection=prototypeSelection,
                                         featureExtraction=featureExtraction,
                                         numRawsPS=numRawsPS, numColsFE=numColsFE, doQSVM=doQSVM))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

        pathData = pathlib.Path(__file__).parents[0]
        self.assertTrue(exists(pathData / 'DataSetTrainPreprocessato.csv'))
        self.assertTrue(exists(pathData / 'DataSetTestPreprocessato.csv'))
        self.assertTrue(exists(pathData / 'yourPCA_Train.csv'))
        self.assertTrue(exists(pathData / 'yourPCA_Test.csv'))

    def test_PreprocessingControl_failFE(self):
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathToPredict = None
        prototypeSelection = None
        featureExtraction = True
        numRawsPS = 10
        numColsFE = 15
        doQSVM = None

        response = tester.post("/preprocessingControl",
                               data=dict(userpath=userpath, userpathToPredict=userpathToPredict,
                                         prototypeSelection=prototypeSelection,
                                         featureExtraction=featureExtraction,
                                         numRawsPS=numRawsPS, numColsFE=numColsFE, doQSVM=doQSVM))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

        pathData = pathlib.Path(__file__).parents[0]
        self.assertFalse(exists(pathData / 'DataSetTrainPreprocessato.csv'))
        self.assertFalse(exists(pathData / 'DataSetTestPreprocessato.csv'))
        self.assertFalse(exists(pathData / 'yourPCA_Train.csv'))
        self.assertFalse(exists(pathData / 'yourPCA_Test.csv'))

    def test_PreprocessingControl_FE_PS(self):
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathToPredict = None
        prototypeSelection = True
        featureExtraction = True
        numRawsPS = 10
        numColsFE = 2
        doQSVM = None

        response = tester.post("/preprocessingControl",
                               data=dict(userpath=userpath, userpathToPredict=userpathToPredict,
                                         prototypeSelection=prototypeSelection,
                                         featureExtraction=featureExtraction,
                                         numRawsPS=numRawsPS, numColsFE=numColsFE, doQSVM=doQSVM))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

        pathData = pathlib.Path(__file__).parents[0]
        self.assertTrue(exists(pathData / 'DataSetTrainPreprocessato.csv'))
        self.assertTrue(exists(pathData / 'DataSetTestPreprocessato.csv'))
        self.assertTrue(exists(pathData / 'reducedTrainingPS.csv'))
        self.assertTrue(exists(pathData / 'yourPCA_Train.csv'))
        self.assertTrue(exists(pathData / 'yourPCA_Test.csv'))

    def test_PreprocessingControl_FE_QSVM(self):
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathToPredict = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupaToPredict.csv"
        prototypeSelection = None
        featureExtraction = True
        numRawsPS = 10
        numColsFE = 2
        doQSVM = True

        response = tester.post("/preprocessingControl",
                               data=dict(userpath=userpath, userpathToPredict=userpathToPredict,
                                         prototypeSelection=prototypeSelection,
                                         featureExtraction=featureExtraction,
                                         numRawsPS=numRawsPS, numColsFE=numColsFE, doQSVM=doQSVM))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

        pathData = pathlib.Path(__file__).parents[0]
        self.assertTrue(exists(pathData / 'DataSetTrainPreprocessato.csv'))
        self.assertTrue(exists(pathData / 'DataSetTestPreprocessato.csv'))
        self.assertTrue(exists(pathData / 'yourPCA_Train.csv'))
        self.assertTrue(exists(pathData / 'yourPCA_Test.csv'))
        self.assertTrue(exists(pathData / 'doPredictionFE.csv'))

    def tearDown(self):
        directory = pathlib.Path(__file__).parents[0]
        allFiles = os.listdir(directory)
        csvFiles = [file for file in allFiles if file.endswith(".csv")]
        for file in csvFiles:
            path = os.path.join(directory, file)
            os.remove(path)
