#This code was developed for the paper
#G. Acampora and A. Vitiello, "TSSweb: a Web Tool for Training Set Selection," 
#2020 IEEE International Conference on Fuzzy Systems (FUZZ-IEEE), 2020, pp. 1-7, doi: 10.1109/FUZZ48607.2020.9177677.

from __future__ import division
import random
from deap import tools


def deapGeneticAlgorithm(
    toolbox,
    cxpb,
    mutpb,
    generations,
    num_evals_max,
    stats=None,
    hof=None,
    verbose=__debug__,
):
    """
    This function use the toolbox and the input parameters to run the genetic algorithm
    with mutation probability on each individual in each generation the population is replace
    with offspring.

    :param toolbox: deap toolbox that contains all the functionality for the genetic algorithm, like
    individuals, population, crossover, mutation, selection and fitness evaluation.
    :param cxpb: probability of crossover
    :param mutpb: probability of mutation
    :param generations: max number of generations
    :param num_evals_max: max number of evaluations
    :param stats: statistic tool
    :param hof: Hall Of Fame that store the best indivual of the entire population
    :param verbose: if True, print in the console logs and statistics for each generations

    :return: final population and logbook of statistics for the run
    """
    logbook = tools.Logbook()
    logbook.header = ["gen", "nevals_gen", "nevals"] + (
        stats.fields if stats else []
    )

    # Create an initial population of individuals
    pop = toolbox.population()

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if hof is not None:
        hof.update(pop)

    record = stats.compile(pop) if stats else {}
    logbook.record(
        gen=0, nevals_gen=len(invalid_ind), nevals=len(invalid_ind), **record
    )
    if verbose:
        print(logbook.stream)
        ind = tools.selBest(pop, 1)
        print("ind best" + str(ind[0].fitness.values))

    g = 0
    # The evolution ends when the maximum number of evaluations of fitness is achieved
    while g < generations and logbook.select("nevals")[-1] < num_evals_max:
        # Select the next generation individuals
        offspring = toolbox.select(pop)
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

        # Since the content of some of our offspring changed during the last two step,
        # we now need to re-evaluate their fitnesses. To save time and resources,
        # we just map those offspring which fitnesses were marked invalid.
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # update the Hall of Fame with the offspring.
        if hof is not None:
            hof.update(offspring)

        # update the logbook
        record = stats.compile(offspring) if stats else {}
        logbook.record(
            gen=g + 1,
            nevals_gen=len(invalid_ind),
            nevals=logbook.select("nevals")[-1] + len(invalid_ind),
            **record
        )
        if verbose:
            print(logbook.stream)
            ind = tools.selBest(offspring, 1)
            print("ind best" + str(ind[0].fitness.values))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        g = g + 1

    return pop, logbook
