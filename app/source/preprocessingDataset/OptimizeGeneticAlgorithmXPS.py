#!C:\Users\Gennaro\Miniconda3\envs\python\python.exe
#print("Content-Type: text/html\n")
import random
import time as t

import numpy as np
from deap import base
from deap import creator
from deap import tools


import genetic_algorithm as ga


import app.source.utils

import statistics as s

import PrototypeSelectionProblem as ps




def optimizeGeneticAlgorithXPS(number_of_solutions, x_train, number_of_reduced_training_instances):


    ##### PARAMETERS FOR THE  PROBLEM ############################################################
    chromosome_size=number_of_reduced_training_instances
    reportName="TestPS_"
    upB=len(x_train)-1
    lowB=0


    ### PARAMETERS FOR THE EVOLUTIVE ALGORITHM ###############################################
    population = 100# starting population
    generations = 5000000000# number of generations
    num_evals_max=number_of_solutions
    mutpb = 1.0  # mutation probability
    verb = True  # verbosity

    numRuns=10




    ### CREATE TOOLBOX ################################################################################
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

    #mps=[0.05, 0.1, 0.15, 0.2, 0.25]
    #cxs=[0.7,0.75,0.8,0.85,0.9]
    #ts=[2,3,5]

    imps=[0.02]
    cxs=[0.8]
    ts=[5]

    for m in imps:
        for c in cxs:
            for td in ts:
                reportName += str(num_evals_max)+ "_" + str(m) + "_" + str(c) + "_" + str(td)
                xlsFileName=reportName+ ".xlsx"
                txtFileName=reportName+ ".txt"

                toolbox.register("mate", tools.cxOnePoint)
                toolbox.register("mutate", tools.mutUniformInt, low=lowB, up=upB, indpb=m)
                toolbox.register("select", tools.selTournament, tournsize=td)
                toolbox.register("evaluate", ps.fitness_knn, x_train=x_train)


                #### CALL EVOLUTIVE ALGORITHMS ##########################################################################
                gens=list()
                evaluations=list()
                bestInds=list()
                bestfits=list()
                times=list()




                for i in range(numRuns):


                    # selects the best among all individuals
                    hof = tools.HallOfFame(1)

                    #To call the memetic algorithm
                    #memeticAlgorithm(toolbox, population, cxpb, mutpb, generations,  num_evals_max, population//2, mgen,stats,  hof )

                    #To call the genetic algorithm
                    time_Start=t.time()

                    best_population,logbook=ga.deapGeneticAlgorithm(toolbox, population, c, mutpb, generations, num_evals_max, stats,  hof)
                   #best_population,logbook=ga.simpleGeneticAlgorithm(toolbox, population, cxpb, simpleMutpb, generations, num_evals_max, stats,  hof)
                   # best_population, logbook = ga.simpleElitistGeneticAlgorithm(toolbox, population, cxpb, simpleMutpb, generations,num_evals_max, stats, hof)
                   # best_population,logbook=ga.geneticAlgorithm(toolbox, population, cxpb, simpleMutpb, generations, num_evals_max, stats,  hof)
                    #best_ind,logbook=hc.hillclimbing(toolbox, num_evals_max)
                    time_End=t.time()

                    time=time_End - time_Start
                    print("Time in seconds " + str(time))

                    #best=best_ind
                    best=hof[0]



                    bestf=best.fitness.values[0]
                    print(best)
                    print(bestf)


                    gens.append(logbook.select('gen')[-1])
                    evaluations.append(logbook.select('nevals')[-1])
                    bestInds.append(best)
                    bestfits.append(bestf)
                    times.append(time)

                    utils.writeXls(xlsFileName, gens, evaluations, bestfits, times)

                    utils.writeTxt(txtFileName, bestInds)




                utils.writeXls(xlsFileName, gens, evaluations, bestfits,times)



