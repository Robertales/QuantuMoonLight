#!C:\Users\Gennaro\Miniconda3\envs\python\python.exe
#print("Content-Type: text/html\n")
from __future__ import division
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

from deap import base
from deap import creator
from deap import tools
from deap import algorithms
from collections import Sequence
from matplotlib import pyplot



#genetic algorithm with mutation probability on each individual and in each generation the population is replace with offpring
def deapGeneticAlgorithm(toolbox, pop_size, cxpb, mutpb, generations, num_evals_max, stats=None,hof=None, verbose=__debug__):

    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals_gen', 'nevals'] + (stats.fields if stats else [])

    pop = toolbox.population(n=pop_size)


   # print(pop)


    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if hof is not None:
        hof.update(pop)

    record = stats.compile(pop) if stats else {}
    logbook.record(gen=0, nevals_gen=len(invalid_ind),  nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    ind = tools.selBest(pop, 1)
    print("ind best" + str(ind[0].fitness.values))

    g=0
    while g < generations and logbook.select("nevals")[-1] < num_evals_max:
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cxpb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        # Apply mutation on the offspring
        for mutant in offspring:
            if random.random() < mutpb:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        if hof is not None:
            hof.update(offspring)

        record = stats.compile(offspring) if stats else {}
        logbook.record(gen=g+1, nevals_gen=len(invalid_ind),nevals=logbook.select("nevals")[-1] + len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

        ind = tools.selBest(offspring, 1)
        print("ind best" + str(ind[0].fitness.values))

        #Evaluate the individuals with an invalid fitnes
        # The population is entirely replaced by the offspring
        pop[:] = offspring

        g = g+1

    return pop,logbook


#genetic algorithm with mutation probability on each gene and in each generation the population is replace with offpring
def simpleGeneticAlgorithm(toolbox, pop_size, cxpb, mutpb, generations, num_evals_max, stats=None,hof=None, verbose=__debug__):

    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals_gen', 'nevals'] + (stats.fields if stats else [])

    pop = toolbox.population(n=pop_size)


    #print(pop)


    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if hof is not None:
        hof.update(pop)

    record = stats.compile(pop) if stats else {}
    logbook.record(gen=0, nevals_gen=len(invalid_ind),  nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    ind = tools.selBest(pop, 1)
    print("ind best" + str(ind[0].fitness.values))

    g=0
    while g < generations and logbook.select("nevals")[-1] < num_evals_max:
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cxpb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        # Apply mutation on the offspring
        for mutant in offspring:
            flag, ind = toolbox.mutate(mutant, indpb=mutpb)
            if flag:
               del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        if hof is not None:
            hof.update(offspring)

        record = stats.compile(offspring) if stats else {}
        logbook.record(gen=g+1, nevals_gen=len(invalid_ind),nevals=logbook.select("nevals")[-1] + len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

        ind = tools.selBest(offspring, 1)
        print("ind best" + str(ind[0].fitness.values))

        #Evaluate the individuals with an invalid fitnes
        # The population is entirely replaced by the offspring
        pop[:] = offspring

        g = g+1

    return pop,logbook

#genetic algorithm with mutation probability on each gene and in each generation the population is replace with the best individuals among population and offpring
def geneticAlgorithm(toolbox, pop_size, cxpb, mutpb, generations, num_evals_max, stats=None,hof=None, verbose=__debug__):

    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals_gen', 'nevals'] + (stats.fields if stats else [])

    pop = toolbox.population(n=pop_size)


    #print(pop)


    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if hof is not None:
        hof.update(pop)

    record = stats.compile(pop) if stats else {}
    logbook.record(gen=0, nevals_gen=len(invalid_ind),  nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    ind = tools.selBest(pop, 1)
    print("ind best" + str(ind[0].fitness.values))

    g=0
    while g < generations and logbook.select("nevals")[-1] < num_evals_max:
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cxpb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

       # Apply mutation on the offspring by a mutpb on each gene
        for mutant in offspring:
            flag, ind = toolbox.mutate(mutant, indpb=mutpb)
            if flag:
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        if hof is not None:
            hof.update(offspring)

        record = stats.compile(offspring) if stats else {}
        logbook.record(gen=g+1, nevals_gen=len(invalid_ind),nevals=logbook.select("nevals")[-1] + len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

        ind = tools.selBest(offspring, 1)
        print("ind best" + str(ind[0].fitness.values))

        #Evaluate the individuals with an invalid fitnes
        # The population is entirely replaced by the best individuals of the offspring and the old population
        pop[:] = tools.selBest(offspring+pop, pop_size)

        g = g+1

    return pop,logbook

#genetic algorithm with mutation probability on each gene and in each generation the population is replaced with the offpring but with elitism
def simpleElitistGeneticAlgorithm(toolbox, pop_size, cxpb, mutpb, generations, num_evals_max, stats=None,hof=None, verbose=__debug__):

    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals_gen', 'nevals'] + (stats.fields if stats else [])

    pop = toolbox.population(n=pop_size)


    #print(pop)


    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if hof is not None:
        hof.update(pop)

    record = stats.compile(pop) if stats else {}
    logbook.record(gen=0, nevals_gen=len(invalid_ind),  nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    ind = tools.selBest(pop, 1)
    print("ind best" + str(ind[0].fitness.values))

    g=0
    while g < generations and logbook.select("nevals")[-1] < num_evals_max:

        #elitism
        elitist = toolbox.clone(tools.selBest(pop,1)[0])

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cxpb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        # Apply mutation on the offspring
        for mutant in offspring:
            flag, ind = toolbox.mutate(mutant, indpb=mutpb)
            if flag:
               del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        if hof is not None:
            hof.update(offspring)

        record = stats.compile(offspring) if stats else {}
        logbook.record(gen=g+1, nevals_gen=len(invalid_ind),nevals=logbook.select("nevals")[-1] + len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

        ind = tools.selBest(offspring, 1)
        print("ind best" + str(ind[0].fitness.values))

        #Evaluate the individuals with an invalid fitnes
        # The population is entirely replaced by the offspring
        pop[:] = tools.selBest(offspring, pop_size -1)
        pop.append(elitist)

        g = g+1

    return pop,logbook