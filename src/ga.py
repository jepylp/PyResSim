'''
Author:     James Porter
Supervisor:   Greg Walker, MA PhD (Cantab)
Genetic Algorithm for use with OPM-project simulator
Can be set to keep previous generations and allow for them to be used for
reproduction. This should help keep the algorithm diverse.

generates and returns the a set of genes

Adapted from:
https://towardsdatascience.com/a-simple-genetic-algorithm-from-scratch-in-python-4e8c66ac3121
'''

import random
import datetime
import logging
from pathlib import Path
import numpy as np
import writer
from reader import Reader
from ecl.summary import EclSum
from individual import Individual
import gene_generator
import calculator

class Genetic_Algorithm:

    def __init__(self,
        model,
        generations,
        gene_size,
        first_generation_size,
        pairings,
        mutation_rate,
        min_diff,
        npv_discount_rate,
        log_file = 'log.txt',
        csv_file = 'output.csv',
        csv_generations = 'generations.csv',
        rock_types_path:Path = Path('./templates/rock_types.csv')
        ):

        self.model = model
        self.generation = generations
        self.gene_size = gene_size
        self.first_generation_size = first_generation_size
        self.pairings = pairings
        self.mutation_rate = mutation_rate
        self.min_diff = min_diff
        self.npv_discount_rate = npv_discount_rate
        self.log_file = log_file
        self.csv_file = csv_file
        self.csv_generations = csv_generations
        self.rock_types_path = rock_types_path

        # initialize log file
        log_format='%(asctime)s - %(levelname)s - %(message)s'
        log_file_path = Path(self.model + '/' + self.log_file)   # Change to save in model folder
        logging.basicConfig(
            filename=log_file_path,
            level=logging.DEBUG,
            format=log_format,
            datefmt='%Y/%m/%d %I:%M:%S %p'
        )

        logging.info('Logging started')

        logging.debug('model: %s' % self.model)
        logging.debug('generation: %s' % self.generation)
        logging.debug('gene size: %s' % self.gene_size)
        logging.debug('first gen size: %s' % self.first_generation_size)
        logging.debug('parings: %s' % self.pairings)
        logging.debug('mutation rate: %s' % self.mutation_rate)
        logging.debug('min diff: %s' % self.min_diff)
        logging.debug('npv discount rate: %s' % self.npv_discount_rate)
        logging.debug('log file: %s' % self.log_file)
        logging.debug('csv file: %s' % self.csv_file)
        logging.debug('csv generations: %s' % self.csv_generations)
        logging.debug('rock types path: %s' % self.rock_types_path)

        # Create the reader object
        reader = Reader()

        # Get the rock types
        self.rock_types = reader.rock_types(rock_types_path)
        logging.debug('%s' % self.rock_types)

        # initialize the generations
        # 0 should be standard cases and/or cases a user wants to include
        self.generation_counter = 0

        # Initialize the population list
        self.population = []

    def generate_population(self, pop_size, generation):
        '''
        Generate the specified number of individuals with the required number of genes
        '''

        logging.info('Generating Random Population, Pop size: %s' % pop_size)

        for case_number in range(self.first_generation_size):
            self.population.append(
                Individual(
                    genes=gene_generator.generate_genes_int(self.gene_size, self.rock_types),
                    case=case_number,
                    generation=generation,
                    parents='none'
                )
            )


    def selection(self):
        '''
        Returns a random parent from the provided population
        Uses the entire population
        '''

        value = random.random()
        logging.debug('Random value for slection: %s' % value)

        for ind in self.population:

            if value < ind.cnf:
                logging.info('Selected - Gen: %s Case: %s' % (ind.generation, ind.case))
                return ind

    
    def pairing(self, parents_genes):
        '''
        return two children from the two parents
        '''
        offspring_genes = []  # Initialize

        # pivot point can't be in position 0 or the last position
        pivot_point = random.randint(1,len(parents_genes[0]) - 2)

        logging.debug('Pivot: %s' % pivot_point)

        offspring_genes.append(parents_genes[0][0:pivot_point] + parents_genes[1][pivot_point:])
        offspring_genes.append(parents_genes[1][0:pivot_point] + parents_genes[0][pivot_point:])

        logging.info('Offspring: %s' % offspring_genes)

        return offspring_genes

    def mutation(self, genes):
        '''
        return gene set with a single gene modified
        '''
        if random.random() < self.mutation_rate:

            # Select gene from position 1 to second last
            mutated_gene = random.randint(1, len(genes) - 2)
            logging.info('Mutating: %s' % mutated_gene)

            # Choose a random selection from the rock types until a
            # different one is found
            mutation = genes[mutated_gene]
            runs = 0
            while mutation == genes[mutated_gene]:
                runs = runs + 1
                mutation = random.randint(0, len(self.rock_types) - 1)

            genes[mutated_gene] = mutation

            logging.debug('Mutation runs: %s Returning: %s', runs, genes)
        return genes

    def next_gen(self, mode):
        '''
        Generate and return the next generation
        mode is set to either fitness, npv, or npv_extremes
        '''

        # set fitness based on mode
        if mode == 'rms':
            calculator.rms_normalize_fitness(self.population)
        elif mode == 'npv':
            calculator.npv_normalize_fitness(self.population)

        # increment generation counter
        self.generation_counter = self.generation_counter + 1

        # starting case number for this generation
        case = 0

        # Generations will generate the same number of individuals each
        # generation rounded down. Two pairs per set of parents.
        for i in range(0, self.pairings):
            parents = [] # initialize blank parent list for pairing

            # Select the parents
            parents.append(self.selection())
            parents.append(self.selection())

            # Make sure parents are different, try up to 50 times
            runs = 0
            while (parents[0] == parents[1] and runs < 50):
                runs = runs + 1
                logging.debug('matching, find another')
                del parents[-1]
                parents.append(self.selection())

            logging.info('Parent selction runs: %s Parents: %s', runs, parents)

            parents_genes = [parents[0].genes, parents[1].genes]

            # append the parents information to the child
            parents_text = ('gen' + str(parents[0].generation) + 'case'
                + str(parents[0].case)    # First parent
                + ' gen' + str(parents[1].generation) + 'case'
                + str(parents[1].case))  # Second parent

            # Get the children
            children = self.pairing(parents_genes)
            logging.info('Children: %s', children)

            # Mutate children and create Individual
            logging.debug('----children----')
            for child_genes in children:

                child_genes = self.mutation(child_genes)
                ind = Individual(
                    genes=child_genes,
                    case=case,
                    generation=self.generation_counter,
                    parents=parents_text
                )
                self.population.append(ind)
                case = case + 1 # Increase case number for child
                logging.debug(str(ind))

            logging.debug('--end children--')
