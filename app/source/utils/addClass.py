import csv

import pandas as pd
import os



def addClassPCAtraining(filename):
    # save the class in array y
    dataset = pd.read_csv(filename)
    y = dataset['labels']
    #k=dataset['Id']

    # add component name in file
    h = open("yourPCA_attribute.csv", "a+")
    h.write("feature1,feature2\r")
    h.close()
    h = open("yourPCA_attribute.csv", "a+")
    g = open("yourPCA.csv", "r")
    contents = g.read()
    h.write(contents)
    h.close()

    # addClass in file
    df = pd.read_csv("yourPCA_attribute.csv")
    df["labels"] = y
    #df["Id"]=k

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

    with open('IdPCADatasetTrain.csv') as input, open('Data_PCA_training.csv', 'w', newline='') as output:
        writer = csv.writer(output)
        for row in csv.reader(input):
            if any(field.strip() for field in row):
                writer.writerow(row)


def addClassPCAtesting(filename):
    # save the class in array y
    dataset = pd.read_csv(filename)
    y = dataset['labels']
    #k = dataset['Id']

    # add component name in file
    h = open("yourPCA_attribute1.csv", "a+")
    h.write("feature1,feature2\r")
    h.close()
    h = open("yourPCA_attribute1.csv", "a+")
    g = open("yourPCA1.csv", "r")
    contents = g.read()
    h.write(contents)
    h.close()

    # addClass in file
    df = pd.read_csv("yourPCA_attribute1.csv")
    df["labels"] = y
    #df["Id"]=k

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

    with open('IdPCADataset.csv') as input, open('Data_PCA_testing.csv', 'w', newline='') as output:
        writer = csv.writer(output)
        for row in csv.reader(input):
            if any(field.strip() for field in row):
                writer.writerow(row)