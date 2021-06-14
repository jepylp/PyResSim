'''
Author:       James Porter

Determine rms, npv, convert days to flowtime, and normalize fitness values
'''

import unittest
import calculator
from individual import Individual

class CalcTest(unittest.TestCase):
    '''Calculator Test'''

    historical_flowrates = [5050, 5050, 5050]
    individual_flowrates = [5000, 5000, 5000]
    individual_time = [
        0.084931506849315, 0.076712328767123, 0.084931506849315,
        0.082191780821918, 0.084931506849315, 0.082191780821918,
        0.084931506849315, 0.084931506849315, 0.082191780821918,
        0.084931506849315, 0.082191780821918, 0.084931506849315
    ]
    rate = 0.1
    monthly_days = [31,28,31,30,31,30,31,31,30,31,30,31]
    days_per_year = 365

    def test_rms(self):
        '''RMS test'''
        self.assertEqual(
            calculator.rms(self.historical_flowrates, self.individual_flowrates),
            50,
            'RMS error'
        )

    def test_npv(self):
        '''NPV test'''
        self.assertAlmostEqual(
            calculator.npv(self.individual_flowrates, self.individual_time, self.rate),
            34068.46,
            'NPV error'
        )

    def test_convert_days_to_flowtime(self):
        '''Convert days to flowtime'''
        # round becuase python is returning more digits than calc/excel
        for i in range(len(self.monthly_days)):
            self.assertEqual(
                round(calculator.convert_days_to_flowtime(
                    days= self.monthly_days[i],
                    days_per_year= self.days_per_year,
                    year= 0
                ), 15),
                self.individual_time[i],
                'Convert days to flowtime error'
            )

    def test_normalize_fitness(self):
        '''Normailze Fitness test'''

        pop = [Individual([1,0,1,0,1], 1, 0, 'none', 'none'),
        Individual([1,0,1,0,1], 2, 0, 'none', 'none'),
        Individual([1,0,1,0,1], 3, 0, 'none', 'none'),
        Individual([1,0,1,0,1], 4, 0, 'none', 'none'),
        Individual([1,0,1,0,1], 5, 0, 'none', 'none')]

        pop[0].fitness = 5
        pop[1].fitness = 10
        pop[2].fitness = 15
        pop[3].fitness = 20
        pop[4].fitness = 50

        calculator.normalize_fitness(pop)

        #for ind in pop:
        #    print(ind)

        self.assertEqual(pop[0].inverse_fitness, 20.0, 'Normalize fitness error')
