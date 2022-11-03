#This code was developed for the paper
#G. Acampora and A. Vitiello, "TSSweb: a Web Tool for Training Set Selection," 
#2020 IEEE International Conference on Fuzzy Systems (FUZZ-IEEE), 2020, pp. 1-7, doi: 10.1109/FUZZ48607.2020.9177677.

import pathlib
import pandas as pd
from src.source.preprocessingDataset import (
    PrototypeSelectionProblem as ps,
)

def callPrototypeSelection(
        path: pathlib.Path, number_of_reduced_training_instances=10
):
    """
    This function executes the prototype selection on the given dataset and write the result in reducedTrainingPS.csv

    :param path: string that points to the location of the dataset that is going to be reduced with PS
    :param number_of_reduced_training_instances: new number of raws
    :return: path that points to the location of the dataset preprocessed with PS
    :rtype: path
    """

    # Create a dataframe from csv
    df = pd.read_csv(path)
    # matrix of values
    X = df.values

    # The evolution ends when the maximum number of evaluations of fitness (corresponding to the number of
    # solutions evaluated) is achieved

    # Run evolution
    bestRows, fitness = ps.runGeneticAlgorithm(
        X,
        number_of_reduced_training_instances,
        path.parent,
    )
    print()
    print("Fitness of the obtained reduced individual %f" % fitness)
    print("Best selection of instance: ")
    print(bestRows)
    print()

    pathFileReducedTrainingPS = pathlib.Path(path).parent
    pathFileReducedTrainingPS = (
            pathFileReducedTrainingPS / "reducedTrainingPS.csv"
    )

    # retrieve best rows and write result in reducedTrainingPS.csv
    PS_df = pd.DataFrame(data=df.values[bestRows, :], columns=df.columns)
    PS_df.to_csv(pathFileReducedTrainingPS, index=False)

    return pathFileReducedTrainingPS
