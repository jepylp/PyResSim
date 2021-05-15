'''
Author:       James Porter

Flowrate test, small class that holds the eom time in years
and the average flowrate for the period
'''

import unittest
import flowrate

class FlowrateTest(unittest.TestCase):
    '''Test the flowrate'''
    # Feb first year, 4000 flowrate
    time = 0.16164383561643836
    avg_flowrate = 4000
    test = flowrate.Flowrate(time, avg_flowrate)

    def test_time(self):
        '''Test time'''
        self.assertEqual(self.test.eom_time, self.time, 'Time difference')

    def test_flowrate(self):
        '''Test average flowrate'''
        self.assertEqual(self.test.avg_flowrate, self.avg_flowrate,
            'Average flowrate difference')

if __name__ == '__main__':
    unittest.main()
