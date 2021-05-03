'''
Author:       James Porter 3140786
Supervisor:   Greg Walker, MA PhD (Cantab)
This is the main part of the program that will accespt user input through the
console commands.
'''

import GeneticAlgorthim
import argparse
import pandas as pd
import os

def main():
    parser = argparse.ArgumentParser(
        description='Generate models with a Genetic Algorithm')

    # Gene Size not included because that would require extensive adjustments
    # to how the cases are generated. Currently the grid is spliced into 25
    # cells that span 12 meters each. The grid must be split into whole numbers

    parser.add_argument('-m', '--model', dest='model',
        help='str: name of the model, used as top level directory',
        metavar='FOLDER', nargs=1, type=str)
    parser.add_argument('-g', '--generations', dest='generations',
        help='int: generations per run type, ie: 4 for fitness, then 4 for NPV',
        nargs=1, type=int)
    parser.add_argument('-f', '--first_generation_size',
        dest='first_generation_size',
        help='int: number of individuals to randomly generate in the first '
        + 'generation',
        nargs=1, type=int)
    parser.add_argument('-p', '--pairs', dest='pairings',
        help='int: Number of pairings for each generation, 2 children are generated'
        + 'per pairing', nargs=1, type=int)
    parser.add_argument('-r', '--mutation_rate', dest='mutation_rate',
        help='float: Chance that a gene will have a mutation', nargs=1, type=float)
    parser.add_argument('-t', '--top_individuals_amount',
        dest='top_individuals_amount',
        help='int: How many individuals to use in for top fitness, ie: top 10 ',
        nargs=1, type=int)
    parser.add_argument('-d', '--top_individuals_min_differences',
        dest='top_individuals_min_diff',
        help='int: How many genes must be different between individuals for the'
        + ' top individuals list', nargs=1, type=int)
    parser.add_argument('-n', '--npv_discount_rate',
        dest='npv_discount_rate',
        help='float: Discount rate to use for the NPV calculation',
        nargs=1, type=float)
    parser.add_argument('-md', '--min_diff',
        dest='min_diff',
        help='int: minimum number of genes that must be different',
        nargs=1, type=int)




    args = parser.parse_args()
    print (args)

    '''
    python pyResGen.py -m test1 -g 3 -p 4 -r 0.05 -t 5 -d 2 -n 0.1

    Output:
    Namespace(generations=[3], model=['test1'], mutation_rate=[0.05],
    npv_discount_rate=[0.1], pairings=[4], top_individuals_amount=[5],
    top_individuals_min_diff=[2])
    '''

    print('Model: '             + str(args.model[0]))
    print('Generations: '       + str(args.generations[0]))
    print('First gen size: ')   + str(args.first_generation_size[0])
    print('Number of pairs: '   + str(args.pairings[0]))
    print('Mutation rate: '     + str(args.mutation_rate[0]))
    print('minimum diff:'       + str(args.min_diff))
    print('Top '                + str(args.top_individuals_amount[0]))
    print('Min diff for top: '  + str(args.top_individuals_min_diff[0]))
    print('NPV discount rate: ' + str(args.npv_discount_rate[0]))

    ga = GeneticAlgorthim.Genetic_Algorithm(
        args.model[0],
        args.generations[0],
        args.first_generation_size[0],
        args.pairings[0],
        args.mutation_rate[0],
        args.min_diff[0],
        args.top_individuals_amount[0],
        args.top_individuals_min_diff[0],
        args.npv_discount_rate[0],
    )

    ga.run()

    for generation in ga.generations:
            print(generation.print_generation())

    print(ga.top_individuals)
    print('Model Complete')


if __name__ == '__main__':
    main()
