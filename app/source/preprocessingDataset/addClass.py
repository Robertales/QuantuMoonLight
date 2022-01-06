import csv
import os
import pandas as pd


def addClassPCAtraining(filename, filenameOut, numColsFE=2):
    """
    This function generate a new dataset train with ID and labels columns, and string
    "ID,feature1,feature2,...,featuren,labels" on top of the file

    :param filename: data set input, with just the attribute raws
    :param filenameOut: data set output
    :param numColsFE: number of columns for the Feature Extraction
    :return: file name out, ready to be downloaded or classified
    :rtype: str
    """
    # salva le label originali da filename
    dataset = pd.read_csv(filename)
    y = dataset['labels']

    # aggiunge la riga feature e le righe del dataset yourPCA
    h = open("yourPCA_attribute.csv", "a+")
    featureString = ''
    for x in range(1, numColsFE):
        stringa = "feature{},".format(x)
        featureString += stringa
    featureString += ("feature{}\r".format(numColsFE))
    h.write(featureString)
    g = open("yourPCA_Train.csv", "r")
    contents = g.read()
    h.write(contents)
    h.close()

    # addClass in file
    df = pd.read_csv("yourPCA_attribute.csv")
    df["labels"] = y

    df.to_csv("myPCAclass_Training.csv", index=False)


    with open('myPCAclass_Training.csv', 'r') as input, open('IdPCADatasetTrain.csv', 'w') as output:
        reader = csv.reader(input, delimiter=',')
        writer = csv.writer(output, delimiter=',')

        all = []
        row = next(reader)
        row.insert(0, 'Id')
        all.append(row)
        count = 0
        for row in reader:
            count += 1
            row.insert(0, count)
            all.append(row)
        writer.writerows(all)

    with open('IdPCADatasetTrain.csv') as input, open(filenameOut, 'w', newline='') as output:
        writer = csv.writer(output)
        for row in csv.reader(input):
            if any(field.strip() for field in row):
                writer.writerow(row)

    os.remove('myPCAclass_Training.csv')
    os.remove('yourPCA_attribute.csv')

    return filenameOut


def addClassPCAtesting(filename, filenameOut, numColsFE=2):
    """
    This function generate a new dataset test with ID and labels columns, and string
    "ID,feature1,feature2,...,featuren,labels" on top of the file

    :param filename: data set input, with just the attribute raws
    :param filenameOut: data set output
    :param numColsFE: number of columns for the Feature Extraction
    :return: file name out, ready to be downloaded or classified
    :rtype: str
    """
    # save the class in array y
    dataset = pd.read_csv(filename)
    y = dataset['labels']
    # k = dataset['Id']

    # add component name in file
    h = open("yourPCA_attribute1.csv", "a+")
    featureString = ''
    for x in range(1, numColsFE):
        stringa = "feature{},".format(x)
        featureString += stringa
    featureString += ("feature{}\r".format(numColsFE))
    h.write(featureString)
    g = open("yourPCA_Test.csv", "r")
    contents = g.read()
    h.write(contents)
    h.close()

    # addClass in file
    df = pd.read_csv("yourPCA_attribute1.csv")
    df["labels"] = y
    # df["Id"]=k

    df.to_csv("myPCAclass_Testing.csv", index=False)

    with open('myPCAclass_Testing.csv', 'r') as input, open('IdPCADataset.csv', 'w') as output:
        reader = csv.reader(input, delimiter=',')
        writer = csv.writer(output, delimiter=',')

        all = []
        row = next(reader)
        row.insert(0, 'Id')
        all.append(row)
        count = 0
        for row in reader:
            count += 1
            row.insert(0, count)
            all.append(row)
        writer.writerows(all)

    with open('IdPCADataset.csv') as input, open(filenameOut, 'w', newline='') as output:
        writer = csv.writer(output)
        for row in csv.reader(input):
            if any(field.strip() for field in row):
                writer.writerow(row)

    os.remove('myPCAclass_Testing.csv')
    os.remove('yourPCA_attribute1.csv')

    return filenameOut
