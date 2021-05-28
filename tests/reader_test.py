'''
Author:       James Porter

reader test to ensure that it can reader files for configuration and flow

load_time_steps is rounding due to a small rounding error only effects
the 16th decimal place
'''

import unittest
from pathlib import Path
from reader import Reader

class ReaderTest(unittest.TestCase):
    ''' Reader test '''
    r = Reader()
    time_steps = []

    def test_rock_types(self):
        ''' Test rock types '''

        self.assertEqual(
            len(self.r.rock_types(path= Path('./templates/rock_types.csv'))),
            2,
            'Error with rock types'
        )

    def test_load_cases_from_tempalte(self):
        ''' load standard cases '''

        population = self.r.load_cases_from_template(
            generation= 0,
            cases_path= Path('./templates/standard_cases/')
        )

        for ind in population:
            print (ind)

        self.assertEqual(
            len(population),
            8,
            'standard cases error'
        )

    def test_load_time_steps(self):
        ''' load time steps '''

        self.time_steps = self.r.load_time_steps(Path('./templates/time.include'))
        days = [31,59,90,120,151,181,212,243,273,304,334,365,
                396,424,455,485,516,546,577,608,638,669,699,730,
                761,789,820,850,881,911,942,973,1003,1034,1064,1095,
                1126,1154,1185,1215,1246,1276,1307,1338,1368,1399,1429,1460,
                1491,1519,1550,1580,1611,1641,1672,1703,1733,1764,1794,1825,
                1856,1884,1915,1945,1976,2006,2037,2068,2098,2129,2159,2190,
                2221,2249,2280,2310,2341,2371,2402,2433,2463,2494,2524,2555,
                2586,2614,2645,2675,2706,2736,2767,2798,2828,2859,2889,2920,
                2951,2979,3010,3040,3071,3101,3132,3163,3193,3224,3254,3285,
                3316,3344,3375,3405,3436,3466,3497,3528,3558,3589,3619,3650]
        year = 365

        for i in range(len(self.time_steps)):
            self.assertEqual(
                round(self.time_steps[i] * year),
                days[i],
                'time steps error'
            )

    def test_load_case_from_flow(self):
        ''' load single case '''

        self.time_steps = self.r.load_time_steps(Path('./templates/time.include'))

        case = self.r.load_case_from_flow(
            case_path= Path('./tests/test_flow_case/CASE000.DATA'),
            time_steps= self.time_steps
        )

        self.assertEqual(
            len(case),
            120,
            'failed to load cases'
        )

    def test_load_history(self):
        ''' load history '''

        self.time_steps = self.r.load_time_steps(Path('./templates/time.include'))

        history = self.r.load_history(time_steps= self.time_steps,
            path= Path('./tests/history/HISTORY.csv')
        )
        print (history)
        print ('history time steps: ' + str(len(history)))

if __name__ == '__main__':
    unittest.main()
