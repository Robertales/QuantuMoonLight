import pathlib
import pandas as pd
from app.source.preprocessingDataset import (
    PrototypeSelectionProblem as ps,
)


def callPrototypeSelection(
        path: pathlib.Path, number_of_reduced_training_instances=10
):
    """
    This function executes the prototype selection on the given dataset

    :param path: string that points to the location of the dataset that is going to be reduced with PS
    :param number_of_reduced_training_instances: new number of raws
    :return: string that points to the location of the dataset preprocessed with PS
    :rtype: str
    """

    # Create a dataframe from csv
    df = pd.read_csv(path)
    X = df.values

    # The evolution ends when the maximum number of evaluations of fitness (corresponding to the number of
    # solutions evaluated) is achieved

    # Run evolution
    chromosomeToEvaluate, fitness = ps.runGeneticAlgorithm(
        X,
        number_of_reduced_training_instances,
        path.parent,
    )
    print("Fitness of the obtained reduced individual %f" % fitness)
    print("Best selection of instance: ")
    print(chromosomeToEvaluate)

    pathFileReducedTrainingPS = pathlib.Path(path).parent
    pathFileReducedTrainingPS = (
            pathFileReducedTrainingPS / "reducedTrainingPS.csv"
    )

    # Recupero nomi colonne e scrivo in reducedTrainingPS.csv
    PS_df = pd.DataFrame(data=df.values[chromosomeToEvaluate, :], columns=df.columns)
    PS_df.to_csv(pathFileReducedTrainingPS, index=False)

    return pathFileReducedTrainingPS.__str__()
