import unittest
import os
import pathlib
from os.path import exists
from app.source.validazioneDataset import kFoldValidation


class TestKFold(unittest.TestCase):

    def test_KFold(self):
        userpath = pathlib.Path(__file__).cwd() / "testingFiles" / "bupa.csv"
        k = 10

        kFoldValidation.cross_fold_validation(userpath, k)
        pathData = pathlib.Path(__file__).cwd()

        for x in range(k):
            StringaTrain = 'training_fold_{}.csv'.format(x + 1)
            StringaTest = 'testing_fold_{}.csv'.format(x + 1)
            self.assertTrue(exists(pathData / StringaTrain))
            self.assertTrue(exists(pathData / StringaTest))

    def tearDown(self):
        directory = pathlib.Path(__file__).cwd()
        allFiles = os.listdir(directory)
        csvFiles = [file for file in allFiles if file.endswith(".csv")]
        for file in csvFiles:
            path = os.path.join(directory, file)
            os.remove(path)
