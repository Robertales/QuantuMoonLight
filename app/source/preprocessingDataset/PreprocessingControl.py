import os
from flask import request
from app import app
from app.source.utils import utils, addAttribute
from app.source.preprocessingDataset import addClass, callPS, aggId, featureExtractionPCA


@app.route('/preprocessingControl', methods=['POST'])
def preprocessingControl():
    userpath = request.form.get("userpath")
    userpathToPredict = request.form.get("userpathToPredict")
    prototypeSelection = bool(request.form.get("prototypeSelection"))
    featureExtraction = bool(request.form.get("featureExtraction"))
    numRawsPS = int(request.form.get("numRawsPS"))
    numColsFE = int(request.form.get("numColsFE"))
    doQSVM = bool(request.form.get("doQSVM"))

    if not featureExtraction and not prototypeSelection and doQSVM:
        # Se l'utente non vuole preprocessare il dataset ma vuole fare QSVM,
        # allora qui creo i dataset da classificare aggiungendo la colonna ID
        aggId.addId('Data_training.csv', 'DataSetTrainPreprocessato.csv')
        aggId.addId('Data_testing.csv', 'DataSetTestPreprocessato.csv')
        print("Exiting from preprocessingControl with NoPS and NoFE")
        return 'DataSetTrainPreprocessato.csv', 'DataSetTestPreprocessato.csv'

    preprocessing(userpath, userpathToPredict, prototypeSelection, featureExtraction, numRawsPS, numColsFE, doQSVM)

    # Cancello i file di supporto al preprocessing
    if os.path.exists("TestPS_500_0.15_0.8_5.txt"):
        os.remove("TestPS_500_0.15_0.8_5.txt")
    if os.path.exists("TestPS_500_0.15_0.8_5.xlsx"):
        os.remove("TestPS_500_0.15_0.8_5.xlsx")
    if os.path.exists("IdPCADataset.csv"):
        os.remove("IdPCADataset.csv")
    if os.path.exists("IdPCADatasetTrain.csv"):
        os.remove("IdPCADatasetTrain.csv")

    return "Exiting from preprocessingControl"


def preprocessing(userpath: str, userpathToPredict: str, prototypeSelection: bool, featureExtraction: bool,
                  numRawsPS: int, numColsFE: int, doQSVM: bool):
    """
    This function is going to preprocess a given Dataset with prototypeSelection or featureExtraction

    :param userpath: string that points to the location of the dataset to be preprocessed
    :param prototypeSelection: boolean flag that indicated whether the user wants to execute a prototypeSelection or not
    :param userpathToPredict: string that points to the location of the dataset to be predicted
    :param featureExtraction: boolean flag that indicated whether the user wants to execute a feature Extraction or not
    :param numRawsPS: number of rows the prototype selection should reduce the dataset to
    :param numColsFE: number of columns the feature extraction should reduce the dataset to
    :param doQSVM: boolean flag that indicated whether the user wants to execute classification or not
    :return: two preprocessed dataset: 'DataSetTrainPreprocessato.csv', 'DataSetTestPreprocessato.csv'
    :rtype: (str, str)
    """

    numCols = utils.numberOfColumns(userpath)
    features = utils.createFeatureList(numCols - 1)
    featuresLabels = features.copy()
    featuresLabels.append("labels")

    # PS with GA
    if prototypeSelection and not featureExtraction:
        print("I'm doing Prototype Selection ...")

        callPS.callPrototypeSelection('Data_training.csv', numRawsPS)  # crea 'reducedTrainingPS.csv'
        addAttribute.addAttribute('reducedTrainingPS.csv', 'featureDataset.csv')  # modifica 'featureDataset.csv'
        # con le istanze create da 'reducedTrainingPS.csv'
        aggId.addId('featureDataset.csv', 'DataSetTrainPreprocessato.csv')
        aggId.addId('Data_testing.csv', 'DataSetTestPreprocessato.csv')

    # FE with PCA
    elif featureExtraction and not prototypeSelection:
        print("I'm doing Feature Extraction ...")

        featureExtractionPCA.callFeatureExtraction('Data_training.csv', 'yourPCA_Train.csv', featuresLabels,
                                                   numColsFE)  # effettua FE su Data_Training e genera yourPCA_Train.csv
        featureExtractionPCA.callFeatureExtraction('Data_testing.csv', 'yourPCA_Test.csv', featuresLabels,
                                                   numColsFE)  # effettua FE su Data_testing e genera yourPCA_Test.csv

        # Aggiunge ID, features e label al Dataset Train
        addClass.addClassPCAtraining('Data_training.csv', 'DataSetTrainPreprocessato.csv', numColsFE)
        # Aggiunge ID, features e label al Dataset Test
        addClass.addClassPCAtesting('Data_testing.csv', 'DataSetTestPreprocessato.csv', numColsFE)

    # FE and PS:
    elif prototypeSelection and featureExtraction:
        print("I'm doing Protype Selection and feature extraction ")

        # ps
        callPS.callPrototypeSelection('Data_training.csv', numRawsPS)  # crea 'reducedTrainingPS.csv'
        addAttribute.addAttribute('reducedTrainingPS.csv', 'reducedTrainingPS_attribute.csv')

        # pca
        featureExtractionPCA.callFeatureExtraction('reducedTrainingPS_attribute.csv', 'yourPCA_Train.csv',
                                                   featuresLabels,
                                                   numColsFE)  # effettua FE su Data_Training e genera yourPCA_Train.csv
        featureExtractionPCA.callFeatureExtraction('Data_testing.csv', 'yourPCA_Test.csv',
                                                   featuresLabels,
                                                   numColsFE)  # effettua FE su Data_testing e genera yourPCA_Test.csv
        # Aggiunge ID, features e label al Dataset Train
        addClass.addClassPCAtraining('Data_training.csv', 'DataSetTrainPreprocessato.csv', numColsFE)
        # Aggiunge ID, features e label al Dataset Test
        addClass.addClassPCAtesting('Data_testing.csv', 'DataSetTestPreprocessato.csv', numColsFE)
        os.remove('reducedTrainingPS_attribute.csv')

    if doQSVM and featureExtraction:
        # effettua feature Extraction sul doPrediction e rigenera doPrediction

        # aggiungere riga delle feature al do Prediction
        h = open("doPredictionFeatured.csv", "a+")
        featureString = ''
        for x in range(1, utils.numberOfColumns(userpath)):
            stringa = "feature{},".format(x)
            featureString += stringa
        featureString += "labels\r"
        h.write(featureString)
        g = open(userpathToPredict, "r")
        contents = g.read()
        h.write(contents)
        h.close()
        g.close()

        featureExtractionPCA.extractFeatureForPrediction("doPredictionFeatured.csv", 'doPredictionFE.csv', numColsFE)
        os.remove("doPredictionFeatured.csv")

    return 'DataSetTrainPreprocessato.csv', 'DataSetTestPreprocessato.csv'
