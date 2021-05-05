'''
Author:       James Porter 3140786

Testing geen generation, currently only contains the int generator
'''
## import the os and sys to set the file path for importing main files
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import gene_generator

# size test
def size_test(genes, size):
    if len(genes) == size:
        return True
    else:
        print('content fail')
        return False

# test that the content is within the range it should be for int generator
def int_content_test(genes, rock_types):
    for gene in genes:
        if gene < 0:
            print('content fail')
            return False
        if gene > (rock_types - 1):
            return False

    return True

def main():
    gene_size = 100
    rock_types = 2
    genes = gene_generator.generate_genes_int(gene_size, rock_types)

    result_size = size_test(genes, gene_size)
    result_content = int_content_test(genes, rock_types)

    print('Size test: ' + str(result_size))
    print('Content test: ' + str(result_content))

    if (result_size == True and result_content == True) :
        print('Gene Generator Tests: Passed')
    else:
        print('Gene Generator Tests: Failed')

if __name__ == '__main__':
    main()