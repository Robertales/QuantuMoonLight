import os
import pathlib
import unittest
from os.path import exists
from app.models import User
from app import app
from app.source.utils import utils
from app.source.validazioneDataset import kFoldValidation
from app.source.validazioneDataset import train_testSplit


class TestValidazioneControl(unittest.TestCase):
    def setUp(self):
        current_user = User(email="boscoverde27@gmail.com", password="prosopagnosia", username="Antonio de Curtis",
                            name="Antonio", surname="De Curtis",
                            token="43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2")
        self.assertTrue(current_user.is_authenticated)

    def test_ValidazioneControl_SimpleSplit(self):
        """
        Tests when the user wants to validate a dataset with SimpleSplit and checks if the new datasets exist
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathTest = None
        simpleSplit = True
        kFold = None
        k = 10

        response = tester.post('/validazioneControl',
                               data=dict(userpath=userpath, userpathTest=userpathTest,
                                         simpleSplit=simpleSplit, kFold=kFold, k=k))
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
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathTest = None
        simpleSplit = None
        kFold = True
        k = 10

        response = tester.post('/validazioneControl',
                               data=dict(userpath=userpath, userpathTest=userpathTest,
                                         simpleSplit=simpleSplit, kFold=kFold, k=k))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        pathData = pathlib.Path(__file__).parents[0]

        for x in range(k):
            StringaTrain = 'training_fold_{}.csv'.format(x + 1)
            StringaTest = 'testing_fold_{}.csv'.format(x + 1)
            self.assertTrue(exists(pathData / StringaTrain))
            self.assertTrue(exists(pathData / StringaTest))

    def test_ValidazioneControl_kFold_Fail(self):
        """
        Tests when the user wants to validate a dataset with kFold and the "k" value is not correct
        and checks if no new datasets exist
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathTest = None
        simpleSplit = None
        kFold = True
        k = 1

        response = tester.post('/validazioneControl',
                               data=dict(userpath=userpath, userpathTest=userpathTest,
                                         simpleSplit=simpleSplit, kFold=kFold, k=k))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        pathData = pathlib.Path(__file__).parents[0]
        StringaTrain = 'training_fold_1.csv'
        StringaTest = 'testing_fold_1.csv'
        self.assertFalse(exists(pathData / StringaTrain))
        self.assertFalse(exists(pathData / StringaTest))

    def test_ValidazioneControl_KFold_SimpleSplit(self):
        """
        Tests when the user wants to validate a dataset with kFold and SimpleSplit and
        checks if no new datasets exist because you can not validate a dataset with both kFold
        and SimpleSplit
        """
        tester = app.test_client(self)
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathTest = None
        simpleSplit = True
        kFold = True
        k = 10

        response = tester.post('/validazioneControl',
                               data=dict(userpath=userpath, userpathTest=userpathTest,
                                         simpleSplit=simpleSplit, kFold=kFold, k=k))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        pathData = pathlib.Path(__file__).parents[0]

        for x in range(k):
            StringaTrain = 'training_fold_{}.csv'.format(x + 1)
            StringaTest = 'testing_fold_{}.csv'.format(x + 1)
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
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathTest = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        simpleSplit = None
        kFold = None
        k = 10

        response = tester.post('/validazioneControl',
                               data=dict(userpath=userpath, userpathTest=userpathTest,
                                         simpleSplit=simpleSplit, kFold=kFold, k=k))
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
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        userpathTest = None
        simpleSplit = None
        kFold = None
        k = 10

        response = tester.post('/validazioneControl',
                               data=dict(userpath=userpath, userpathTest=userpathTest,
                                         simpleSplit=simpleSplit, kFold=kFold, k=k))
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

    def test_KFold(self):
        """
        Tests when the user wants to validate a dataset with kFold and checks if the new datasets exist
        """
        userpath = pathlib.Path(__file__).parents[0] / "testingFiles" / "bupa.csv"
        k = 10

        kFoldValidation.cross_fold_validation(userpath, k)
        pathData = pathlib.Path(__file__).parents[0]

        for x in range(k):
            StringaTrain = 'training_fold_{}.csv'.format(x + 1)
            StringaTest = 'testing_fold_{}.csv'.format(x + 1)
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

    def test_simpleSplit(self):
        """
        Tests when the user wants to validate a dataset with SimpleSplit and checks if the new datasets exist
        """
        filename = pathlib.Path(__file__).parents[0] / 'testingFiles' / 'bupa.csv'
        numRaws = utils.numberOfRaws(filename.__str__())

        train_testSplit.splitDataset(filename.__str__())
        self.assertEqual(20, utils.numberOfRaws('Data_testing.csv'))
        self.assertEqual(numRaws - 20, utils.numberOfRaws('Data_training.csv'))
        self.assertTrue(exists(pathlib.Path(__file__).parents[0] / "Data_testing.csv"))
        self.assertTrue(exists(pathlib.Path(__file__).parents[0] / "Data_training.csv"))

    def tearDown(self):
        os.remove('Data_testing.csv')
        os.remove('Data_training.csv')
