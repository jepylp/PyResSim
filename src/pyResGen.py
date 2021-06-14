'''
Author:       James Porter
Supervisor:   Greg Walker, MA PhD (Cantab)
This is the main part of the program that will accespt user input through the
console commands.
'''
import argparse
import sys
import os
import csv
from reader import Reader
import genetic_algorithm



def main():
    parser = argparse.ArgumentParser(
        description='Generate models with a Genetic Algorithm')

    # Gene Size not included because that would require extensive adjustments
    # to how the cases are generated. Currently the grid is spliced into 25
    # cells that span 12 meters each. The grid must be split into whole numbers
    gene_size = 25

    parser.add_argument('-m', '--model', dest='model',
        help='str: name of the model, used as top level directory',
        metavar='FOLDER', nargs=1, type=str)
    parser.add_argument('-g', '--generations', dest='generations',
        help='int: generations per run type, ie: 4 for fitness, then 4 for NPV',
        nargs=1, type=int)
    parser.add_argument('-f', '--first_generation_size',
        dest='first_generation_size',
        help='int: number of individuals to randomly generate in the first generation',
        nargs=1, type=int)
    parser.add_argument('-p', '--pairs', dest='pairings',
        help='int: Number of pairings for each generation, 2 children are generated'
        + 'per pairing', nargs=1, type=int)
    parser.add_argument('-r', '--mutation_rate', dest='mutation_rate',
        help='float: Chance that a gene will have a mutation', nargs=1, type=float)
    parser.add_argument('-n', '--npv_discount_rate',
        dest='npv_discount_rate',
        help='float: Discount rate to use for the NPV calculation',
        nargs=1, type=float)
    parser.add_argument('-md', '--min_diff',
        dest='min_diff',
        help='int: minimum number of genes that must be different',
        nargs=1, type=int)
    parser.add_argument('-c', '--children',
        dest='children',
        help='int: Amount of children per parent pairings ',
        nargs=1, type=int)
    parser.add_argument('-s', '--set_case',
        dest='gen0',
        help='provide a folder with cases to use as gen 0',
        nargs=1, type=str)
    parser.add_argument('-top', '--top_file',
        dest='top',
        help='path to file that has the case file information above PORO and PERM',
        nargs=1, type=str)
    parser.add_argument('-b', '--bottom_file',
        dest='bottom',
        help='path to file that has the case file information below PORO and PERM',
        nargs=1, type=str)
    parser.add_argument('-t', '--time_steps',
        dest='time_steps',
        help='path to time steps file ',
        nargs=1, type=str)
    parser.add_argument('-rt', '--rock_types',
        dest='rocks',
        help='path to rock type file ',
        nargs=1, type=str)




    args = parser.parse_args()
    print (args)

    '''
    python3 pyResGen.py -m test1 -g 3 -f 4 -p 4 -r 0.05 -n 0.1 -c 2 -md 2 -top './include/top.include' -b './include/bottom.include' -t './include/time.include' -s './include/standard_cases' -rt './include/rock_types.csv'

    Output:
    Namespace(top=['./include/top.include'], bottom=['./include/bottom.include'], children=[2], 
    first_generation_size=[4], gen0=['./include/standard_cases'], generations=[3], min_diff=[2], 
    model=['test1'], mutation_rate=[0.05], npv_discount_rate=[0.1], pairings=[4], 
    rocks=['./include/rock_types.csv'], time_steps=['./include/time.include']
    '''

    print('Model: '             + str(args.model[0]))
    print('Generations: '       + str(args.generations[0]))
    print('First gen size: '    + str(args.first_generation_size[0]))
    print('Number of pairs: '   + str(args.pairings[0]))
    print('Mutation rate: '     + str(args.mutation_rate[0]))
    print('minimum diff:'       + str(args.min_diff[0]))
    print('NPV discount rate: ' + str(args.npv_discount_rate[0]))
    print('Children: '          + str(args.children[0]))
    print('Top File: '          + str(args.top[0]))
    print('Bottom File: '       + str(args.bottom[0]))
    print('Time File: '         + str(args.time_steps[0]))
    print('Generation 0: '      + str(args.gen0[0]))

    
    file_reader = Reader()

    rock_types = file_reader.rock_types()

    

    ga = genetic_algorithm.Genetic_Algorithm(
        rock_types,
        gene_size,
        args.children[0],
        args.model[0],
        args.generations[0],
        args.first_generation_size[0],
        args.pairings[0],
        args.mutation_rate[0],
        args.min_diff[0],
        args.npv_discount_rate[0],
    )

    '''
    ga.run()

    for generation in ga.generations:
            print(generation.print_generation())

    print('Model Complete')
    '''

    


if __name__ == '__main__':
    main()