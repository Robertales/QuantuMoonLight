import datetime
import hashlib
import os
import pathlib
import unittest
import warnings
from datetime import datetime
from os.path import exists
from unittest import TestCase

from flask_login import UserMixin, AnonymousUserMixin
from flask_login import current_user
from sqlalchemy import desc
from sqlalchemy_utils import database_exists, create_database

from app import app
from app import db
from app.source.model.models import Article, Dataset
from app.source.model.models import User
from app.source.utils import utils
from app.source.validazioneDataset import kFoldValidation
from app.source.validazioneDataset import train_testSplit
from app.source.classificazioneDataset.ClassifyControl import ClassificazioneControl

warnings.filterwarnings("ignore", category=DeprecationWarning)


class TestValidazioneControl(unittest.TestCase):
    def setUp(self):
        # path del dataset a disposizione del testing
        pathOrigin = pathlib.Path(__file__).parents[0] / "testingFiles"
        # path della cartella dove scrivere i files che verranno letti dai test
        pathMock = pathlib.Path(__file__).parents[0]

        f = open((pathMock / "bupa.csv").__str__(), "a+")
        g = open((pathOrigin / "bupa.csv").__str__(), "r")
        contents = g.read()
        f.write(contents)
        f.close()
        g.close()

        self.assertTrue(exists(pathMock / "bupa.csv"))

    def test_ValidazioneControl_SimpleSplit(self):
        """
        Tests when the user wants to validate a dataset with SimpleSplit and checks if the new datasets exist
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "bupa.csv"
        userpathTest = None
        simpleSplit = True
        kFold = None
        k = 10

        response = tester.post(
            "/validazioneControl",
            data=dict(
                userpath=userpath,
                userpathTest=userpathTest,
                simpleSplit=simpleSplit,
                kFold=kFold,
                k=k,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        pathData = pathlib.Path(__file__).parents[0]
        self.assertTrue(exists(pathData / "Data_training.csv"))
        self.assertTrue(exists(pathData / "Data_testing.csv"))
        self.assertTrue(exists(pathData / "featureDataset.csv"))

    def test_ValidazioneControl_KFold(self):
        """
        Tests when the user wants to validate a dataset with kFold and checks if the new datasets exist
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "bupa.csv"
        userpathTest = None
        simpleSplit = None
        kFold = True
        k = 10

        response = tester.post(
            "/validazioneControl",
            data=dict(
                userpath=userpath,
                userpathTest=userpathTest,
                simpleSplit=simpleSplit,
                kFold=kFold,
                k=k,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        pathData = pathlib.Path(__file__).parents[0]

        for x in range(k):
            StringaTrain = "training_fold_{}.csv".format(x + 1)
            StringaTest = "testing_fold_{}.csv".format(x + 1)
            self.assertTrue(exists(pathData / StringaTrain))
            self.assertTrue(exists(pathData / StringaTest))

    def test_ValidazioneControl_kFold_Fail(self):
        """
        Tests when the user wants to validate a dataset with kFold and the "k" value is not correct
        and checks if no new datasets exist
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "bupa.csv"
        userpathTest = None
        simpleSplit = None
        kFold = True
        k = 1

        response = tester.post(
            "/validazioneControl",
            data=dict(
                userpath=userpath,
                userpathTest=userpathTest,
                simpleSplit=simpleSplit,
                kFold=kFold,
                k=k,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        pathData = pathlib.Path(__file__).parents[0]
        StringaTrain = "training_fold_1.csv"
        StringaTest = "testing_fold_1.csv"
        self.assertFalse(exists(pathData / StringaTrain))
        self.assertFalse(exists(pathData / StringaTest))

    def test_ValidazioneControl_KFold_SimpleSplit(self):
        """
        Tests when the user wants to validate a dataset with kFold and SimpleSplit and
        checks if no new datasets exist because you can not validate a dataset with both kFold
        and SimpleSplit
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "bupa.csv"
        userpathTest = None
        simpleSplit = True
        kFold = True
        k = 10

        response = tester.post(
            "/validazioneControl",
            data=dict(
                userpath=userpath,
                userpathTest=userpathTest,
                simpleSplit=simpleSplit,
                kFold=kFold,
                k=k,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        pathData = pathlib.Path(__file__).parents[0]

        for x in range(k):
            StringaTrain = "training_fold_{}.csv".format(x + 1)
            StringaTest = "testing_fold_{}.csv".format(x + 1)
            self.assertFalse(exists(pathData / StringaTrain))
            self.assertFalse(exists(pathData / StringaTest))

        self.assertFalse(exists(pathData / "Data_training.csv"))
        self.assertFalse(exists(pathData / "Data_testing.csv"))
        self.assertFalse(exists(pathData / "featureDataset.csv"))

    def test_ValidazioneControl_NoSplit(self):
        """
        Tests when the user wants not to validate the dataset and has to upload both training and testing
        dataset and checks if the new name of the loaded datasets are Data_training.csv and Data_testing.csv
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "bupa.csv"
        userpathTest = pathlib.Path(__file__).parents[0] / "bupa.csv"
        simpleSplit = None
        kFold = None
        k = 10

        response = tester.post(
            "/validazioneControl",
            data=dict(
                userpath=userpath,
                userpathTest=userpathTest,
                simpleSplit=simpleSplit,
                kFold=kFold,
                k=k,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        pathData = pathlib.Path(__file__).parents[0]
        self.assertTrue(exists(pathData / "Data_training.csv"))
        self.assertTrue(exists(pathData / "Data_testing.csv"))

    def test_ValidazioneControl_NoSplit_Fail(self):
        """
        Tests when the user doesn't want to validate the dataset and has not uploaded the test Set
         and checks if no new datasets exist
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "bupa.csv"
        userpathTest = None
        simpleSplit = None
        kFold = None
        k = 10

        response = tester.post(
            "/validazioneControl",
            data=dict(
                userpath=userpath,
                userpathTest=userpathTest,
                simpleSplit=simpleSplit,
                kFold=kFold,
                k=k,
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        pathData = pathlib.Path(__file__).parents[0]

        self.assertFalse(exists(pathData / "Data_training.csv"))
        self.assertFalse(exists(pathData / "Data_testing.csv"))

    def tearDown(self):
        directory = pathlib.Path(__file__).parents[0]
        allFiles = os.listdir(directory)
        csvFiles = [file for file in allFiles if file.endswith(".csv")]
        for file in csvFiles:
            path = os.path.join(directory, file)
            os.remove(path)


class TestKFold(unittest.TestCase):
    def setUp(self):
        # path del dataset a disposizione del testing
        pathOrigin = pathlib.Path(__file__).parents[0] / "testingFiles"
        # path della cartella dove scrivere i files che verranno letti dai test
        pathMock = pathlib.Path(__file__).parents[0]

        f = open((pathMock / "bupa.csv").__str__(), "a+")
        g = open((pathOrigin / "bupa.csv").__str__(), "r")
        contents = g.read()
        f.write(contents)
        f.close()
        g.close()

        self.assertTrue(exists(pathMock / "bupa.csv"))

    def test_KFold(self):
        """
        Tests when the user wants to validate a dataset with kFold and checks if the new datasets exist
        """
        userpath = pathlib.Path(__file__).parents[0] / "bupa.csv"
        k = 10

        kFoldValidation.cross_fold_validation(userpath, k)
        pathData = pathlib.Path(__file__).parents[0]

        for x in range(k):
            StringaTrain = "training_fold_{}.csv".format(x + 1)
            StringaTest = "testing_fold_{}.csv".format(x + 1)
            self.assertTrue(exists(pathData / StringaTrain))
            self.assertTrue(exists(pathData / StringaTest))

    def tearDown(self):
        directory = pathlib.Path(__file__).parents[0]
        allFiles = os.listdir(directory)
        csvFiles = [file for file in allFiles if file.endswith(".csv")]
        for file in csvFiles:
            path = os.path.join(directory, file)
            os.remove(path)


class TestSimpleSplit(unittest.TestCase):
    def setUp(self):
        # path del dataset a disposizione del testing
        pathOrigin = pathlib.Path(__file__).parents[0] / "testingFiles"
        # path della cartella dove scrivere i files che verranno letti dai test
        pathMock = pathlib.Path(__file__).parents[0]

        f = open((pathMock / "bupa.csv").__str__(), "a+")
        g = open((pathOrigin / "bupa.csv").__str__(), "r")
        contents = g.read()
        f.write(contents)
        f.close()
        g.close()

        self.assertTrue(exists(pathMock / "bupa.csv"))

    def test_simpleSplit(self):
        """
        Tests when the user wants to validate a dataset with SimpleSplit.
        Checks if the new datasets exist and the new datasets have the correct number of rows
        """
        path = pathlib.Path(__file__).parent
        filename = path / "bupa.csv"
        numRaws = utils.numberOfRows(filename.__str__())

        train_testSplit.splitDataset(filename.__str__())
        self.assertEqual(20, utils.numberOfRows("Data_testing.csv"))
        self.assertEqual(
            numRaws - 20, utils.numberOfRows("Data_training.csv")
        )
        self.assertTrue(
            exists(pathlib.Path(__file__).parent / "Data_testing.csv")
        )
        self.assertTrue(
            exists(pathlib.Path(__file__).parent / "Data_training.csv")
        )

    def tearDown(self):
        path = pathlib.Path(__file__).parent
        os.remove(path / "Data_testing.csv")
        os.remove(path / "Data_training.csv")
        os.remove(path / "bupa.csv")


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


class Test_signup(TestCase):
    def setUp(self):
        super().setUp()
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "mysql://root@127.0.0.1/test_db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
            create_database(app.config["SQLALCHEMY_DATABASE_URI"])
        with app.app_context():
            db.create_all()

    def test_signup(self):
        """
        test the sign-up functionality of the website, creating a dummy  account and verifying it was correctly
        registered as a user
        """
        tester = app.test_client()
        response = tester.post(
            "/signup",
            data=dict(
                email="mariorossi12@gmail.com",
                password="Password123",
                confirmPassword="Password123",
                username="Antonio de Curtis ",
                token="43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2",
                nome="Antonio",
                cognome="De Curtis",
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(
            User.query.filter_by(email="mariorossi12@gmail.com").first()
        )
        db.session.commit()

    def test_signupInvalidToken(self):
        """
        test the sign-up functionality of the website, creating a dummy  account with an empty and verifying it was
        correctly registered as a user and the token was correctly parsed to Null
        """

        tester = app.test_client()
        response = tester.post(
            "/signup",
            data=dict(
                email="mariorossi12@gmail.com",
                password="Password123",
                confirmPassword="Password123",
                username="Antonio de Curtis ",
                token="0e906980a743e9313c848becb8810b2667535e188365e8db829e1c206421d1ec02360127de06b13013782ca87efc3b7487853aba99061df220b825adee92e316a57ef7a<f689eafea5",
                nome="Antonio",
                cognome="De Curtis",
            ),
        )
        print(response.get_data())
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user.token)
        db.session.commit()

    def test_signupInvalidUsername(self):
        """
        test the sign-up functionality of the website, creating a dummy  account with an empty username and verifying
        it wasn't correctly registered as a user
        """
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user)
        tester = app.test_client()
        response = tester.post(
            "/signup",
            data=dict(
                email="ADeCurtis123@gmail.com ",
                password="Password123",
                confirmPassword="Password123",
                nome="Antonio",
                cognome="De Curtis",
                token='0e906980a743e9313c848becb8810b2667535e188365e8db829e1c206421d1ec02360127de06b13013782ca87efc3b7487853aba99061df220b825adee92e316'
            ),
        )
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user)
        db.session.commit()

    def test_signupInvalidEmail(self):
        """
        test the sign-up functionality of the website, creating a dummy  account with an empty email and verifying it
        wasn't correctly registered as a user.
        """
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user)
        tester = app.test_client()
        response = tester.post(
            "/signup",
            data=dict(
                email="ADeCurtis123cfsdil.com ",
                password="Password123",
                confirmPassword="Password123",
                username="Antonio de Curtis ",
                nome="Antonio",
                cognome="De Curtis",
            ),
        )
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user)
        db.session.commit()

    def test_signupInvalidPassword(self):
        """
        test the sign-up functionality of the website, creating a dummy  account with an empty email and verifying it
        wasn't correctly registered as a user.
        """
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user)
        tester = app.test_client()
        response = tester.post(
            "/signup",
            data=dict(
                email="ADeCurtis123@gmail.com ",
                password="123456",
                confirmPassword="Password123",
                username="Antonio de Curtis ",
                nome="Antonio",
                cognome="De Curtis",
            ),
        )
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user)
        db.session.commit()

    def test_signupInvalidConfirmPassword(self):
        """
        test the sign-up functionality of the website, creating a dummy  account with an empty email and verifying it
        wasn't correctly registered as a user.
        """
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user)
        tester = app.test_client()
        response = tester.post(
            "/signup",
            data=dict(
                email="ADeCurtis123@gmail.com ",
                password="123456",
                confirmPassword="efkjhjefwikefji",
                username="Antonio de Curtis ",
                nome="Antonio",
                cognome="De Curtis",
            ),
        )
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user)
        db.session.commit()

    def test_signupInvalidName(self):
        """
        test the sign-up functionality of the website, creating a dummy  account with an empty username and verifying
        it wasn't correctly registered as a user
        """
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user)
        tester = app.test_client()
        response = tester.post(
            "/signup",
            data=dict(
                email="ADeCurtis123@gmail.com ",
                password="Password123",
                confirmPassword="Password123",
                nome="Antonio",
                cognome="",
                token='0e906980a743e9313c848becb8810b2667535e188365e8db829e1c206421d1ec02360127de06b13013782ca87efc3b7487853aba99061df220b825adee92e316'
            ),
        )
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user)
        db.session.commit()

    def test_signupInvalidSurName(self):
        """
        test the sign-up functionality of the website, creating a dummy  account with an empty username and verifying
        it wasn't correctly registered as a user
        """
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user)
        tester = app.test_client()
        response = tester.post(
            "/signup",
            data=dict(
                email="ADeCurtis123@gmail.com ",
                password="Password123",
                confirmPassword="Password123",
                nome="",
                cognome="De Curtis",
                token='0e906980a743e9313c848becb8810b2667535e188365e8db829e1c206421d1ec02360127de06b13013782ca87efc3b7487853aba99061df220b825adee92e316'
            ),
        )
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user)
        db.session.commit()

    def test_signupInvalidToken(self):
        """
        test the sign-up functionality of the website, creating a dummy  account with an empty username and verifying
        it wasn't correctly registered as a user
        """
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user)
        tester = app.test_client()
        response = tester.post(
            "/signup",
            data=dict(
                email="ADeCurtis123@gmail.com ",
                password="Password123",
                confirmPassword="Password123",
                nome="",
                cognome="De Curtis",
                token='0e906980a743e9313c848becb8810b2667535e188365e8db829e1c206421d1ec02360127de06b13013782ca87efc3b7487853aba99061df220b825adee92e316a57ef7a<f689eafea5 '
            ),
        )
        user = User.query.filter_by(email="mariorossi12@gmail.com").first()
        self.assertIsNone(user)
        db.session.commit()


    def tearDown(self):
        with app.app_context():
            db.drop_all()


class Test_Login_Logout(TestCase):
    def setUp(self):
        super().setUp()
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "mysql://root@127.0.0.1/test_db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
            create_database(app.config["SQLALCHEMY_DATABASE_URI"])
        with app.app_context():
            db.create_all()
            password = "quercia"
            password = hashlib.sha512(password.encode()).hexdigest()
            utente = User(
                email="boscoverde27@gmail.com",
                password=password,
                username="Antonio de Curtis",
                name="Antonio",
                surname="De Curtis",
                token="",
                isResearcher=False
            )
            db.session.add(utente)
            db.session.commit()

    def test_LoginLogout(self):
        """
        test the login functionality of the website,by trying to log in a predetermined and existing user account and
        then logging out
        """
        tester = app.test_client()
        self.assertFalse(current_user)
        with tester:
            response = tester.post(
                "/login",
                data=dict(email="boscoverde27@gmail.com", password="quercia"),
            )
            statuscode = response.status_code
            self.assertEqual(statuscode, 200)
            assert isinstance(current_user, User)
            self.assertTrue(current_user.is_authenticated)
            response = tester.post("/logout")
            statuscode = response.status_code
            self.assertEqual(statuscode, 200)
            self.assertFalse(current_user.is_authenticated)

    def test_loginUnregistered(self):
        tester = app.test_client()
        self.assertFalse(current_user)
        with tester:
            response = tester.post(
                "/login",
                data=dict(
                    email="emailsbagliata1234d@gmail.com",
                    password="quercia",
                ),
            )
            statuscode = response.status_code
            self.assertEqual(statuscode, 200)
            self.assertNotIsInstance(current_user, UserMixin)
            self.assertIsInstance(current_user, AnonymousUserMixin)
            self.assertFalse(current_user.is_authenticated)

    def test_loginWrongPassword(self):
        tester = app.test_client()
        self.assertFalse(current_user)
        with tester:
            response = tester.post(
                "/login",
                data=dict(
                    email="boscoverde27@gmail.com",
                    password="passwordsbagliata",
                ),
            )
            statuscode = response.status_code
            self.assertEqual(statuscode, 200)
            self.assertNotIsInstance(current_user, UserMixin)
            self.assertIsInstance(current_user, AnonymousUserMixin)
            self.assertFalse(current_user.is_authenticated)

    def test_Newsletter(self):
        tester = app.test_client()
        with tester:
            tester.post(
                "/login",
                data=dict(email="boscoverde27@gmail.com", password="quercia"),
            )
            assert isinstance(current_user, User)
            self.assertFalse(current_user.newsletter)
            response = tester.post(
                "/newsletter",
                data=dict(email="boscoverde27@gmail.com"),
            )
            statuscode = response.status_code
            self.assertEqual(statuscode, 200)
            self.assertTrue(current_user.newsletter)

    def tearDown(self):
        with app.app_context():
            db.drop_all()


class TestUser(TestCase):
    def setUp(self):
        super().setUp()
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "mysql://root@127.0.0.1/test_db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        tester = app.test_client(self)
        if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
            create_database(app.config["SQLALCHEMY_DATABASE_URI"])
        with app.app_context():
            db.create_all()
            user = User(
                email="mariorossi12@gmail.com",
                password="prosopagnosia",
                username="Antonio de Curtis ",
                name="Antonio",
                token="43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2",
                surname="De Curtis",
            )
            db.session.add(user)
            db.session.commit()

    def test_removeUser(self):
        tester = app.test_client(self)
        with app.app_context():
            db.create_all()
            self.assertTrue(
                User.query.filter_by(email="mariorossi12@gmail.com").first()
            )
            response = tester.post(
                "/removeUser/",
                data=dict(email="mariorossi12@gmail.com"),
            )
            statuscode = response.status_code
            self.assertEqual(statuscode, 200)
            self.assertFalse(
                User.query.filter_by(email="mariorossi12@gmail.com").first()
            )
            db.session.commit()

    def test_modifyUser(self):
        tester = app.test_client()
        with app.app_context():
            db.create_all()
        self.assertTrue(
            User.query.filter_by(email="mariorossi12@gmail.com").first()
        )
        response = tester.post(
            "/ModifyUser/",
            data=dict(
                email="mariorossi12@gmail.com",
                password="newPassword",
                username="newUsername ",
                nome="newName",
                cognome="newSurname",
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(
            User.query.filter_by(
                email="mariorossi12@gmail.com", username="newUsername"
            ).first()
        )
        db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all()


class TestList(TestCase):
    def setUp(self):
        super().setUp()
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "mysql://root@127.0.0.1/test_db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        tester = app.test_client(self)
        if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
            create_database(app.config["SQLALCHEMY_DATABASE_URI"])
        with app.app_context():
            db.create_all()
            user1 = User(
                email="mariorossi12@gmail.com",
                password="prosopagnosia",
                username="Antonio de Curtis ",
                name="Antonio",
                token="43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2",
                surname="De Curtis",
            )
            user2 = User(
                email="giuseppeverdi@gmail.com",
                password="asperger",
                username="giuVerdiProXX",
                name="Giuseppe",
                surname="Verdi",
            )
            art1 = Article(
                email_user="mariorossi12@gmail.com",
                title="BuonNatale",
                body="primobody",
                category="primaCat",
                data=datetime(2021, 12, 25),
            )
            art2 = Article(
                email_user="mariorossi12@gmail.com",
                title="BuonCapodanno",
                body="secondoBody",
                category="secondaCat",
                data=datetime(2022, 1, 1),
            )
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()
            db.session.add(art1)
            db.session.add(art2)
            db.session.commit()

    def test_listUser(self):
        tester = app.test_client()
        with app.app_context():
            db.create_all()
        self.assertTrue(
            User.query.filter_by(email="mariorossi12@gmail.com").first()
        )
        response = tester.post(
            "/gestione/",
            data=dict(scelta="listUser", email="mariorossi12@gmail.com"),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(
            User.query.filter_by(email="mariorossi12@gmail.com").first()
        )
        self.assertTrue(
            User.query.filter_by(email="giuseppeverdi@gmail.com").first()
        )
        db.session.commit()

    def test_listArticlesUser(self):
        tester = app.test_client()
        with app.app_context():
            db.create_all()
        response = tester.post(
            "/gestione/",
            data=dict(
                scelta="listArticlesUser",
                email="mariorossi12@gmail.com",
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(
            Article.query.filter_by(
                email_user="mariorossi12@gmail.com"
            ).limit(2)
        )
        db.session.commit()

    def test_listArticlesData(self):
        tester = app.test_client()
        with app.app_context():
            db.create_all()
        response = tester.post(
            "/gestione/",
            data=dict(
                scelta="listArticlesData",
                firstData="2021-12-20",
                secondData="2021-12-30",
            ),
        )
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertTrue(
            Article.query.filter(
                Article.data.between("2021-12-20", "2021-12-30")
            ).first()
        )
        db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all()


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
        control = ClassificazioneControl()
        result = control.classification_thread(path_train, path_test, path_prediction, features, token, backend_selected, email)

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
        control = ClassificazioneControl()
        print(token)
        print(backend_selected)
        result = control.classify(
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
        control = ClassificazioneControl()
        value = control.get_classified_dataset(
            result, user_path_to_predict, "quantumoonlight@gmail.com"
        )
        self.assertEqual(value, 1)

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
        control = ClassificazioneControl()
        result = control.classify(
            path_train,
            path_test,
            path_prediction,
            features,
            token,
            backend_selected,
        )
        self.assertEqual(result, 1)
        print(pathlib.Path(__file__).parent / "testingFiles" / "classifiedFile.csv")
        self.assertFalse(
            exists(
                pathlib.Path(__file__).parent
                / "testingFiles"
                / "classifiedFile.csv"
            )
        )

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


class TestRoutes(unittest.TestCase):
    def setUp(self):
        super().setUp()
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "mysql://root@127.0.0.1/test_db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
            create_database(app.config["SQLALCHEMY_DATABASE_URI"])
        with app.app_context():
            db.create_all()
            # Setup for login testing
            password = "quercia"
            password = hashlib.sha512(password.encode()).hexdigest()
            utente = User(
                email="boscoverde27@gmail.com",
                password=password,
                username="Antonio de Curtis",
                name="Antonio",
                surname="De Curtis",
                token=""
            )
            db.session.add(utente)
            db.session.commit()

    def test_routes(self):
        # Login User and test if that works
        tester = app.test_client()
        self.assertFalse(current_user)
        with tester:
            response = tester.post(
                "/login",
                data=dict(email="boscoverde27@gmail.com", password="quercia"),
            )
            statuscode = response.status_code
            self.assertEqual(statuscode, 200)
            assert isinstance(current_user, User)
            self.assertTrue(current_user.is_authenticated)
            print(current_user)
            simpleSplit = True
            prototypeSelection = True
            featureExtraction = True
            numRowsPS = 10
            numColsFE = 2
            doQSVM = True
            token = "43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2"
            backend = "ibmq_qasm_simulator"
            email = "quantumoonlight@gmail.com"

            path = pathlib.Path(__file__).parent
            pathpred = path / "testingFiles" / "bupaToPredict.csv"
            pathtrain = path / "testingFiles" / "bupa.csv"

            # Test smista with that the whole
            # validation/preprocessing/classification process
            response = tester.post(
                "/formcontrol",
                data=dict(
                    dataset_train=open(pathtrain.__str__(), "rb"),
                    dataset_test=open(pathpred.__str__(), "rb"),
                    dataset_prediction=open(pathpred.__str__(), "rb"),
                    splitDataset=True,
                    reducePS=prototypeSelection,
                    reduceFE=featureExtraction,
                    doQSVM=doQSVM,
                    simpleSplit=simpleSplit,
                    nrRows=numRowsPS,
                    nrColumns=numColsFE,
                    backend=backend,
                    token=token,
                    email=email,


                ),
            )

            statuscode = response.status_code
            print(statuscode)
            self.assertEqual(statuscode, 200)
            pathData = pathlib.Path(__file__).parents[3] / "upload_dataset" / current_user.email / str(
                Dataset.query.filter_by(
                    email_user=current_user.email).order_by(
                    desc(
                        Dataset.id)).first().id)  # Find a way to get the id
            self.assertTrue(exists(pathData / "Data_training.csv"))
            self.assertTrue(exists(pathData / "Data_testing.csv"))
            self.assertTrue(exists(pathData / "featureDataset.csv"))
            self.assertTrue(exists(pathData / "DataSetTrainPreprocessato.csv"))
            self.assertTrue(exists(pathData / "DataSetTestPreprocessato.csv"))
            self.assertTrue(exists(pathData / "reducedTrainingPS.csv"))
            self.assertTrue(exists(pathData / "yourPCA_Train.csv"))
            self.assertTrue(exists(pathData / "yourPCA_Test.csv"))

    def tearDown(self):
        directory = pathlib.Path(__file__).parents[0]
        allFiles = os.listdir(directory)
        csvFiles = [file for file in allFiles if file.endswith(".csv")]
        for file in csvFiles:
            path = os.path.join(directory, file)
            os.remove(path)
        with app.app_context():
            db.drop_all()


