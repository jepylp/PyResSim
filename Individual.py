'''
Author:       James Porter 3140786
Supervisor:   Greg Walker, MA PhD (Cantab)

Generate an individual

Variables:
genes - array of 0s and 1s, generated if no genes are passed in
case -  Case number associated with genes
fitness -   root mean squared, placeholder 9999999 for low chance of selection
        just in case
npv -   net present value, placeholder 0 for low chance of selection

'''
import random
import pandas as pd

class Individual:

    def __init__(self, size, case, generation, parents = 'none', genes = 'none'):

        #initialize all values of the individual
        self.genes = []                 # Genes made up of 0s, and 1s.
        self.case = case                # Case number for individual
        self.generation = generation    # Generation individual belongs to
        self.parents = parents
        self.fitness = 0                # Fitness value
        self.inverse_fitness = 0        # 1 / Fitness
        self.normalized_fitness = 0     # used to determine which parents for
                                        # the next generation. can use fitness,
                                        # or NPV
        self.run_me = False             # Determine if the case should be run

        self.npv = 0                    # NPV from case run in flow
        self.abs_difference = 0         # Distance value is away from average
                                        # The further away the more likely to
                                        # be selected for the next generation

        # Input check
        if genes == 'none' and size <= 1:
            print ('Gene size too small')
        elif genes == 'none':
            self.generate_genes(size)
        else:
            self.genes = genes

    def __repr__(self):
        s = ('gen: ' + str(self.generation)
            + ' case: ' + str(self.case)
            + ', ' + str(self.genes)
            + ', f: ' + str(self.fitness)
            + ' if: ' + str(self.inverse_fitness)
            + ' nf: ' + str(self.normalized_fitness)
            + ' npv: ' + str(self.npv)
            + ' abs_diff: ' + str(self.abs_difference)
            + ' parents: ' + str(self.parents)
            + '\n')

        return s

    # Randomly set the genes of a given size
    def generate_genes(self, size):
        for i in range(size):
            self.genes.append(random.randint(0,1))

    # Set the normalize fitness
    # float wrapper around the values incase a int is sent in
    def set_normalized_fitness(self, mode, denominator):
        if mode == 'fitness':
            self.normalized_fitness = float(self.inverse_fitness) / float(denominator)
            print(self.normalized_fitness)
        elif mode == 'npv':
            self.normalized_fitness = float(self.abs_difference) / float(denominator)
        else:
            print('Invalid mode')

    # Return self as a pandas tables
    def pandas_table(self):

        # Pandas Table Setup
        pd.options.display.float_format = '{:.2f}'.format
        pandasColumns=(['Gen', 'Case', 'Fitness', 'NPV', 'ABS Diff', 'Parents'])
        pandasDataFrame = pd.DataFrame(columns=(pandasColumns))

        pandasDataFrame = pandasDataFrame.append({
            'Gen': self.generation,
            'Case': self.case,
            'Fitness': self.fitness,
            'NPV': self.npv,
            'ABS Diff': self.abs_difference,
            'Parents': self.parents
            } , ignore_index = True)

        return pandasDataFrame

    # Compare genes between self and provided genes and return the number of
    # matching genes (same gene, in the same position)
    def count_matches(self, individual):

        matches = 0;

        for x in range(len(individual.genes)):
            if individual.genes[x] == self.genes[x]:
                matches = matches + 1

        return matches

    # Compare genes between self and provided genes and return the number of
    # different genes (same gene, in the same position)
    def count_differences(self, individual):

        differences = 0

        for x in range(len(individual.genes)):
            if individual.genes[x] != self.genes[x]:
                differences = differences + 1

        return differences


def main():
    ## Testing ##
    # 10 Gene creation test
    print('Creating individual with 10 genes')
    ind = Individual(10, 0, 0)
    print(ind)

    # 3 Gene provided test
    print('Creating individual with [1,0,1] genes')
    ind = Individual(0, 0, 1, 'none', [1,0,1])
    print(ind)

    # Too few genes test
    print('Individual should have too few genes')
    ind = Individual(0, 0, 0)

    # Create 10 individuals, 10 genes each
    print('create 10 individuals with 10 gene per individuals')
    for i in range(10):
        x = Individual(10, i, 1)
        print(x)

    # Test Normalized Fitness
    print('Set normalized fitness test')
    print('inverse fitness = 5, abs difference = 2, denominator = 10')
    print('mode = "fitness" , result expected = 0.5')
    mode = 'fitness'
    x.inverse_fitness = 5
    x.abs_difference = 2
    denominator = 10
    x.set_normalized_fitness(mode, denominator)
    print(x)

    # Mode change test
    print('mode = "npv" , result expected = 0.2')
    mode = 'npv'
    x.set_normalized_fitness(mode, denominator)
    print(x)

    # Match test
    print('Count Matches test')
    ind  = Individual(0, 0, 1, 'none', [1,0,1])
    ind2 = Individual(0, 0, 1, 'none', [1,0,1])
    ind3 = Individual(0, 0, 1, 'none', [0,0,0])

    print ('Matches Expect 3: ' + str(ind.count_matches(ind2)))
    print ('Matches Expect 1: ' + str(ind.count_matches(ind3)))

    # Count Difference Test
    print('\nCount Difference test')
    print('Differences expected 0: ' + str(ind.count_differences(ind2)))
    print('Differences expected 2: ' + str(ind.count_differences(ind3)))

if __name__ == '__main__':
    main()
