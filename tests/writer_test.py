'''
Author:       James Porter

Tests the writer class that is responsible for the writing case files and
creating tht efiles showing all the case statistics.
'''

import unittest
from pathlib import Path
import writer
import individual
import reader

class WriterTest(unittest.TestCase):
    ''' Writer test '''

    def test_write_case(self):
        ''' Test writing a case file '''

        ind = individual.Individual(
            genes= [1,0,1,1,0],
            case= 0,
            generation= 0,
            parents= 'none',
        )

        r = reader.Reader()
        rock_types = r.rock_types()

        writer.write_case(
            indi= ind,
            generation= 0,
            rock_types= rock_types,
            folder_path= Path('./tests/write_test_output/'),
            top_file= Path('./templates/top.include'),
            bottom_file= Path('./templates/bottom.include'),
            time_file= Path('./templates/time.include')
        )

        test_case_file_path = Path('./tests/write_test_output/GEN00/CASE000/CASE000.DATA')
        match_case_file_path = Path('./tests/write_test_output/matchme.DATA')


        with open(test_case_file_path, 'r') as test_case:
            with open(match_case_file_path, 'r') as match_case:

                self.assertEqual(test_case.read(), match_case.read(), 'case file content error')

            match_case.close()
        test_case.close()

if __name__ == '__main__':
    unittest.main()
