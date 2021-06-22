'''
Author:       James Porter

Fitness calculator, reads in the case file to
determine the npv and abs difference
'''

import numpy as np
from flowrate import Flowrate


def rms (historical_flowrates, individual_flowrates) -> float:
    '''
    Root mean squared error
    reference: https://www.statology.org/mean-squared-error-python/
    '''

    # Only flowrates are required for comparison
    individual_flowrates = individual_flowrates[0:len(historical_flowrates)]

    historical_flowrates = np.array(historical_flowrates)
    individual_flowrates = np.array(individual_flowrates)

    return np.sqrt(((historical_flowrates - individual_flowrates) ** 2).mean())

def npv (individual_flowrates: Flowrate, rate: float) -> float:
    '''
    Calculate npv of case given a discount rate, case time stamps are used
    '''

    return_npv = 0 # Initialize npv

    # npv = future value / (1 + rate) ^ time
    # sum up all net present values for the total npv of the well

    for step in individual_flowrates:

        return_npv = return_npv + (step.avg_flowrate / (1 + rate) ** step.eom_time)

    return return_npv

def convert_days_to_flowtime(days:int, days_per_year:int, year:int) -> float:
    '''
    convert the days per year, to a floating value for the time in years
    '''

    return days / days_per_year + year

def rms_normalize_fitness(population):
    '''
    ## Currently rms and npv are split becuase I didn't know how close they
    ## would be

    Normalize the fitness values for the entire population,
    if a generation is sent then it will normalize the fitness for that
    generation.

    1. Get the population to be run
    2. Total the fitness values for the population
    3. Loop through fitness values
        Inverse fitness = Total fitness / fitness values
        Total of inverse fitness for next step
    4. Loop through inverse fitness
        Normalized fitness = inverse fitness / total inverse fitness
        Individual cumulative normalized fitness = running total of normalized

    There might be some rounding issues
    '''

    # initialize variables
    total_fitness = 0
    running_pop = active_pop(population)

    # first loop total the fitness values for the population
    for ind in running_pop:
        total_fitness = total_fitness + ind.fitness

    inverse_normalize(running_pop, total_fitness)

def npv_normalize_fitness(population):

    '''
    ## Currently rms and npv are split becuase I didn't know how close they
    ## would be
    Normalize the fitness based on the average npv of the population

    1. Get the population to be run
    2. Total the NPV of all individuals, then get the average npv
    3. Total the fitness values for the population
    4. Loop through fitness values
        Inverse fitness = Total fitness / fitness values
        Total of inverse fitness for next step
    5. Loop through inverse fitness
        Normalized fitness = inverse fitness / total inverse fitness
        Individual cumulative normalized fitness = running total of normalized

    There might be some rounding issues
    '''

    # initialize variables
    total_npv = 0
    total_fitness = 0
    running_pop = active_pop(population)

    # second loop gets the total npv and population that was run
    for ind in running_pop:
        total_npv = total_npv + ind.npv

    average_npv = total_npv / len(running_pop)

    print('avg: %s' % average_npv)

    # third loop sets the fitness as the abs difference between the
    # individuals npv and the average npv
    for ind in running_pop:
        ind.fitness = abs(ind.npv - average_npv)

        # can't divide by zero so set value close to 0
        # very unlikely but you never know.
        if ind.fitness == 0:
            ind.fitness = 1

        total_fitness = total_fitness + ind.fitness

    inverse_normalize(running_pop, total_fitness)

def active_pop(population):
    '''
    Returns the portion of the population that should have been run
    through flow
    '''

    running_pop = []

    for ind in population:
        if ind.run:
            running_pop.append(ind)

    return running_pop

def inverse_normalize(population, total_fitness):
    '''
    set the inverse fitness and then the normalized fitness for each
    individual in a population
    '''
    total_inverse_fitness = 0
    running_cnf = 0 # running total of cumalative normalized fitness

    # first loop set the inverse fitness
    for ind in population:
        ind.inverse_fitness = total_fitness / ind.fitness
        total_inverse_fitness = total_inverse_fitness + ind.inverse_fitness

    # second loop set the normalized fitness and cumaltive normalized fitness
    for ind in population:
        ind.normalized_fitness = ind.inverse_fitness / total_inverse_fitness
        running_cnf = running_cnf + ind.normalized_fitness
        ind.cnf = running_cnf
