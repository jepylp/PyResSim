'''
Author:       James Porter

Fitness calculator, reads in the case file to
determine the npv and abs difference
'''

from pathlib import Path        # Converts file/folder path to which ever os
import numpy as np

# Root mean squared error
# reference: https://www.statology.org/mean-squared-error-python/
def rms (history_flowrates, individual_flowrates) -> float:

    # Only flowrates are required for comparison
    individual_flowrates = individual_flowrates[0:len(history_flowrates)]
    
    history_flowrates = np.array(history_flowrates)
    individual_flowrates = np.array(individual_flowrates)

    return np.sqrt(((history_flowrates - individual_flowrates) ** 2).mean())

# Calculate npv of case given a discount rate, case time stamps are used
def npv (individual_flowrates, individual_time, rate: float) -> float:
    return_npv = 0 # Initialize npv

    # npv = future value / (1 + rate) ^ time
    # sum up all net present values for the total npv of the well

    for step in individual_time:

        return_npv = return_npv + (individual_flowrates[step] / (1 + rate) ** individual_time[step])

    return return_npv

# convert the days per year, to a floating value for the time in years
def convert_days_to_flowtime(
        days:int, 
        days_per_year:int, 
        year:int
    ) -> float:

        return (days / days_per_year + year)

def normalize_fitness(
    population
):
    running_normalized_fitness = 0  # Initialize

    for ind in population:
        # Running total of the normailized fitness, full total
        # should be 1.0 but there are some rounding issues
        running_normalized_fitness = (running_normalized_fitness +
            ind.normalized_fitness)

        # Print the running total of the normalized fitness
        print(str(ind.case) + ': ' +
            str(running_normalized_fitness))

        ind.normalized_fitness = normalize_fitness
