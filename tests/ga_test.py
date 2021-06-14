'''
Author:       James Porter

GA tests:
Generate a population
'''

import unittest
import ga

class GATest(unittest.TestCase):
    '''GA Test'''

    gen_alg = ga.Genetic_Algorithm(
        model= 'test_model',
        generations= 2,
        gene_size= 25,
        first_generation_size=20,
        pairings=10,
        mutation_rate=0.1,
        min_diff= 2,
        npv_discount_rate= 0.1
    )

    def test_gen_pop(self):
        '''Test generator for population'''
        pop = self.gen_alg.generate_population(self.gen_alg.first_generation_size)

        print()
        for p in pop:
            print(p)

        self.assertEqual(len(pop), self.gen_alg.first_generation_size,
            'Not enough individuals generated'
        )

        self.assertEqual(len(pop[0]), self.gen_alg.gene_size,
            'Gene size incorrect'
        )

    def test_selection(self):
        '''Test selection in the GA'''

        pop = self.gen_alg.generate_population(self.gen_alg.first_generation_size)

        # make each normalized fitness 0.05 so that the total is 1.00

        for ind in pop:
            ind.normalized_fitness = 0.05

        selected = self.gen_alg.selection()
