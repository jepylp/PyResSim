'''
Author:       James Porter 3140786
Supervisor:   Greg Walker, MA PhD (Cantab)

Generate an population of individuals

Inputs:
pop_size -      Populations size to generate for this generation
gene_size -     Number of genes per individual (used for generating individual)


Variables:
individuals -   Array to store the individuals


Can create a blank population. Helpful when creating a the next generations
and not keeping the generations.

'''

import Individual
import pandas as pd

class Generation:

    # If no individuals passed in then initialize the array and create a pop
    def __init__(self, mode, generation, pop_size = 0, gene_size = 0):

        #initialize all values of the individual
        self.individuals = []

        # Method holds the method used to create generation
        # Expected:
        #   random
        #   standard
        #   fitness
        #   npv
        #   npv_extremes

        self.mode = mode

        # generation number
        self.generation = generation


        # Input check
        # no individuals passed in then initialize the array and create a pop

        if pop_size > 0 and gene_size <= 1:
            print ('gene_size required for population creation')
        elif pop_size != 0:
            self.generate_generation(pop_size, gene_size)

    def __repr__(self):
        s = ('mode: ' + self.mode + '\n')
        for ind in self.individuals:
            s = (s + str(ind))

        return s

    # Randomly set the genes of a given size
    def generate_generation(self, pop_size, gene_size):
        for i in range(pop_size):
            self.individuals.append(Individual.Individual(gene_size, i,
                self.generation))

    # Add individual to the generation
    # Currently used for the adding children
    def add_individual(self, individual):
        self.individuals.append(individual)

    def print_generation(self):
        s = ('mode: ' + self.mode + '\n')
        for ind in self.individuals:
            s = (s + str(ind))
        return s

    def pandas_table(self):

        # Pandas Table Setup
        pd.options.display.float_format = '{:.2f}'.format
        pandasColumns=(['Gen', 'Case', 'Fitness', 'NPV', 'ABS Diff', 'Parents'])
        pandasDataFrame = pd.DataFrame(columns=(pandasColumns))

        for individual in self.individuals:
            if individual.fitness != 999999999.99:
                pandasDataFrame = pandasDataFrame.append(individual.pandas_table())

        return pandasDataFrame


def main():
    ## Generation Testing ##
    print ('Create generation of 10, with 25 genes')
    gen = Generation('test', 0, 10, 25)

    print(gen.print_generation())

    print('Adding Individual')
    gen.add_individual(Individual.Individual(25, 0, 1))
    print(gen.print_generation())

    gen.pandas_table()

if __name__ == '__main__':
    main()
