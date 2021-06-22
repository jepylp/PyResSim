'''
Author:       James Porter

GA tests:
Generate a population
'''

import unittest
import ga
from individual import Individual

class GATest(unittest.TestCase):
    '''GA Test'''

    gen_alg = ga.Genetic_Algorithm(
        model= 'test_model',
        generations= 2,
        gene_size= 5,
        first_generation_size=10,
        pairings=5,
        mutation_rate=0.1,
        min_diff= 1,
        npv_discount_rate= 0.1
    )

    gen_alg.generate_population(gen_alg.first_generation_size, 0)

    def test_gen_pop(self):
        '''Test generator for population'''

        self.assertEqual(len(self.gen_alg.population), self.gen_alg.first_generation_size,
            'Not enough individuals generated'
        )

        self.assertEqual(len(self.gen_alg.population[0].genes), self.gen_alg.gene_size,
            'Gene size incorrect'
        )

    def test_selection(self):
        '''Test selection'''

        # make each normalized fitness 0.05 so that the total is 0.5

        for ind in self.gen_alg.population:
            ind.fitness = 5

        selected = self.gen_alg.selection()

        self.assertIn(selected, self.gen_alg.population, 'selection error')

        # Will have to check log for the random value that and selected case

    def test_pairing(self):
        '''Test Pairing'''

        ind1 = Individual(
            genes=[1,1,1,1,1],
            case=1,
            generation=1,
            parents='none'
        )

        ind2 = Individual(
            genes=[0,0,0,0,0],
            case=2,
            generation=1,
            parents='none'
        )

        parents = [ind1.genes, ind2.genes]

        possible_pairings = [[1,0,0,0,0],[1,1,0,0,0],[1,1,1,0,0],[1,1,1,1,0]]

        children = self.gen_alg.pairing(parents)

        self.assertEqual(len(children), 2, 'Number of children generate error')

        self.assertIn(children[0], possible_pairings, 'Pairing error')

    def test_mutation(self):
        '''Test Mutation'''
        genes = [1,1,1,1,1]
        starting_genes = [1,1,1,1,1]
        mutation_occured = False
        counter = 0

        print([1,1] == [1,1])

        # Run test 100 times to see if any genes are mutated
        while (counter < 100 and mutation_occured is False):
            counter = counter + 1

            if self.gen_alg.mutation(genes) != starting_genes:
                mutation_occured = True

        self.assertNotEqual(genes, starting_genes, 'Mutation error')

        print('Mutation attempts: %s' % counter)

    def test_next_gen(self):
        '''Test Next Generation'''

        ind1 = Individual(
            genes=[1,1,1,1,1],
            case=1,
            generation=2,
            parents='none'
        )

        ind2 = Individual(
            genes=[0,0,0,0,0],
            case=2,
            generation=2,
            parents='none'
        )

        ind3 = Individual(
            genes=[0,1,0,0,0],
            case=3,
            generation=2,
            parents='none'
        )

        ind4 = Individual(
            genes=[0,0,1,0,0],
            case=4,
            generation=2,
            parents='none'
        )

        ind5 = Individual(
            genes=[0,0,0,1,0],
            case=5,
            generation=2,
            parents='none'
        )

        sample_pop = [ind1, ind2, ind3, ind4, ind5]

        for ind in sample_pop:
            ind.fitness = 5

        self.gen_alg.population = sample_pop

        selected = self.gen_alg.selection()
