import random
import statistics as s
import time as t
import numpy as np
from pathlib import Path
from deap import base
from deap import creator
from deap import tools
from pandas import DataFrame
from sklearn.neighbors import KNeighborsClassifier
from app.source.preprocessingDataset import genetic_algorithm as ga
from app.source.utils import utils


def fitness_knn(chromosome, X: DataFrame.values):
    """
    This function evaluate the chromosome: the fitness value is the accuracy of the classification with a
    KNeighborsClassifier, trained with the rows specified by the chromosome

    :param chromosome: individual to evaluate, array of index of rows
    :param X: dataset

    :return: fintess value that corresponds to the accuracy of the classification
    """
    num = len(chromosome)
    neigh = KNeighborsClassifier(
        n_neighbors=num, weights="distance"
    )
    # Fit the classifier with data selected by the chromosome
    neigh.fit(X[chromosome, :-2], X[chromosome, -1])

    # Test the accuracy of the classifier with data from X
    X_data = X[:, :-2]  # Test samples from X
    X_labels = X[:, -1]  # True labels from X
    accuracy = neigh.score(X_data, X_labels)

    return accuracy,


def drawGraph(idRun, gen, fit_max, fit_min, size_avgs, time, dataPath):
    """
    This function draw the graph releative to the run #idRun.

    :param idRun: id of the run
    :param gen: number of generations for the run
    :param fit_max: list of max fitness value for each generation of the run
    :param fit_min: list of min fitness value for each generation of the run
    :param size_avgs: list of average fitness value for each generation of the run
    :param time: time spent for the run
    :param dataPath: path that point to the location to save the plot
    """
    import matplotlib.pyplot as plt

    fig, ax1 = plt.subplots()
    line1 = ax1.plot(gen, fit_max, "b-", label="Maximum Fitness")
    line2 = ax1.plot(gen, fit_min, "g-", label="Minimum Fitness")
    line3 = ax1.plot(gen, size_avgs, "r-", label="Average Size")
    ax1.set_xlabel("Generation", fontsize=12)
    ax1.set_ylabel("Fitness", fontsize=12)
    lns = line1 + line2 + line3
    labs = [lines.get_label() for lines in lns]

    ax1.legend(lns, labs, loc="lower right")
    plt.suptitle("Genetic Run #" + str(idRun), fontsize=15)
    plt.title("Time to run: " + str(time), fontsize=15)

    plt.savefig(dataPath / ('graphPCA' + str(idRun)))
    plt.show()


def runGeneticAlgorithm(
    X: DataFrame.values,
    number_of_reduced_training_instances: int,
    dataPath: Path,
):
    """
    This functions set the toolbox for the genetic algorithm, write statistics in xlsx file and return the best
    individual that represents the set of best rows

    :param X: dataset that is going to be reduced with PS
    :param number_of_reduced_training_instances: new number of rows and length of chromosome
    :param dataPath: path that points to the location to write statistics file

    :return: the best individual and its fitness value
    """
    # PARAMETERS FOR THE  PROBLEM
    chromosome_size = number_of_reduced_training_instances
    upB = len(X) - 1
    lowB = 0

    # PARAMETERS FOR THE EVOLUTIVE ALGORITHM
    population = 100  # starting population
    generations = 30  # max number of generations
    num_evals_max = 1000  # max number of evaluations of fitness
    cxpb = 0.5  # crossover probability
    mutpb = 0.15  # mutation probability
    indpb = 0.05  # independent probability for each attribute (gene) to be mutated.
    tournsize = 5  # number of individuals per tournament selection

    numRuns = 3  # number of runs of GA

    # CREATE TOOLBOX
    # creates classes a runtime
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    # creates toolbox
    toolbox = base.Toolbox()
    # each gene is an integer between 0 and numRows -1
    toolbox.register("genes", random.randint, lowB, upB)
    # Ogni individuo è un cromosoma di geni. Ovvero un array di n numeri compresi tra 0 e numero di righe -1
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.genes, n=chromosome_size)
    # Inizializzazione casuale di n individui
    toolbox.register("population", tools.initRepeat, list, toolbox.individual, n=population)
    # Crossover con metodo single-point, ovvero selezione casuale del punto di taglio nella codifica dei genitori
    toolbox.register("mate", tools.cxOnePoint)
    # Mutazione con probabilità indpb di cambiare un gene con un altro int compreso tra lowB e upB
    toolbox.register("mutate", tools.mutUniformInt, low=lowB, up=upB, indpb=indpb)
    # selezione con "torneo": per generare la prossima generazione ogni individuo è sostituito
    # dal migliore (fittest) di 5 individui scelti a casa dalla generazione corrente
    toolbox.register("select", tools.selTournament, tournsize=tournsize, k=population)
    # registrazione della funzione di valutazione da massimizzare
    toolbox.register("evaluate", fitness_knn, X=X)

    # The hall of fame contains the best individual that ever lived in the population during the entire run.
    hof = tools.HallOfFame(1)

    # Computa statistiche sulla generazione
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    # CALL EVOLUTIVE ALGORITHMS
    gens = list()
    evaluations = list()
    bestInds = list()
    bestFits = list()
    times = list()

    for i in range(numRuns):
        print("\nGenetic Run #" + str(i+1))

        # Clear the hall of fame before every run
        hof.clear()

        # Call the genetic algorithm
        time_Start = t.time()
        best_population, logbook = ga.deapGeneticAlgorithm(
            toolbox,
            cxpb,
            mutpb,
            generations,
            num_evals_max,
            stats,
            hof,
            verbose=False  # Set True to print in the console info about generations
        )
        time_End = t.time()
        time = time_End - time_Start

        # Select the best individual of the actual run and his fitness value
        best_ind = hof[0]
        best_ind_fit = best_ind.fitness.values[0]
        # save in the list the best individuals
        bestInds.append(best_ind)
        bestFits.append(best_ind_fit)

        print("Time in seconds " + str(time))
        print("Best individual is " + str(best_ind))
        print("With fitness value: " + str(best_ind_fit))

        # Update the statistics that will be written in the reports
        gens.append(logbook.select("gen")[-1])
        evaluations.append(logbook.select("nevals")[-1])
        times.append(time)

        # draw the graph of the current run
        gen = logbook.select("gen")
        fit_max = logbook.select("max")
        fit_min = logbook.select("min")
        size_avgs = logbook.select("avg")
        drawGraph(i+1, gen, fit_max, fit_min, size_avgs, time, dataPath)

        # end of run

    # write two reports
    reportName = "TestPS_"
    reportName += (
            str(num_evals_max)
            + "_"
            + str(indpb)
            + "_"
            + str(cxpb)
            + "_"
            + str(tournsize)
    )
    xlsFileName = reportName + ".xlsx"
    txtFileName = reportName + ".txt"
    utils.writeXls(dataPath / xlsFileName, gens, evaluations, bestFits, times)
    utils.writeTxt(dataPath / txtFileName, bestInds)

    # finished the run and choose best individual
    medianFitness = s.median_high(bestFits)
    indexM = bestFits.index(medianFitness)
    final_individual = bestInds[indexM]

    return final_individual, medianFitness
