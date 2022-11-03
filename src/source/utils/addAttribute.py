from pathlib import Path

from src.source.utils import utils


def createFeatureString(numCols: int):
    """
    This function generate the string "feature1,feature2,...,featureN,labels" where n=:numCols

    :param numCols: number of columns of the dataset
    :return: string "feature1,feature2,...,featureN,labels" where n=:numCols
    :rtype: str
    """

    featureString = ""

    for x in range(numCols - 1):
        stringa = "feature{},".format(x + 1)
        featureString += stringa

    featureString += "labels\r"

    return featureString


def addAttribute(filename: Path, outputName):
    """
    This function add into the output file the features string and all the raws contained in the input file

    :param filename: input file name
    :param outputName: output file name
    :return: name of the output file, now with all the raws
    :rtype: str
    """
    numCols = utils.numberOfColumns(filename)
    featuresString = createFeatureString(numCols)

    f = open(outputName, "w")
    f.write(featuresString)
    f.close()

    f = open(outputName, "a+")
    g = open(filename, "r")
    contents = g.read()
    f.write(contents)
    f.close()
    g.close()

    return outputName
