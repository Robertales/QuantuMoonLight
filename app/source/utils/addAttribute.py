

#filename="heart.csv"

def addAttribute(filename):

    #text = open(filename, "r")
    #text = ''.join([i for i in text]) \
     #   .replace(" ", ",")
    #x = open("featureDataset.csv", "w")
    #x.writelines(text)
   # x.close()


    f = open("featureDataset.csv", "w")
    f.write("feature1,feature2,feature3,feature4,labels\r")
    f.close()

    f = open("featureDataset.csv", "a+")
    g = open(filename, "r")
    contents = g.read()
    f.write(contents)
    f.close()
    g.close()

    return 0


def addAttribute_to_ps(filename):
    # text = open(filename, "r")
    # text = ''.join([i for i in text]) \
    #   .replace(" ", ",")
    # x = open("featureDataset.csv", "w")
    # x.writelines(text)
    # x.close()

    f = open("reducedTrainingPS_attribute.csv", "w")
    f.write("feature1,feature2,feature3,feature4,labels\r")
    f.close()

    f = open("reducedTrainingPS_attribute.csv", "a+")
    g = open(filename, "r")
    contents = g.read()
    f.write(contents)
    f.close()
    g.close()


    return 0



