'''
Author:       James Porter 3140786

Testing gene generation, currently only contains the int generator
'''
import unittest
import gene_generator

class GeneGeneratorTest(unittest.TestCase):
    '''Test the gen e generator, currently only generates int but can be
    expanded on later.'''
    gene_size = 100
    rock_types = 2

    test_genes = gene_generator.generate_genes_int(gene_size, rock_types)

    def test_size(self):
        '''Test that the size of the genes are correct'''
        self.assertEqual(len(self.test_genes), self.gene_size,
            'Returned wrong size')

    def test_content(self):
        '''Test that the genes are within the bounds set by rock type'''
        self.assertTrue(self.int_content_test(), 'Gene outside bounds')

    def int_content_test(self):
        '''helper fuction for checking the content, will return false
        if one of the genes is out side the range'''
        for gene in self.test_genes:
            if gene < 0:
                return False
            if gene > (self.rock_types - 1):
                return False

        return True

if __name__ == '__main__':
    unittest.main()
