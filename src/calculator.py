'''
Author:       James Porter

Fitness calculator, reads in the case file to
determine the npv and abs difference
'''

import numpy as np


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

def npv (individual_flowrates, individual_time, rate: float) -> float:
    '''
    Calculate npv of case given a discount rate, case time stamps are used
    '''

    return_npv = 0 # Initialize npv

    # npv = future value / (1 + rate) ^ time
    # sum up all net present values for the total npv of the well

    for step in individual_time:

        return_npv = return_npv + (individual_flowrates[step] / (1 + rate) ** individual_time[step])

    return return_npv

def convert_days_to_flowtime(days:int, days_per_year:int, year:int) -> float:
    '''
    convert the days per year, to a floating value for the time in years
    '''

    return days / days_per_year + year

def normalize_fitness(population):
    '''
    Normalize the fitness values for the entire population,
    if a generation is sent then it will normalize the fitness for that
    generation.

    1. Total the fitness values for the population
    2. Loop through fitness values
        Inverse fitness = Total fitness / fitness values
        Total of inverse fitness for next step
    3. Loop through inverse fitness
        Normalized fitness = inverse fitness / total inverse fitness
        Individual cumulative normalized fitness = running total of normalized

    There might be some rounding issues
    '''
    # first loop total the fitness values for the population
    total_fitness = 0  # initialize

    for ind in population:
        total_fitness = total_fitness + ind.fitness

    # second loop set the inverse fitness
    total_inverse_fitness = 0 # running total of inverse fitness

    for ind in population:
        ind.inverse_fitness = total_fitness / ind.fitness
        total_inverse_fitness = total_inverse_fitness + ind.inverse_fitness

    # third loop set the normalized fitness and cumaltive normalized fitness
    running_cnf = 0 # running total of cumalative normalized fitness

    for ind in population:
        ind.normalized_fitness = ind.inverse_fitness / total_inverse_fitness
        running_cnf = running_cnf + ind.normalized_fitness
