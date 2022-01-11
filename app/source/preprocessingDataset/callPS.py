import pathlib
import numpy as np
from app.source.utils import utils
from app.source.preprocessingDataset import PrototypeSelectionProblem as ps


def callPrototypeSelection(path: pathlib.Path, number_of_reduced_training_instances=10):
    """
    This function executes the prototype selection on the given dataset

    :param path: string that points to the location of the dataset that is going to be reduced with PS
    :param number_of_reduced_training_instances: new number of raws
    :return: string that points to the location of the dataset preprocessed with PS
    :rtype: str
    """
    x_train, x_test, number_of_features, number_of_classes, number_of_total_instances = utils.prepareData(path)

    number_of_solutions = 500
    chromosomeToEvaluate, fitness = ps.runGeneticAlgorithXPS(number_of_solutions, x_train,
                                                             number_of_reduced_training_instances,path.parent)

    print(chromosomeToEvaluate)
    pathFileReducedTrainingPS = pathlib.Path(path).parent
    pathFileReducedTrainingPS = pathFileReducedTrainingPS / 'reducedTrainingPS.csv'

    np.savetxt(pathFileReducedTrainingPS.__str__(), x_train[chromosomeToEvaluate, :], delimiter=",", fmt='%s')

    return pathFileReducedTrainingPS.__str__()
