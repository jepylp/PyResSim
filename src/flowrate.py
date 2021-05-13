'''
Author:       James Porter
Supervisor:   Greg Walker, MA PhD (Cantab)

Data structure objects to store information

Flowrate - stores the eom time values and average flowrates for those periods
'''

from dataclasses import dataclass

@dataclass
class Flowrate:
    '''stores the time values and flowrates for those time values'''
    eom_time: float                 # time from flow simulation
    avg_flowrate: float             # average flowrate from flow
