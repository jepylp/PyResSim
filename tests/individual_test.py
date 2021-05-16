'''
Author:       James Porter

Flowrate test, small class that holds the eom time in years
and the average flowrate for the period
'''

import unittest
from pathlib import Path
import individual

class IndividualTest(unittest.TestCase):
    '''Test the individual'''
    # create individual 1
    ind1 = individual.Individual(
        case= 1,
        case_file_path= Path('./ind_test/test1.DATA'),
        generation= 0,
        parents= 'none',
        genes= [1,0,1,0,1]
    )

    print(ind1)

    # create individual 2
    ind2 = individual.Individual(
        genes= [0,0,1,0,1],
        case= 2,
        case_file_path= Path('./ind_test/test2.DATA'),
        generation= 0,
        parents= 'none'
    )

    print(ind2)

    # Comparison tests

    def test_count_matches(self):
        '''Test Count Matches'''
        self.assertEqual(self.ind1.count_matches(self.ind2), 4, 'Count match error')

    def test_count_deff(self):
        '''Test Count Diff'''
        self.assertEqual(self.ind1.count_differences(self.ind2), 1, 'Count diff error')

if __name__ == '__main__':
    unittest.main()
