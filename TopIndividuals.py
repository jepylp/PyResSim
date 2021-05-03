'''
Author:       James Porter 3140786
Supervisor:   Greg Walker, MA PhD (Cantab)

Store top individuals, set the max entries at initialization.
If the list grows to large it will drop the last entry after sorting.
'''

import Individual
import Individual_Diff
import random
import pandas as pd

class TopIndividuals:

    def __init__(self, max_entries, req_diff):

        self.max_entries = max_entries      # max number of entries in list
        self.individuals = []               # sorted indivduals
        self.average_npv = 0                # average for the top individuals
        self.req_diff = req_diff            # Number of genes required to be different
                                            # to be included on the list

        # module to handle checking the genes for differences
        self.ind_diff = Individual_Diff.Individual_Diff()

    def __repr__(self):
        s = ('top ' + str(self.max_entries)
            + ' Average NPV: ' + str(self.average_npv)
            + '\n')
        for ind in self.individuals:
            s = s + str(ind)
        return s

    # Add individual to the list, then sort the list
    def add_individual(self, individual):

        if self.similarity_check(individual):

            self.individuals.append(individual)
            self.individuals.sort(key=lambda individual: individual.fitness)

        self.remove_last_entry()
        self.update_average_npv()

    # Check to make sure thet Individual being added is different enough
    # Individuals genes must meet requirement set by req_diff
    def similarity_check(self, individual):

        # Go through each individual on the list
        for top_ind in self.individuals:
            # If returned count is <= req_diff
            if self.ind_diff.count_diff(individual, top_ind) <= self.req_diff:
                print('Too close: '
                    + str(self.ind_diff.count_diff(individual, top_ind)))
                return False    # individual is not different enough

        return True # individual is different enough



    # Remove the last entry from the list if it's too large
    def remove_last_entry(self):
        if len(self.individuals) > self.max_entries:
            print('removing: ' + str(self.individuals[-1]))
            del self.individuals[-1]

    # Average of the npv values
    def update_average_npv(self):
        total_npv = 0 # Running average

        # Go through each individual and get the npv
        for ind in self.individuals:

            #add npv to the running total npv
            total_npv = total_npv + ind.npv


        # Update average npv
        self.average_npv = total_npv / len(self.individuals)

    def pandas_table(self):

        # Pandas Table Setup
        pd.options.display.float_format = '{:.2f}'.format
        pandasColumns=(['Gen', 'Case', 'Fitness', 'NPV', 'ABS Diff', 'Parents'])
        pandasDataFrame = pd.DataFrame(columns=(pandasColumns))

        for individual in self.individuals:
            pandasDataFrame = pandasDataFrame.append(individual.pandas_table())

        return pandasDataFrame

def main():
    top_ind = TopIndividuals(4, 2)

    # Create Individuals to fill top 4
    ind = []
    ind.append(Individual.Individual(10, 0, 0, 'none', [1,1,0,0,0,0,0,0,0,0]))
    ind.append(Individual.Individual(10, 1, 0, 'none', [0,0,1,1,0,0,0,0,0,0]))
    ind.append(Individual.Individual(10, 2, 0, 'none', [0,0,0,0,1,1,0,0,0,0]))
    ind.append(Individual.Individual(10, 3, 0, 'none', [0,0,0,0,0,0,1,1,0,0]))

    # Change fitness
    ind[0].fitness = 100
    ind[1].fitness = 200
    ind[2].fitness = 300
    ind[3].fitness = 400

    # Change NPV
    ind[0].npv = 1100
    ind[1].npv = 1200
    ind[2].npv = 1300
    ind[3].npv = 1400

    for i in ind:
        top_ind.add_individual(i)

    print(top_ind)

    ### Done Setup for Testing ###

    # Adding an individual with high fitness, list should remain the same
    print('Adding high fitness individual, list should not change')

    ind = Individual.Individual(10, 4, 0, 'none', [0,0,0,0,0,0,0,0,0,1])
    ind.fitness = 5000
    ind.npv = 1110

    top_ind.add_individual(ind)
    print(top_ind)

    # Adding an individual with fitness 101, so should drop in second place
    print('Adding 101 fitness individual, list should not change')

    ind = Individual.Individual(10, 5, 0, 'none', [0,0,0,0,0,0,0,0,0,1])
    ind.fitness = 150
    ind.npv = 1110

    top_ind.add_individual(ind)
    print(top_ind)

    # Adding matching Individual
    # This should be rejected based on genes being too similar
    print('Adding matching individual, should be rejected')
    top_ind.add_individual(ind)
    print(top_ind)

    # Adding Individual with a single different gene
    # This should be rejected based on genes being too similar
    print('Adding individual with only a single difference, should be rejected')

    ind = Individual.Individual(10, 6, 0, 'none', [0,0,0,0,0,0,0,0,1,1])
    ind.fitness = 155
    ind.npv = 1115

    top_ind.add_individual(ind)
    print(top_ind)

    # Adding Individual with a two different genes
    # This should be rejected based on genes being too similar
    print('Adding individual two different genes, should be rejected')

    ind = Individual.Individual(10, 7, 0, 'none', [0,0,0,0,0,0,0,1,1,1])
    ind.fitness = 175
    ind.npv = 1215

    top_ind.add_individual(ind)
    print(top_ind)

    # Adding Individual with a three different genes
    # This should be accepted into the top 4, goes to top position
    print('Adding individual three different genes, should be accepted')

    ind = Individual.Individual(10, 8, 0, 'none', [0,0,0,0,0,0,1,1,1,1])
    ind.fitness = 90
    ind.npv = 4215

    top_ind.add_individual(ind)
    print(top_ind)


if __name__ == '__main__':
    main()
