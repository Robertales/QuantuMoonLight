#!C:\Users\Gennaro\Miniconda3\envs\python\python.exe
#print("Content-Type: text/html\n")
#Import packages

import callPS
import train_testSplit
#import getFileToDB
import mysql.connector
from mysql.connector import errorcode
import featureExtractionPCA1
import QSVM_iris as qsvm
import addAttribute
import addClass
import aggId, aggIdTesting

autosplit = True
prototypeSelection = True
featureExtraction = True
ten_kfold = True

try:
    mydb = mysql.connector.connect(user='root',
                                   database='quantumknn_db')
    mycursor = mydb.cursor()


    mycursor.execute("SELECT paths,ps,fe FROM files ORDER BY id_files DESC")

    myresult = mycursor.fetchone()

    #for result in myresult:
    #print(myresult)


except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    mydb.close()


# into string
def convertTuple(tuple):
    dbpath = ''.join(tuple)
    return dbpath


# Driver code
dbpath = convertTuple(myresult[0])
print("Dataset: ",dbpath)

autosplit = True

if myresult[1] == 1:
    prototypeSelection = True
    print("Prototype Selection: ",prototypeSelection)
else:
    prototypeSelection = False
    print("Prototype Selection ", prototypeSelection)

if myresult[2] == 1:
    featureExtraction = True
    print("Feature Extraction: ", featureExtraction)
else:
    featureExtraction= False
    print("Feature Extraction: ", featureExtraction)


filename = dbpath
token = ''
features = ['feature1','feature2','feature3','feature4']
features1= ['feature1','feature2','feature3','feature4','labels']
featuresPCA = ['feature1','feature2']
print("\n")

#spilt and PS
if autosplit == True and prototypeSelection == True and featureExtraction == False and ten_kfold == False:
    print("I'm doing Prototype Selection and QSVM...")
    addAttribute.addAttribute(filename)
    train_testSplit.splitDataset('featureDataset.csv')
    callPS.callPS('Data_training.csv')
    addAttribute.addAttribute('reducedTrainingPS.csv')
    aggId.addId('featureDataset.csv')
    aggIdTesting.aggIdTesting()
    qsvm.myQSVM('IdFeatureDataset_compatted.csv','IdData_Testing_compatted.csv',features,token,4)



#split and PCA
elif autosplit == True and prototypeSelection == False and featureExtraction == True and ten_kfold == False:
    print("I'm doing Feature Extraction and QSVM...")
    addAttribute.addAttribute(filename)
    train_testSplit.splitDataset('featureDataset.csv')

    featureExtractionPCA1.featureExtractionPCA2('Data_training.csv',features1)  # do pca of training
    featureExtractionPCA1.featureExtractionPCA2('Data_testing.csv',features1)  # do pca of testing
    addClass.addClassPCAtraining('Data_training.csv')  # add class to pca dataset training
    addClass.addClassPCAtesting('Data_testing.csv')  # add class to pca dataset training
    qsvm.myQSVM('Data_PCA_training.csv', 'Data_PCA_testing.csv', featuresPCA, token, 2)

#Split PCA and PS:
elif autosplit == True and prototypeSelection == True and featureExtraction ==True and ten_kfold == False:
    print("I'm doing Protype Selection, feature extraction and QSVM")
    # ps
    addAttribute.addAttribute(filename)
    train_testSplit.splitDataset('featureDataset.csv')
    callPS.callPS('Data_training.csv')
    addAttribute.addAttribute_to_ps('reducedTrainingPS.csv')

    #pca
    featureExtractionPCA1.featureExtractionPCA2('reducedTrainingPS_attribute.csv', features1)  # do pca of PS training
    featureExtractionPCA1.featureExtractionPCA2('Data_testing.csv', features1)  # do pca of testing
    addClass.addClassPCAtraining('Data_training.csv')  # add class to pca dataset training
    addClass.addClassPCAtesting('Data_testing.csv')  # add class to pca dataset training
    qsvm.myQSVM('Data_PCA_training.csv', 'Data_PCA_testing.csv', featuresPCA, token, 2)

#NOTHING ONLY QSVM
elif autosplit == True and prototypeSelection == False and featureExtraction == False and ten_kfold == False:
    print("I'm doing only QSVM")
    #split
    addAttribute.addAttribute(filename)
    train_testSplit.splitDataset('featureDataset.csv')
    aggId.addId('Data_training.csv')
    aggIdTesting.aggIdTesting()
    #qsvm
    qsvm.myQSVM('IdFeatureDataset_compatted.csv', 'IdData_Testing_compatted.csv', features, token, 10)

#PROTOTYPE SELECTION AND 10 KFOLD
elif autosplit == True and prototypeSelection == True and featureExtraction == False and ten_kfold == True:
    print("I'm doing Prototype Selection and QSVM with ten_kfolds validation...")

    callPS.callPS('venv/10-kfolds/training/training_fold_1.csv') #chiamo ps su training
    addAttribute.addAttribute('reducedTrainingPS.csv') #aggiungo attributi al risultato della ps
    aggId.addId('featureDataset.csv')   #aggiungo id ai dati
    addAttribute.addAttribute('testing_fold_0.csv')  # aggiungo attributi al testing
    aggIdTesting.aggIdTesting('featureDataset.csv') #aggiungo id al testing
    qsvm.myQSVM('IdFeatureDataset_compatted.csv','IdData_Testing_compatted.csv',features,token,4)


#PROTOTYPE SELECTION, FEATURE EXTRACTION AND 10 KFOLD
elif autosplit == True and prototypeSelection == True and featureExtraction == True and ten_kfold == True:
    print("I'm doing Prototype Selection, Feature Extraction and QSVM with ten_kfolds validation...")

    # ps
    callPS.callPS('venv/10-kfolds/training/training_fold_8.csv')
    addAttribute.addAttribute_to_ps('reducedTrainingPS.csv')

    # pca
    featureExtractionPCA1.featureExtractionPCA2('reducedTrainingPS_attribute.csv', features1)  # do pca of PS training
    addAttribute.addAttribute('venv/10-kfolds/testing/testing_fold_8.csv')
    featureExtractionPCA1.featureExtractionPCA2('featureDataset.csv', features1)  # do pca of testing
    addClass.addClassPCAtraining('reducedTrainingPS_attribute.csv ') #take labels from reduced trainingps that is a dataset of training set and apply id, features and labels
    addClass.addClassPCAtesting('featureDataset.csv') #take labels from feature dataset that is a dataset of testing set and apply id, features and labels

    qsvm.myQSVM('Data_PCA_training.csv', 'Data_PCA_testing.csv', featuresPCA, token, 2)





