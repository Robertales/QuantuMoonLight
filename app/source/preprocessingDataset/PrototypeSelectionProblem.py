import random
import statistics as s
import time as t
import numpy as np
from pathlib import Path
from deap import base
from deap import creator
from deap import tools
from sklearn.neighbors import KNeighborsClassifier

from app.source.preprocessingDataset import genetic_algorithm as ga
from app.source.utils import utils


# fitness for scikit-learn knn pesato #####
def fitness_knn(chromosome, X):
    num = len(chromosome)
    neigh = KNeighborsClassifier(
        n_neighbors=num, weights="distance"
    )
    neigh.fit(X[chromosome, :-2], X[chromosome, -1])
    accuracy = neigh.score(X[:, :-2], X[:, -1])
    return (accuracy, )


def runGeneticAlgorithm(
    x_train,
    number_of_reduced_training_instances,
    dataPath: Path,
):
    # PARAMETERS FOR THE  PROBLEM
    chromosome_size = number_of_reduced_training_instances
    upB = len(x_train) - 1
    lowB = 0

    # PARAMETERS FOR THE EVOLUTIVE ALGORITHM
    population = 100  # starting population
    generations = 5000000000  # number of generations
    num_evals_max = 1000  # number of solutions
    cxpb = 0.8  # crossov0er probability
    mutpb = 1.0  # mutation probability
    indpb = 0.15  # rate of independent mutations
    tournsize = 4  # number of individuals per tournament selection

    numRuns = 5  # numero di ripetizioni e vincitori

    # CREATE TOOLBOX
    # creates classes
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    # creates toolbox
    toolbox = base.Toolbox()
    # Ogni gene è un numero intero tra 0 e numero di righe -1
    toolbox.register("genes", random.randint, lowB, upB)
    # Ogni individuo è un cromosoma di geni. Ovvero un array di n numeri compresi tra 0 e numero di righe -1
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.genes, n=chromosome_size)
    # Inizializzazione casuale
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    # Crossover con metodo single-point, ovvero selezione casuale del punto di taglio nella codifica dei genitori
    toolbox.register("mate", tools.cxOnePoint)
    # Mutazione con probabilità indpb di cambiare un gene con un altro int compreso tra lowB e upB
    toolbox.register("mutate", tools.mutUniformInt, low=lowB, up=upB, indpb=indpb)
    # selezione con "torneo": si selezionano 5 individui e il migliore passa
    toolbox.register("select", tools.selTournament, tournsize=tournsize)
    # registrazione della funzione di valutazione
    toolbox.register("evaluate", fitness_knn, X=x_train)

    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    # CALL EVOLUTIVE ALGORITHMS
    gens = list()
    evaluations = list()
    bestInds = list()
    bestfits = list()
    times = list()

    for i in range(numRuns):
        # selects the best among all individuals
        hof = tools.HallOfFame(1)
        # To call the genetic algorithm
        time_Start = t.time()
        best_population, logbook = ga.deapGeneticAlgorithm(
            toolbox,
            population,
            cxpb,
            mutpb,
            generations,
            num_evals_max,
            stats,
            hof,
        )
        time_End = t.time()
        time = time_End - time_Start
        print("Time in seconds " + str(time))

        best = hof[0]
        bestf = best.fitness.values[0]

        # Aggiorno le statistiche, che poi scriverò nei report
        gens.append(logbook.select("gen")[-1])
        evaluations.append(logbook.select("nevals")[-1])
        bestInds.append(best)
        bestfits.append(bestf)
        times.append(time)

    # Scrivo i due report
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
    utils.writeXls(
        dataPath / xlsFileName, gens, evaluations, bestfits, times
    )
    utils.writeTxt(dataPath / txtFileName, bestInds)

    # Terminate le Run scelgo l'individuo migliore
    medianFitness = s.median_high(bestfits)
    indexM = bestfits.index(medianFitness)
    final_individual = bestInds[indexM]

    return final_individual, medianFitness
