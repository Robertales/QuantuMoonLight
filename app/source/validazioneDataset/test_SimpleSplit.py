import os
from os.path import exists
import pathlib
import unittest
from app.source.utils import utils
from app.source.validazioneDataset import train_testSplit


class TestSimpleSplit(unittest.TestCase):

    def test_simpleSplit(self):
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
