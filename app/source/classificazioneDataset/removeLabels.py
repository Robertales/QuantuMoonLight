import csv
import pathlib
from app.source.utils import utils

# open input CSV file as source
# open output CSV file as result
pathGroundTruth = pathlib.Path(__file__).cwd()
pathGroundTruth = pathGroundTruth / 'ground_truth.csv'
numCols = utils.numberOfColumns(pathGroundTruth)-1

with open(pathGroundTruth.__str__(), "r") as source:
    reader = csv.reader(source)

    pathDoPrediction = pathlib.Path(__file__).cwd()
    pathDoPrediction = pathDoPrediction / 'doPrediction1.csv'
    with open(pathDoPrediction.__str__(), "w", newline='') as result:
        writer = csv.writer(result)
        for r in reader:
            # Use CSV Index to remove a column from CSV
            # r[3] = r['year']
            #ci devono stare tante r[x] quante le colonne del datasete SENZA LA COLONNA LABELS
            writer.writerow((r[0], r[1], r[2], r[3], r[4], r[5]))
                             #,r[6],r[7],r[8],r[9],r[10],r[11],r[12],r[13],r[14],r[15],r[16],r[17],r[18]))
            #Ricorda di cancellare la prima riga dal file doPrection1.csv


