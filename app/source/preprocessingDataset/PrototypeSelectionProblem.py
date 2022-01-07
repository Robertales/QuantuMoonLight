import random
import time as t
import numpy as np
import statistics as s
from deap import base
from deap import creator
from deap import tools
from app.source.preprocessingDataset import genetic_algorithm as ga
from app.source.utils import utils


# fitness for scikit-learn knn pesato #####
def fitness_knn(chromosome, x_train):
    # print(chromosome)
    num = len(chromosome)
    neigh = utils.classifier(num)
    neigh.fit(x_train[chromosome, :-2], x_train[chromosome, -1])
    accuracy = neigh.score(x_train[:, :-2], x_train[:, -1])
    return accuracy,


def runGeneticAlgorithXPS(number_of_solutions, x_train, number_of_reduced_training_instances):
    # PARAMETERS FOR THE  PROBLEM
    chromosome_size = number_of_reduced_training_instances
    reportName = "TestPS_"
    upB = len(x_train) - 1
    lowB = 0

    # PARAMETERS FOR THE EVOLUTIVE ALGORITHM
    population = 100  # starting population
    generations = 5000000000  # number of generations
    num_evals_max = number_of_solutions
    cxpb = 0.8  # crossov0er probability
    mutpb = 1.0  # mutation probability
    indpb = 0.15  # rate of independent mutations
    simpleMutpb = 0.15
    tournsize = 5  # number of individuals per tournament selection
    verb = True  # verbosity

    numRuns = 3

    # CREATE TOOLBOX
    # creates classes
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # creates toolbox
    toolbox = base.Toolbox()

    toolbox.register("genes", random.randint, lowB, upB)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.genes, n=chromosome_size)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    reportName += str(num_evals_max) + "_" + str(indpb) + "_" + str(cxpb) + "_" + str(tournsize)
    xlsFileName = reportName + ".xlsx"
    txtFileName = reportName + ".txt"

    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutUniformInt, low=lowB, up=upB, indpb=indpb)
    toolbox.register("select", tools.selTournament, tournsize=tournsize)
    toolbox.register("evaluate", fitness_knn, x_train=x_train)

    # CALL EVOLUTIVE ALGORITHMS
    gens = list()
    evaluations = list()
    bestInds = list()
    bestfits = list()
    times = list()

    for i in range(numRuns):
        # selects the best among all individuals
        hof = tools.HallOfFame(1)

        # To call the memetic algorithm
        # memeticAlgorithm(toolbox, population, cxpb, mutpb, generations,  num_evals_max, population//2, mgen,stats,  hof )

        # To call the genetic algorithm
        time_Start = t.time()

        best_population, logbook = ga.deapGeneticAlgorithm(toolbox, population, cxpb, mutpb, generations, num_evals_max,
                                                           stats, hof)
        time_End = t.time()

        time = time_End - time_Start
        print("Time in seconds " + str(time))

        # best=best_ind
        best = hof[0]

        bestf = best.fitness.values[0]
        # print(best)
        # print(bestf)

        gens.append(logbook.select('gen')[-1])
        evaluations.append(logbook.select('nevals')[-1])
        bestInds.append(best)
        bestfits.append(bestf)
        times.append(time)

        utils.writeXls(xlsFileName, gens, evaluations, bestfits, times)

        utils.writeTxt(txtFileName, bestInds)

    # print(bestfits)
    medianFitness = s.median_high(bestfits)
    print("Fitness of the obtained reduced individual %f" % medianFitness)
    indexM = bestfits.index(medianFitness)
    final_individual = bestInds[indexM]

    return final_individual, medianFitness
