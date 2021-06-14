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

    def generate_population(self, pop_size):
        '''
        Generate the specified number of individuals with the required number of genes
        '''

        logging.info('Generating Random Population, Pop size: %s' % pop_size)

        generation = []
        for x in range(self.first_generation_size):
            generation.append(gene_generator.generate_genes_int(self.gene_size, self.rock_types))

        return generation

    def selection(self):
        '''
        Returns a random parent from the provided population
        Uses the entire population
        '''

        value = random.random()
        logging.debug('Random value for slection: %s' % value)

        running_normalized_fitness = 0

        for generation in self.population:
            for ind in generation:

                # Running total of the normailized fitness, full total
                # should be 1.0 but there are some rounding issues
                running_normalized_fitness = (running_normalized_fitness +
                    ind.normalized_fitness)

                # Print the running total of the normalized fitness
                logging.debug('Gen: %s Case: %s Running_normalized_fitness: %s'
                    % (ind.generation, ind.case, running_normalized_fitness)
                )

                # if the value is less than the running total then use
                # the current individual
                if value < running_normalized_fitness:
                    logging.info('Selected - Gen: %s Case: %s'
                        % (ind.gen, ind.case)
                    )
                    return (ind)
