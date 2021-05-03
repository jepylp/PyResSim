'''
Author:       James Porter 3140786
Supervisor:   Greg Walker, MA PhD (Cantab)

Compare individuals and return the number of genes that are different
'''

import Individual

class Individual_Diff:

    def __init__(self, mode = 'ind'):
        self.mode = mode

    def __repr__(self):
        s = mode
        return s

    # Accepts 2 individuals and returns the number of different genes
    def count_diff(self, x, y):

        if len(x.genes) != len(y.genes):
            return(-1)  # Error message: genes different size
        else:
            diff = 0   # Tracks the number of matches
            for i in range(len(x.genes)):

                # If they are equal
                if int(x.genes[i]) != int(y.genes[i]):
                    diff = diff + 1

            return diff


    # Accepts 2 individuals and returns the number of matching genes
    def count_matches(self, x, y):

        if len(x.genes) != len(y.genes):
            return(-1)  # Error message: genes different size
        else:
            matches = 0   # Tracks the number of matches
            for i in range(len(x.genes)):

                # If they are equal
                if int(x.genes[i]) == int(y.genes[i]):
                    matches = matches + 1

            return matches


def main():

    # Setup the individuals that match
    match1 = Individual.Individual(10, 0, 0, 'none', [1,1,1,1,1,0,0,0,0,0])
    match2 = Individual.Individual(10, 1, 0, 'none', [1,1,1,1,1,0,0,0,0,0])

    # Setup the individuals that are different
    diff1 = Individual.Individual(10, 2, 0, 'none', [1,1,1,1,1,0,0,0,0,0])
    diff2 = Individual.Individual(10, 2, 0, 'none', [1,1,1,1,1,1,1,0,0,0])

    # Change the differences
    id = Individual_Diff()
    print('count_diff: All genes match test, 0 expected: '
        + str(id.count_diff(match1, match2)))
    print('count_diff: 2 genes different test, 2 expected: '
        + str(id.count_diff(diff1, diff2)))

    # Count the matches
    print('count_matches: All genes match test, 10 expected: '
        + str(id.count_matches(match1, match2)))
    print('count_matches: 2 genes different test, 8 expected: '
        + str(id.count_matches(diff1, diff2)))

if __name__ == '__main__':
    main()
