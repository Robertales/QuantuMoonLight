import os
import pathlib

from flask import request, Response

from app import app
from app.source.preprocessingDataset import (
    addClass,
    callPS,
    aggId,
    featureExtractionPCA,
)
from app.source.utils import utils, addAttribute

class PreprocessingControl:
    @app.route("/preprocessingControl", methods=["POST"])
    # @login_required
    def preprocessingControl():
        userpath = request.form.get("userpath")
        userpathToPredict = request.form.get("userpathToPredict")
        prototypeSelection = request.form.get("prototypeSelection")
        featureExtraction = request.form.get("featureExtraction")
        numRawsPS = request.form.get("numRawsPS", type=int)
        numColsFE = request.form.get("numColsFE", type=int)
        doQSVM = request.form.get("doQSVM")

        # Cartella dell'utente dove scrivere tutti i risultati
        pathPC = pathlib.Path(userpath).parents[0]
        print("path in PC: ", pathPC)
        if not featureExtraction and not prototypeSelection and doQSVM:
            # Se l'utente non vuole preprocessare il dataset ma vuole fare QSVM,
            # allora qui creo i dataset da classificare aggiungendo la colonna ID
            aggId.addId(
                pathPC / "Data_training.csv",
                pathPC / "DataSetTrainPreprocessato.csv",
            )
            aggId.addId(
                pathPC / "Data_testing.csv",
                pathPC / "DataSetTestPreprocessato.csv",
            )
            print("Exiting from preprocessingControl with NoPS and NoFE")
            return Response(status=200)

        numRaws = utils.numberOfRows(userpath)
        numCols = utils.numberOfColumns(userpath)
        if featureExtraction and numColsFE > numCols:
            print("Impossibile ridurre le colonne: numColsFE > numColsData")
            return Response(status=400)
        if prototypeSelection and numRawsPS > numRaws:
            print("Impossibile ridurre le righe: numRawsPS > numRawsData ")
            return Response(status=400)

        PreprocessingControl.preprocessing(
            userpath,
            userpathToPredict,
            prototypeSelection,
            featureExtraction,
            numRawsPS,
            numColsFE,
            doQSVM,
        )

        # Cancello i file di supporto al preprocessing
        if os.path.exists(pathPC / "TestPS_500_0.15_0.8_5.txt"):
            os.remove(pathPC / "TestPS_500_0.15_0.8_5.txt")
        if os.path.exists(pathPC / "TestPS_500_0.15_0.8_5.xlsx"):
            os.remove(pathPC / "TestPS_500_0.15_0.8_5.xlsx")
        if os.path.exists(pathPC / "IdPCADataset.csv"):
            os.remove(pathPC / "IdPCADataset.csv")
        if os.path.exists(pathPC / "IdPCADatasetTrain.csv"):
            os.remove(pathPC / "IdPCADatasetTrain.csv")

        print("Exiting from preprocessingControl")
        return Response(status=200)

    def preprocessing(
            userpath: str,
            userpathToPredict: str,
            prototypeSelection: bool,
            featureExtraction: bool,
            numRowsPS: int,
            numColsFE: int,
            doQSVM: bool,
    ):
        """
        This function is going to preprocess a given Dataset with prototypeSelection or featureExtraction

        :param userpath: string that points to the location of the dataset to be preprocessed
        :param prototypeSelection: boolean flag that indicated whether the user wants to execute a prototypeSelection or not
        :param userpathToPredict: string that points to the location of the dataset to be predicted
        :param featureExtraction: boolean flag that indicated whether the user wants to execute a feature Extraction or not
        :param numRowsPS: number of rows the prototype selection should reduce the dataset to
        :param numColsFE: number of columns the feature extraction should reduce the dataset to
        :param doQSVM: boolean flag that indicated whether the user wants to execute classification or not
        :return: two preprocessed dataset: 'DataSetTrainPreprocessato.csv', 'DataSetTestPreprocessato.csv'
        :rtype: (str, str)
        """

        numRows = utils.numberOfRows(userpath)
        numCols = utils.numberOfColumns(userpath)
        features = utils.createFeatureList(numCols - 1)
        featuresLabels = features.copy()
        featuresLabels.append("labels")
        pathPC = pathlib.Path(userpath).parents[0]

        # PS with GA
        if prototypeSelection and not featureExtraction:
            print("I'm doing Prototype Selection ...")

            callPS.callPrototypeSelection(
                pathPC / "Data_training.csv", numRowsPS
            )  # crea 'reducedTrainingPS.csv'
            addAttribute.addAttribute(
                pathPC / "reducedTrainingPS.csv",
                pathPC / "featureDataset.csv",
            )  # modifica 'featureDataset.csv'
            # con le istanze create da 'reducedTrainingPS.csv'
            aggId.addId(
                pathPC / "featureDataset.csv",
                pathPC / "DataSetTrainPreprocessato.csv",
            )
            aggId.addId(
                pathPC / "Data_testing.csv",
                pathPC / "DataSetTestPreprocessato.csv",
            )

        # FE with PCA
        elif featureExtraction and not prototypeSelection:
            print("I'm doing Feature Extraction ...")

            featureExtractionPCA.callFeatureExtraction(
                pathPC / "Data_training.csv",
                pathPC / "yourPCA_Train.csv",
                featuresLabels,
                numColsFE,
            )  # effettua FE su Data_Training e genera yourPCA_Train.csv
            featureExtractionPCA.callFeatureExtraction(
                pathPC / "Data_testing.csv",
                pathPC / "yourPCA_Test.csv",
                featuresLabels,
                numColsFE,
            )  # effettua FE su Data_testing e genera yourPCA_Test.csv

            # Aggiunge ID, features e label al Dataset Train
            addClass.addClassPCAtraining(
                pathPC / "Data_training.csv",
                pathPC / "DataSetTrainPreprocessato.csv",
                numColsFE,
            )
            # Aggiunge ID, features e label al Dataset Test
            addClass.addClassPCAtesting(
                pathPC / "Data_testing.csv",
                pathPC / "DataSetTestPreprocessato.csv",
                numColsFE,
            )

        # FE and PS:
        elif prototypeSelection and featureExtraction:  # pragma: no branch
            print("I'm doing Protype Selection and feature extraction ")

            # ps
            callPS.callPrototypeSelection(
                pathPC / "Data_training.csv", numRowsPS
            )  # crea 'reducedTrainingPS.csv'
            addAttribute.addAttribute(
                pathPC / "reducedTrainingPS.csv",
                pathPC / "reducedTrainingPS_attribute.csv",
            )

            # pca
            featureExtractionPCA.callFeatureExtraction(
                pathPC / "reducedTrainingPS_attribute.csv",
                pathPC / "yourPCA_Train.csv",
                featuresLabels,
                numColsFE,
            )  # effettua FE su Data_Training e genera yourPCA_Train.csv
            featureExtractionPCA.callFeatureExtraction(
                pathPC / "Data_testing.csv",
                pathPC / "yourPCA_Test.csv",
                featuresLabels,
                numColsFE,
            )  # effettua FE su Data_testing e genera yourPCA_Test.csv
            # Aggiunge ID, features e label al Dataset Train
            addClass.addClassPCAtraining(
                pathPC / "Data_training.csv",
                pathPC / "DataSetTrainPreprocessato.csv",
                numColsFE,
            )
            # Aggiunge ID, features e label al Dataset Test
            addClass.addClassPCAtesting(
                pathPC / "Data_testing.csv",
                pathPC / "DataSetTestPreprocessato.csv",
                numColsFE,
            )
            os.remove(pathPC / "reducedTrainingPS_attribute.csv")

        if doQSVM and featureExtraction:
            # effettua feature Extraction sul doPrediction e rigenera doPrediction

            # aggiungere riga delle feature al do Prediction
            h = open(pathPC / "doPredictionFeatured.csv", "a+")
            featureString = ""
            for x in range(1, utils.numberOfColumns(userpath)):
                stringa = "feature{},".format(x)
                featureString += stringa
            featureString += "labels\r"
            h.write(featureString)
            print("USERPATH TO PREDICT", userpathToPredict)
            g = open(userpathToPredict, "r")
            contents = g.read()
            h.write(contents)
            h.close()
            g.close()

            featureExtractionPCA.extractFeatureForPrediction(
                pathPC / "doPredictionFeatured.csv",
                pathPC / "doPredictionFE.csv",
                numColsFE,
            )
            os.remove(pathPC / "doPredictionFeatured.csv")

        return (
            pathPC / "DataSetTrainPreprocessato.csv",
            pathPC / "DataSetTestPreprocessato.csv",
        )


