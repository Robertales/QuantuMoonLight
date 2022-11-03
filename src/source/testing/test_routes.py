import hashlib
import os
import pathlib
import unittest
from os.path import exists

from flask_login import current_user
from sqlalchemy import desc
from sqlalchemy_utils import create_database, database_exists

from src import app, db
from src.source.model.models import User, Dataset


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

    def test_routes(self):
        # Login User and test if that works
        tester = app.test_client()
        self.assertFalse(current_user)
        with tester:
            # Setup for login testing
            password = "quercia12345"
            password = hashlib.sha512(password.encode()).hexdigest()
            response = tester.post(
                "/signup",
                data=dict(
                    email="boscoverde27@gmail.com",
                    password=password,
                    confirmPassword=password,
                    username="Antonio",
                    isResearcher="",
                    nome="Antonio",
                    cognome="De Curtis",
                    token="43a75c20e78cef978267a3bdcdb0207dab62575c3c9da494a1cd344022abc8a326ca1a9b7ee3f533bb7ead73a5f9fe519691a7ad17643eecbe13d1c8c4adccd2"),
            )
            print(current_user)
            assert isinstance(current_user, User)
            self.assertTrue(current_user.is_authenticated)

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
                    Radio="simpleSplit"

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

