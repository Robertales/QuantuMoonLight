#!C:\Users\Gennaro\Miniconda3\envs\python\python.exe
# print("Content-Type: text/html\n")
# Import packages


from sqlalchemy import desc

from app.source.validazioneDataset import train_testSplit
from app.source.preprocessingDataset import callPS, featureExtractionPCA
from app.source.classificazioneDataset import QSVM_iris as qsvm
from app.source.utils import addAttribute, addClass, aggId, aggIdTesting, utils
from app.models import Files

# Recupero dataset e conto le colonne
file = Files.query.order_by(desc(Files.id)).first()
dbpath = file.paths
print("Dataset: ", dbpath)
filename = dbpath
numCols = utils.numberOfColumns(filename)

# Recupero le impostazioni dell'utente, cioè
# quali operazioni vuole effettuare e, in caso di QSVM, anche il token
autosplit = True
print("AutoSplit: ", autosplit)
prototypeSelection = file.ps
numRawsPS = 200  # numero di righe dopo la Prototype Selection con GA
print("Prototype Selection: ", prototypeSelection)
featureExtraction = file.fe
numColsFE = 2  # numero di colonne dopo la Feature Extraction con PCA
print("Feature Extraction: ", featureExtraction)
kFold = False
print("K-Fold: ", kFold)
doQSVM = True
print("Do QSVM: ", doQSVM)
token = 'ab13c0c375e41880eb7859adafd65cff1fbfb258d423015c6ab5d1f03f3e83d9a8a937076478eee47c8b897d31010496339879c8a1ffa8ab1801571155983c50'

# Creo le Liste di features per la qsvm
features = utils.createFeatureList(numCols - 1)
features1 = features.copy()
features1.append("labels")
featuresPCA = utils.createFeatureList(numColsFE)
print("\n")

# spilt and PS
if autosplit == True and prototypeSelection == True and featureExtraction == False and kFold == False:
    print("I'm doing Prototype Selection and QSVM...")
    addAttribute.addAttribute(
        filename)  # copia il dataset dell'utente (con il suo path preso dal DB), con  l'aggiunta degli attributi in 'featureDataset.csv'
    train_testSplit.splitDataset('featureDataset.csv')  # crea 'Data_training.csv' e 'Data_testing.csv'
    callPS.callPS('Data_training.csv')  # crea 'reducedTrainingPS.csv'
    addAttribute.addAttribute(
        'reducedTrainingPS.csv')  # modifica 'featureDataset.csv' con le istanze create da 'reducedTrainingPS.csv'
    aggId.addId('featureDataset.csv')
    aggIdTesting.aggIdTesting()
    qsvm.myQSVM('IdFeatureDataset_compatted.csv', 'IdData_Testing_compatted.csv', features, token, len(features))



# split and PCA
elif autosplit == True and prototypeSelection == False and featureExtraction == True and kFold == False:
    print("I'm doing Feature Extraction and QSVM...")
    addAttribute.addAttribute(filename)
    train_testSplit.splitDataset('featureDataset.csv')

    featureExtractionPCA.featureExtractionPCA2('Data_training.csv', features1)  # do pca of training
    featureExtractionPCA.featureExtractionPCA2('Data_testing.csv', features1)  # do pca of testing
    addClass.addClassPCAtraining('Data_training.csv')  # add class to pca dataset training
    addClass.addClassPCAtesting('Data_testing.csv')  # add class to pca dataset training
    qsvm.myQSVM('Data_PCA_training.csv', 'Data_PCA_testing.csv', featuresPCA, token, 2)

# Split PCA and PS:
elif autosplit == True and prototypeSelection == True and featureExtraction == True and kFold == False:
    print("I'm doing Protype Selection, feature extraction and QSVM")
    # ps
    addAttribute.addAttribute(filename)
    train_testSplit.splitDataset('featureDataset.csv')
    callPS.callPS('Data_training.csv')
    addAttribute.addAttribute_to_ps('reducedTrainingPS.csv')

    # pca
    featureExtractionPCA.featureExtractionPCA2('reducedTrainingPS_attribute.csv', features1)  # do pca of PS training
    featureExtractionPCA.featureExtractionPCA2('Data_testing.csv', features1)  # do pca of testing
    addClass.addClassPCAtraining('Data_training.csv')  # add class to pca dataset training
    addClass.addClassPCAtesting('Data_testing.csv')  # add class to pca dataset training
    qsvm.myQSVM('Data_PCA_training.csv', 'Data_PCA_testing.csv', featuresPCA, token, 2)

# NOTHING ONLY QSVM
elif autosplit == True and prototypeSelection == False and featureExtraction == False and kFold == False:
    print("I'm doing only QSVM")
    # split
    addAttribute.addAttribute(filename)
    train_testSplit.splitDataset('featureDataset.csv')
    aggId.addId('Data_training.csv')
    aggIdTesting.aggIdTesting()
    # qsvm
    qsvm.myQSVM('IdFeatureDataset_compatted.csv', 'IdData_Testing_compatted.csv', features, token, 10)

# PROTOTYPE SELECTION AND 10 KFOLD
elif autosplit == True and prototypeSelection == True and featureExtraction == False and kFold == True:
    print("I'm doing Prototype Selection and QSVM with ten_kfolds validation...")

    callPS.callPS('venv/10-kfolds/training/training_fold_1.csv')  # chiamo ps su training
    addAttribute.addAttribute('reducedTrainingPS.csv')  # aggiungo attributi al risultato della ps
    aggId.addId('featureDataset.csv')  # aggiungo id ai dati
    addAttribute.addAttribute('testing_fold_0.csv')  # aggiungo attributi al testing
    aggIdTesting.aggIdTesting('featureDataset.csv')  # aggiungo id al testing
    qsvm.myQSVM('IdFeatureDataset_compatted.csv', 'IdData_Testing_compatted.csv', features, token, 4)


# PROTOTYPE SELECTION, FEATURE EXTRACTION AND 10 KFOLD
elif autosplit == True and prototypeSelection == True and featureExtraction == True and kFold == True:
    print("I'm doing Prototype Selection, Feature Extraction and QSVM with ten_kfolds validation...")

    # ps
    callPS.callPS('venv/10-kfolds/training/training_fold_8.csv')
    addAttribute.addAttribute_to_ps('reducedTrainingPS.csv')

    # pca
    featureExtractionPCA.featureExtractionPCA2('reducedTrainingPS_attribute.csv', features1)  # do pca of PS training
    addAttribute.addAttribute('venv/10-kfolds/testing/testing_fold_8.csv')
    featureExtractionPCA.featureExtractionPCA2('featureDataset.csv', features1)  # do pca of testing
    addClass.addClassPCAtraining(
        'reducedTrainingPS_attribute.csv ')  # take labels from reduced trainingps that is a dataset of training set and apply id, features and labels
    addClass.addClassPCAtesting(
        'featureDataset.csv')  # take labels from feature dataset that is a dataset of testing set and apply id, features and labels

    qsvm.myQSVM('Data_PCA_training.csv', 'Data_PCA_testing.csv', featuresPCA, token, 2)
