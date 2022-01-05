from app.source.utils import utils

def createFeatureString(numCols):
    featureString = ""

    for x in range(numCols - 1):
        stringa = "feature{},".format(x + 1)
        featureString += stringa

    featureString += "labels\r"

    return featureString

def addAttribute(filename, outputName = "featureDataset.csv"):
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

    return 0


def addAttribute_to_ps(filename):
    numCols = utils.numberOfColumns(filename)
    featuresString = createFeatureString(numCols)

    f = open("reducedTrainingPS_attribute.csv", "w")
    f.write(featuresString)
    f.close()

    f = open("reducedTrainingPS_attribute.csv", "a+")
    g = open(filename, "r")
    contents = g.read()
    f.write(contents)
    f.close()
    g.close()

    return 0



