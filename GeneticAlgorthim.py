'''
Author:       James Porter 3140786
Supervisor:   Greg Walker, MA PhD (Cantab)
Genetic Algorithm for use with OPM-project simulator
Can be set to keep previous generations and allow for them to be used for
reproduction. This should help keep the algorithm diverse.
'''

import sys, os, random, csv
from ecl.summary import EclSum
import numpy as np
import Individual
import Generation
import TopIndividuals
import datetime

class Genetic_Algorithm:

    def __init__(self, model, generations, first_generation_size, pairings,
        mutation_rate, min_diff, top_individuals_amount, top_individuals_min_diff,
        npv_discount_rate, log_file = 'log.txt', csv_file = 'output.csv',
        csv_generations = 'generations.csv', csv_top = 'top.csv',
        gene_size = 25):

        # Initialize all variables
        self.generations = []    # Stores the entire population

        self.rocks = []         # Rock types from CSV file

        self.history = []       # History the algorithm will try to match to

        self.model = model      # Name of the model, used to name the folder

        self.total_inverse_fitness = 0  # Track the total inverse fitness to
                                        # pass to individuals to calculate the
                                        # normalized fitness values

        self.pairings = pairings        # Total amount of children for each
                                        # generation, should always be an even
                                        # number, as each pair will produce 2
                                        # children

        self.mutation_rate = mutation_rate  # Chance of mutation for the child

        self.min_diff = min_diff    # Minimum number of gene that must be
                                    # different from already run cases

        self.generations_per_trail = generations    # Number of generations to
                                                    # run per objective
                                                    # function change

        self.npv_discount_rate = npv_discount_rate  # Discount rate for NPV

        # Number of random individuals to generate in the first generation
        self.first_generation_size = first_generation_size

        self.gene_size = gene_size      # number of genes used for each case
                                        # currently set to 25 due to
                                        # constraints with generated case
                                        # files, please see documentation
                                        # for a more detailed explination

        self.average_npv = 0            # Average NPV of all cases

        self.total_abs_difference = 0   # Total of all abs differences

        # Stores the top individuals, updates at the end of each generation
        self.top_individuals = TopIndividuals.TopIndividuals(
            top_individuals_amount, top_individuals_min_diff)

        # Output files for logs and csv file
        # Pandas can output directly to excel file if required
        self.log_file_path = (self.model + '/' + log_file)
        self.log_file = ''

        self.csv_file_path = (self.model + '/' + csv_file)
        self.csv_file = ''

        self.csv_generations_path = (self.model + '/' + csv_generations)
        self.csv_generations = ''

        self.csv_top_path = (self.model + '/' + csv_top)
        self.csv_top = ''

        # Create folder if required
        if not os.path.exists(self.model):
            os.makedirs(self.model)

        # Delete the output if the already exist
        if os.path.isfile(self.log_file_path):
            os.remove(self.log_file_path)

        # Create log file
        self.log_file = open(self.log_file_path, 'w+')
        self.log_file.write('Start Time: ' + str(datetime.datetime.now())
            + '\n')

        # Fill the rocks array
        self.rock_types()

        # Fill history
        self.history_FOPR()

        # Get standard cases
        self.standard_cases()

        # Write standard cases to log file
        self.log_file.write(str(self.generations[0]))

    # Generate a random population, of given size
    # pop_size - size of the population to generator
    # gene_size - number of genes for each individual
    def generate_population(self, pop_size, gene_size):
        self.log_file.write('\nGenerating Random Population, Pop size: '
            + str(pop_size) + ' Gene Size: ' + str(gene_size))
        self.generations.append(Generation.Generation('random',
            len(self.generations), pop_size, gene_size))

    # Import the rock types csv
    # default path ./include/rockType.csv
    def rock_types(self, path='./include/rockType.csv'):
        self.log_file.write('\nImporting rocks')

        with open(path) as csvDataFile:
            csvReader = csv.reader(csvDataFile)
            for row in csvReader:
                self.log_file.write('\n' + str(row))
                self.rocks.append(row)


    # Print imported rocks
    # Used for testing and making sure that the rocks are importing properly
    def print_rock_types(self):
        for x in self.rocks:
            print(str(x))

    # Standard cases to run for every model
    # returns a population from the standard cases
    # TODO: generate the RMS difference for these cases also
    def standard_cases(self, case_path='./include/cases/'):

        # zero generation
        x = Generation.Generation('standard', 0, 0, 0) # Create empty population
        case = 0;

        for file in os.listdir(case_path):

            # open the standard case files as read only
            with open(os.path.join(case_path,file), 'r') as csvDataFile:
                csvReader = csv.reader(csvDataFile)
                filename = (file + '.DATA')
                genes = [] # initialize the genes

                # For each cell in the csv file create a gene
                for row in csvReader:
                    for cell in row:
                        genes.append(int(cell))

                # Create the Individual, assigning a case number and size
                x.add_individual(Individual.Individual(len(genes), case, 0,
                    'standard', genes))

                # Increment to next case
                case = case + 1

        print('Printing x')
        print (str(x))
        self.generations.append(x)
        print(str(x.individuals[0].genes))

    # Open the history file for the rate of production for the well
    # and return an array with the values from the csv file
    def history_FOPR(self, history_CSV_Path = './history/HISTORY.csv'):

        # Open csv and read it into the history array
        with open(history_CSV_Path) as csvDataFile:
            csvReader = csv.reader(csvDataFile)
            for row in csvReader:
                for entry in row:

                    # convert the value to a float and append to array
                    try:
                        self.history.append(float(entry))
                    except Exception as e:
                        print(
                            "Could not convert '{}' to "
                            "a float...skipping.".format(entry)
                        )
                        print ("Stopping, please check history file")
                        sys.exit();

    # Calculate the root mean diference between the individual and the history
    # individual is run through EclSum to get the FOPR
    # history is an array that is passed into the fuction for comparison
    def fitness_calculation(self, case_path):

        # The upper size of the array will be dictated by the history match
        upper = len(self.history)

        # Import the individual and shorten it to the number of history values
        # using a numpy array
        individual_summary = EclSum(case_path)
        individual_FOPR = individual_summary.numpy_vector("FOPR")
        individual_FOPR = individual_FOPR[0:upper]
        print ("history:    " + str(self.history))
        print ("individual: " + str(individual_FOPR))

        return np.sqrt(((self.history - individual_FOPR) ** 2).mean())


    def npv_from_flow (self, case_path):
        npv = 0                                 # Initialize npv
        summary = EclSum(case_path)             # Open the summary file in ECL
        fopr = summary.numpy_vector("FOPR")     # Get the FOPR values
        time = summary.numpy_vector("YEARS")    # Get the Years values
        last_time = 0

        self.log_file.write('\nfopr: ' + str(fopr) + '\n')
        self.log_file.write('\ntime: ' + str(time) + '\n')

        # npv = future value / (1 + rate) ^ time
        # sum up all net present values for the total npv of the well
        for i in range(0, len(fopr)):

            npv = npv + (fopr[i] / (1 + self.npv_discount_rate) ** time[i])

        return npv


    # Returns a random parent from the provided population
    # selection mode: Using all the generation or not
    def selection(self):

        # Value to determine which Individual to select from normalized
        # probability
        value = random.random()
        print(value)


        gen = -1 # set generation
        running_normalized_fitness = 0

        for generation in self.generations:
            gen = gen + 1
            for individual in generation.individuals:

                # Running total of the normailized fitness, full total
                # should be 1.0 but there are some rounding issues
                running_normalized_fitness = (running_normalized_fitness +
                    individual.normalized_fitness)

                # Print the running total of the normalized fitness
                print(str(individual.case) + ': ' +
                    str(running_normalized_fitness))

                # if the value is less than the running total then use
                # the current individual
                if value < running_normalized_fitness:
                    print ('selected - gen: ' + str(gen) + ' ' +
                        str(individual))
                    return [individual, gen]


    # Single random point within the genes for pairing
    # Produces two children with initialize fitness
    # Returns a set of two children
    def pairing(self, parents):
        offspring = [] # initialize offspring array

        # pivot point can not be the first cell or the last
        pivotPoint = random.randint(1,len(parents[0]) - 2)
        print('pivot:' + str(pivotPoint))


        offspring.append(parents[0][0:pivotPoint] + parents[1][pivotPoint:])
        offspring.append(parents[1][0:pivotPoint] + parents[0][pivotPoint:])

        return offspring

    # Mutate a random sample of genes, default is 10%, flips one gene of an
    # individual chosen at random, the first and last gene will be untouched
    # returns an individual
    def mutation(self, genes):
        if ((random.random()) < self.mutation_rate):

            # Select gene from position 1 to second last
            mutated_gene = random.randint(1, len(genes) - 2)
            print('mutating' + str(mutated_gene))

            # If gene is 0 change to 1, else change to 0
            if genes[mutated_gene] == 0:
                genes[mutated_gene] = 1
            else:
                genes[mutated_gene] = 0
        return genes


    # Generate and return the next generation
    # mode is set to either fitness, npv, or npv_extremes
    def next_gen(self, mode):

        case = 0   # case number to assign to individual

        # create an empty generation for the children
        generation = Generation.Generation(mode, len(self.generations), 0, 25)

        # Generations will generate the same number of individuals each
        #  generation rounded down. Two pairs per set of parents.
        for i in range(0, self.pairings):
            parents = [] # initialize blank parent list for pairing

            # Select the parents
            parents.append(self.selection())
            parents.append(self.selection())

            # Make sure parents are different
            runs = 0
            while (parents[0] == parents[1] and runs < 50):
                runs = runs + 1
                print('matching, find another')
                del parents[-1]
                parents.append(self.selection())

            print('runs: ' + str(runs) + ' ' + str(parents))

            parents_genes = [parents[0][0].genes, parents[1][0].genes]

            # append the parents information to the child
            parents_text = ('gen' + str(parents[0][1]) + 'case'
                + str(parents[0][0].case)    # First parent
                + ' gen' + str(parents[1][1]) + 'case'
                + str(parents[1][0].case))  # Second parent

            # Get the children
            children = self.pairing(parents_genes)
            print ('children: ' + str(children))

            # Mutate children and create Individual

            for row in children:

                row = self.mutation(row)
                ind = Individual.Individual(25, case, len(self.generations),
                    parents_text, row)
                generation.add_individual(ind)
                case = case + 1 # Increase case number for child

            print('----children----')
            print(generation.print_generation())
            print('--end children--')

        self.generations.append(generation)

    # Print a given generation
    def print_generation(self, generation):

        # Print the generation
        print('  Generation: ' + str(generation))

        if generation > len(self.generations):
            print('Generation out of range, number of generations: ' +
                len(self.generations))
        else:

            # print generation
            print(self.generations[generation].print_generation())


    # Generate all cases for generation
    def generate_all_files_for_generation(self, generation):

        folder_path = './' + self.model + '/'

        for ind in self.generations[generation].individuals:
            self.case_generator(ind, folder_path, generation)

    # Check to make sure that there are enough genes to warrent running the
    # case through flow
    def individual_too_close(self, individual):
        max_gen = individual.generation
        max_case = individual.case
        print ('max gen: ' + str(max_gen) + ' max case: ' + str(max_case))

        # If it's part of the first generation, then only run that generation
        if individual.generation == 0:
            gen = self.generations[0]
            for x in range(max_case):
                indi = gen.individuals[x]
                differences = indi.count_differences(individual)
                if differences <= self.min_diff:
                    individual.run_me = False
                    print('Match ' + str(indi.generation)
                        + ',' + str(indi.case))
                    return True

        # if this is later in a run we have to run all generations
        else:

            # Check 0 generation (for loop will miss it with first gen)
            gen = self.generations[0]
            for x in range(len(gen.individuals)):
                indi = gen.individuals[x]
                differences = indi.count_differences(individual)
                if differences <= self.min_diff:
                    individual.run_me = False
                    print('Match ' + str(indi.generation)
                        + ',' + str(indi.case))
                    return True


            # Check the generations below the current individual we are checking
            for gen in range(max_gen): # exclusive of max_gen
                print ('gen = ' + str(gen) + ' max_gen = ' + str(max_gen))
                for indi in self.generations[gen].individuals:

                    # Count the differences
                    differences = indi.count_differences(individual)
                    if differences <= self.min_diff:
                        individual.run_me = False
                        print('Match ' + str(indi.generation)
                            + ',' + str(indi.case))
                        return True

            # Check the current generation up to the current individual
            if individual.run_me == False:
                gen = self.generations[max_gen]
                for x in range(max_case):
                    indi = gen.individuals[x]
                    differences = indi.count_differences(individual)
                    if differences <= self.min_diff:
                        individual.run_me = False
                        print('Match ' + str(indi.generation)
                            + ',' + str(indi.case))
                        return True

        # No matches found
        individual.run_me = True
        print ('No Match, please run')
        return False


    # Generate the cases to work with the OPM simulator flow
    # Uses the eclipse simulator data file, so a template of that has been built
    # and only the porosity and permeability are being adjusted through the
    # genetic algorithm to try and find a match.
    def case_generator(self, individual, folder_path, generation,
                        topFileTemplateLoc='./include/top.include',
                        bottomFileTemplateLoc='./include/bottom.include'):
        cellWidth = '12*'
        permString = ''         # Set perm string to blank
        poroString = ''         # Set poro string to blank
        self.rock_types()
        for gene in individual.genes:
            for rock in self.rocks:
                if str(gene) == rock[0]:
                    # Currently set to 12 as 25 cell must now fill 300
                    # Needs to be changed to a calculated value, change SPE1
                    # grid, or change the number of cells we are generating
                    permString = permString + (cellWidth + rock[2] + ' ')
                    poroString = poroString + (cellWidth + rock[3] + ' ')
                    break   # Once the permeability and porosity are found we
                                # exit the loop

        # Add a / to folder path if missing
        # Add a / to gen_path if it's missing

        if folder_path[-1] != '/':
            folder_path = folder_path + '/'

        # Create Path to Generation folder, Case folder, and Case file
        generation_folder = folder_path + 'gen' + str(generation)  + '/'
        #print('Generation Folder: ' + generation_folder)

        #Set case, for use with folder and file
        case = 'CASE' + '%03d' % individual.case

        case_folder = generation_folder + case + '/'
        #print('Case Folder: ' + case_folder)

        case_file = case_folder + case + '.DATA'
        #print('Case file: ' + case_file)

        # Create folder
        if not os.path.exists(case_folder):
            os.makedirs(case_folder)

        # add end of the line slashes to .DATA file
        permString = permString + ('/')
        poroString = poroString + ('/')

        # Generate Eclipse file from template
        topFileTemplate = open(topFileTemplateLoc)
        bottomFileTemplate = open(bottomFileTemplateLoc)
        f = open(case_file, 'w+')

        # Write the Porosity and Permiabilty to the file
        f.write(topFileTemplate.read())
        f.write('PORO\n')						#PORO
        f.write(poroString)
        f.write('\n\nPERMX\n')						#PERMX
        f.write(permString)
        f.write('\n\nPERMY\n')						#PERMY
        f.write(permString)
        f.write('\n\nPERMZ\n')						#PERMZ
        f.write(permString)
        f.write('\n')

        # Write the last part of the file from the bottom template
        f.write(bottomFileTemplate.read())

        topFileTemplate.close()
        bottomFileTemplate.close()
        f.close()


        # Files is now created, ready to run in flow

        # Check if the genes look like a slow run and if the individual is too
        # close, if so then assign a high fitness and skip the run
        if ((individual.genes[0] == 0 and
            individual.genes[len(individual.genes) - 1] == 1)
            or
            self.individual_too_close(individual)): #too close, so skip

            # Set fitness very high for first geen 0, and last a 1, so that it
            # shouldn't be chosen to reproduce
            individual.fitness = 999999999.99
            individual.normalized_fitness = 1 / individual.fitness

        else:

            # Run Flow, provides directory and file to store the case
            # CASE must be capitalized for flow to run otherwise it throws
            # an error, history file is provided to fitnessCalculation
            os.system('flow ' + case_file)
            individual.fitness = self.fitness_calculation(case_file)
            individual.inverse_fitness = 1 / individual.fitness
            self.total_inverse_fitness = (self.total_inverse_fitness +
                individual.inverse_fitness)
            individual.npv = self.npv_from_flow(case_file)

            # Update top individuals list
            self.top_individuals.add_individual(individual)


    # Set the normalized fitness using:
    # either fitness or npv
    # over
    # total inverse fitness or total absolute difference
    def set_normalized_fitness(self, mode):

        # if mode is NPV then total abs_difference and pass that as denominator
        if mode == 'npv':
            total_abs_difference = 0

            for generation in self.generations:
                for individual in generation.individuals:
                    total_abs_difference = (total_abs_difference
                        + individual.abs_difference)

        for generation in self.generations:
            for individual in generation.individuals:
                if mode == 'fitness':
                    individual.set_normalized_fitness('fitness',
                        self.total_inverse_fitness)
                if mode == 'npv':
                    individual.set_normalized_fitness('npv',
                        total_abs_difference)

    # Update each individuals abs difference (npv) from the top individuals
    # average npv
    def update_abs_difference(self):
        # Update the abs_difference for each case that is not 0
        # abs difference = abs (npv - average npv)
        self.log_file.write('\n' + 'UPDATING abs_difference' + '\n'
            + 'Top ' + str(self.top_individuals.max_entries) + ' average npv: '
            + str(self.top_individuals.average_npv))
        for generation in self.generations:
            for individual in generation.individuals:
                if individual.npv != 0:
                    individual.abs_difference = abs(individual.npv -
                        self.top_individuals.average_npv)
                    self.log_file.write('\n'
                        + 'gen: ' + str(individual.generation)
                        + ' case: ' + str(individual.case)
                        + ' npv: ' + str(individual.npv)
                        + ' abs_difference: ' + str(individual.abs_difference))

                else:
                    self.log_file.write('\nSkip '
                        + 'gen: ' + str(individual.generation)
                        + ' case: ' + str(individual.case)
                        + ' npv: ' + str(individual.npv))


    # gene_size is hard coded for the grid size we are using.
    # grid 300 cells, so the output file will use 12 for length, width,
    # and height of the cell, so it has to be 25 genes
    def run(self):

        # Standard generation is 0, first generation is random and will be
        # assigned generation 1

        print(datetime.datetime.now())

        # mode should be fitness to start
        mode = 'fitness'
        # Generate random first generation
        self.generate_population(self.first_generation_size, self.gene_size)

        for gen in range(len(self.generations)):
            # Generate files for the standard generation
            self.generate_all_files_for_generation(gen)

        self.set_normalized_fitness(mode)

        # Update geneations csv file with standard generation
        self.csv_generations = open(self.csv_generations_path, 'w+')
        self.csv_generations.write(self.generations[0].pandas_table().to_csv(index = False))

        # Log Random generation
        self.log_file.write(str(self.generations[-1]))
        self.log_file.write('Top ' + str(self.top_individuals.max_entries)
            + '\n' + str(self.top_individuals) + '\n')

        # Update Generations csv file with random generation
        self.csv_generations.write(self.generations[-1].pandas_table().to_csv(header = False, index = False))

        # Update Top csv file with top Individuals
        self.csv_top = open(self.csv_top_path, 'w+')
        self.csv_top.write(self.top_individuals.pandas_table().to_csv())


        # Generate the next generation using fitness
        for i in range(self.generations_per_trail):

            self.next_gen(mode)
            self.generate_all_files_for_generation(len(self.generations)-1)
            self.set_normalized_fitness(mode)

            # Log Fitness generation
            self.log_file.write('\n' + str(self.generations[-1]))
            self.log_file.write('Top ' + str(self.top_individuals.max_entries)
                + '\n' + str(self.top_individuals) + '\n')

            # Update Generations csv file with fitness generation
            self.csv_generations.write(self.generations[-1].pandas_table().to_csv(header = False, index = False))

            # Update Top csv file with top Individuals
            self.csv_top.write('Top ' + str(self.top_individuals.max_entries)
                + ' Generation: ' + str(len(self.generations) - 1) + '\n' )
            self.csv_top.write(self.top_individuals.pandas_table().to_csv())


        # Change mode to npv
        mode = 'npv'

        #update the average npv
        self.top_individuals.update_average_npv()
        self.update_abs_difference()
        self.set_normalized_fitness(mode)

        for i in range(self.generations_per_trail):



            # Generate next generation
            self.next_gen(mode)
            self.generate_all_files_for_generation(len(self.generations)-1)

            #update the average npv
            self.top_individuals.update_average_npv()
            self.update_abs_difference()
            self.set_normalized_fitness(mode)

            # Log NPV generation
            self.log_file.write('\n' + str(self.generations[-1]))
            self.log_file.write('Top ' + str(self.top_individuals.max_entries)
                + '\n' + str(self.top_individuals) + '\n')

            # Update Generations csv file with npv generation
            self.csv_generations.write(self.generations[-1].pandas_table().to_csv(header = False, index = False))

            # Update Top csv file with top Individuals
            self.csv_top.write('Top ' + str(self.top_individuals.max_entries)
                + ' Generation: ' + str(len(self.generations) - 1) + '\n' )
            self.csv_top.write(self.top_individuals.pandas_table().to_csv())

        self.csv_generations.close()
        self.csv_top.close()

        # Write out the end time to the log file
        self.log_file.write('\nEnd Time: ' + str(datetime.datetime.now()))
        self.log_file.close()

def main():
    ## Genetic Algorithm Test ##
    print ('Genetic Algorithm Test')
    gen = Genetic_Algorithm('test', 2, 10, 4, 0.1, 2, 5, 2, 0.1)

    # Rock Types
    print('Rock Types:')
    gen.print_rock_types()

    # Standard Cases
    print('Standard Cases:')
    print(gen.generations[0].print_generation())

    # Distance Check
    print('Distance Check:')
    individual = Individual.Individual(25, 200, 0, 'none',
        [1,1,1,0,0,1,1,1,0,0,0,1,1,0,0,1,0,0,0,1,1,0,0,1,0])
    gen.generations[0].add_individual(individual)
    print(individual)
    print('Should be a match\n')
    print(gen.individual_too_close(individual))
    print('-----------')

    individual = Individual.Individual(25, 201, 0, 'none',
        [1,0,1,0,0,1,0,1,1,1,1,0,1,1,0,0,0,1,0,1,0,1,1,0,0])
    gen.generations[0].add_individual(individual)
    print(individual)
    print('Should be a match\n')
    print(gen.individual_too_close(individual))
    print('-----------')

    individual = Individual.Individual(25, 202, 0, 'none',
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
    gen.generations[0].add_individual(individual)
    print(individual)
    print('Should NOT be a match and return no match, please run \n')
    print(gen.individual_too_close(individual))
    print('-----------')

        #Star new generation
    print("\nStarting new generation\n")
    gen.generations.append(Generation.Generation('Sample', 1))
    print('Distance Check:')
    individual = Individual.Individual(25, 0, 1, 'none',
        [1,1,1,0,0,1,1,1,0,0,0,1,1,0,0,1,0,0,0,1,1,0,0,1,0])
    gen.generations[1].add_individual(individual)
    print(individual)
    print('Should be a match\n')
    print(gen.individual_too_close(individual))
    print('-----------')

    individual = Individual.Individual(25, 1, 1, 'none',
        [1,0,1,0,0,1,0,1,1,1,1,0,1,1,0,0,0,1,0,1,0,1,1,0,0])
    gen.generations[1].add_individual(individual)
    print(individual)
    print('Should be a match\n')
    print(gen.individual_too_close(individual))
    print('-----------')

    individual = Individual.Individual(25, 2, 1, 'none',
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
    gen.generations[1].add_individual(individual)
    print(individual)
    print('Should be a match\n')
    print(gen.individual_too_close(individual))
    print('-----------')

    print("\nStarting new generation\n")
    gen.generations.append(Generation.Generation('Sample', 2))

    print('Distance Check:')
    individual = Individual.Individual(25, 0, 2, 'none',
        [1,1,1,0,0,1,1,1,0,0,0,1,1,0,0,1,0,0,0,1,1,0,0,1,0])
    gen.generations[2].add_individual(individual)
    print(individual)
    print('Should be a match\n')
    print(gen.individual_too_close(individual))
    print('-----------')

    individual = Individual.Individual(25, 1, 2, 'none',
        [1,0,1,0,0,1,0,1,1,1,1,0,1,1,0,0,0,1,0,1,0,1,1,0,0])
    gen.generations[2].add_individual(individual)
    print(individual)
    print('Should be a match\n')
    print(gen.individual_too_close(individual))
    print('-----------')

    individual = Individual.Individual(25, 2, 2, 'none',
        [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0])
    gen.generations[2].add_individual(individual)
    print(individual)
    print('Should NOT be a match\n')
    print(gen.individual_too_close(individual))
    print('-----------')

    individual = Individual.Individual(25, 3, 2, 'none',
        [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0])
    gen.generations[2].add_individual(individual)
    print(individual)
    print('Should be a match 2,2\n')
    print(gen.individual_too_close(individual))
    print('-----------')

    print("\nStarting new generation\n")
    gen.generations.append(Generation.Generation('Sample', 3))

    individual = Individual.Individual(25, 0, 3, 'none',
        [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0])
    gen.generations[3].add_individual(individual)
    print(individual)
    print('Should be a match 2,2\n')
    print(gen.individual_too_close(individual))
    print('-----------')

    # History
    print('Test History:')
    gen.history_FOPR()
    print(str(gen.history) + '\n')

    histCheck = [4389.62841797, 4270.94140625, 4129.33349609, 4010.40283203,
                3922.61474609, 3871.13232422, 3846.37353516, 3839.87426758,
                3847.41113281, 3866.38476562, 3894.0144043, 3927.07666016,
                3966.56542969, 4008.54785156, 4055.13818359, 4103.53955078,
                4148.28320312, 4198.49316406, 4247.14599609, 4297.05126953,
                4344.50488281, 4392.58789062, 4439.01708984, 4482.9921875,
                4527.32861328, 4568.70996094, 4609.9765625, 4649.78417969,
                4684.59375, 4721.76806641, 4756.5234375, 4791.11914062,
                4823.4140625, 4855.58251953, 4886.71679688, 4915.82128906,
                4944.55273438, 4971.76611328, 4998.64599609, 5024.92285156,
                5047.84521484]

    mismatch = 0    # Number of mismatch

    for i in range(len(histCheck)):

        if histCheck[i] != gen.history[i]:
            print('history line ' + str(i) + ': does not match')
            mismatch = mismatch + 1

    if mismatch > 0:
        print('history check is incorrect on ' + str(mismatch) + ' lines')
    else:
        print('all values match')

    #raw_input('Press Enter to continue run test...')

    # Run Testing
    # model, generations, first_generation_size, pairings,
    #   mutation_rate, min_diff, top_individuals_amount, top_individuals_min_diff,
    #   npv_discount_rate

    # Uncomment this section if you want to do a run
    # I would suggest using the console though:
    # time python pyResGen.py -m test -g 4 -f 100 -p 20 -r 0.1 -t 10 -d 2 -n 0.1 -md 2


    run_test = Genetic_Algorithm('test', 2, 10, 4, 0.1, 2, 5, 2, 0.1)
    print(run_test.generations[0].print_generation())
    run_test.run()

    for generation in run_test.generations:
            print(generation.print_generation())

    print(run_test.top_individuals)


if __name__ == '__main__':
    main()
