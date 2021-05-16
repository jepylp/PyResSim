'''
Author:       James Porter 3140786
Supervisor:   Greg Walker, MA PhD (Cantab)

Individual for genetic algorithm.
To be used with pyResSim.

'''

from pathlib import Path        # Converts file/folder path to which ever os
from dataclasses import dataclass

@dataclass
class Individual:
    '''
    Holds the information required to build cases, sort cases, and build the
    next generation
    '''
    genes: int                      # genes that make up this individual
    case: int                       # case id in generation (used as folder name)
    generation: int                 # Geneation this individual belongs to
    parents: str = 'none'           # Array to store the parents
    case_file_path: Path = Path('./')   # file path for case
    flowrates: float = 0            # store the flowrates from flow
    fitness: float = 0              # Fitness value determines the likelyhood of
                                    # selection
    inverse_fitness: float = 0      # 1 / Fitness
    normalized_fitness: float = 0   # used to determine which parents for
                                    # the next generation. can use fitness,
                                    # or NPV
    run: bool = True                # Should this case be run
    npv: float = 0                  # NPV from case run in flow
    abs_difference: float = 0       # Distance value is away from average
                                    # The further away the more likely to
                                    # be selected for the next generation
    mode: str = 'rms'               # Mode for fitness


    def count_matches(self, individual):
        '''
        Compare genes between self and provided genes and return the number of
        matching genes (same gene, in the same position)
        '''

        matches = 0

        for x in range(len(individual.genes)):
            if individual.genes[x] == self.genes[x]:
                matches = matches + 1

        return matches

    def count_differences(self, individual):
        '''
        Compare genes between self and provided genes and return the number of
        different genes (same gene, in the same position)
        '''

        differences = 0

        for x in range(len(individual.genes)):
            if individual.genes[x] != self.genes[x]:
                differences = differences + 1

        return differences
