import csv
import os
from pathlib import Path


def addId(filename: Path, filenameOut: Path):
    """
    This function adds the colomumn ID as the first column of the given dataset

    :param filename: path to to the location of the dataset
    :param filenameOut: path to the location of new the dataset
    :return: string that points to the location of new the dataset
    :rtype: str
    """
    dataPath = filename.parent
    with open(filename, 'r') as input, open(dataPath/'DatasetTEMP.csv', 'w') as output:
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
        input.close()
        output.close()

    with open(dataPath/'DatasetTEMP.csv') as input, open(filenameOut, 'w', newline='') as output:
        writer = csv.writer(output)
        for row in csv.reader(input):
            if any(field.strip() for field in row):
                writer.writerow(row)
    input.close()
    output.close()
    os.remove(dataPath/'DatasetTEMP.csv')

    return filenameOut