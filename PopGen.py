'''
Author:       James Porter 3140786
Supervisor:   Greg Walker, MA PhD (Cantab)

This was generated for testing to produce a random population for testing the
exclusion zone

Generated a random population for the use in the PyResGen.
The random int that is generated is only 0 or 1, this can be expanded upon if
required in the future. It could be as simple as reading in from the template
file the number of entries there are, and passing that in, or hard coding it
like I have here.
'''

import os
import random

class popgen:

    def __init__(self):

        self.folder_path = './testingPop/'
        self.case = 0

    # Generate the genes
    def generate(self):
        genes = []
        for i in range(25):
            genes.append(random.randint(0,1))   # <- Change this value to the
                                                # number of rock types
        return genes

    def write_to_file(self, case, genes):

        case_file = self.folder_path + str(case) + '.CASE'

        f = open(case_file, 'w+')

        cell = 1

        for gene in genes:
            if cell % 5 == 0:
                f.write(str(gene) + '\n')
            else:
                f.write(str(gene) + ',')
            cell = cell + 1

        #f.write(str(genes))

        f.close()

def main():
    gen = popgen()

    for i in range(200):    # <- Change this value to the number of individuals
                            # you want to generate

        genes = gen.generate()

        while (genes[0] == 0 and genes[-1] == 1):
            print('new one!')
            genes = gen.generate()

        gen.write_to_file(i, genes)
        print genes

if __name__ == '__main__':
    main()
