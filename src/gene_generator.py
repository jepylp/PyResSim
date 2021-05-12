'''
Author:       James Porter 3140786
Supervisor:   Greg Walker, MA PhD (Cantab)

Gene generator for genetic algorithm
Currently only the integer generator is implemented
'''

import random

# Generate genes given the gene size and the number of rock types to
# choose from. 
def generate_genes_int(gene_size:int, rock_types: int):

    # use temp to allow for overwriting of the genes
    genes = []
    
    # use _ for unsude integer in for loop
    for _ in range(gene_size):
        genes.append(random.randint(0, rock_types - 1))
        
    return genes