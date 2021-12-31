from app.source.utils import utils

def createFeatureString(numCols):
    featureString = ""

    for x in range(numCols - 1):
        stringa = "feature{},".format(x + 1)
        featureString += stringa

    featureString += "labels\r"

    return featureString

def addAttribute(filename):
    numCols = utils.numberOfColumns(filename)
    featuresString = createFeatureString(numCols)

    f = open("featureDataset.csv", "w")
    f.write(featuresString)
    f.close()

    f = open("featureDataset.csv", "a+")
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



