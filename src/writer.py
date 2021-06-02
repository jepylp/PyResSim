'''
Author:       James Porter
Supervisor:   Greg Walker, MA PhD (Cantab)

Helper object to write files for pyResSim
'''

import os
from pathlib import Path
import individual

def write_case(
    indi: individual,
    generation: int,
    rock_types,
    folder_path: str,
    top_file: str,
    bottom_file: str,
    time_file: str,
    cell_width = '12*'
):

    '''
    Write the case file used by FLOW
    '''

    # Initialize the poro and perm strings
    perm_string = ''         # Set perm string to blank
    poro_string = ''         # Set poro string to blank

    for gene in indi.genes:
        for rock in rock_types:
            if str(gene) == rock[0]:
                # Currently set to 12 as 25 cell must now fill 300
                # Needs to be changed to a calculated value, change SPE1
                # grid, or change the number of cells we are generating
                perm_string = perm_string + (cell_width + rock[2] + ' ')
                poro_string = poro_string + (cell_width + rock[3] + ' ')
                break   # Once the permeability and porosity are found we
                            # exit the loop

    # Create Path to Generation folder, Case folder, and Case file
    generation_path = str(folder_path) + '/GEN' + '%02d' % generation + '/'
    #print('Generation path: ' + generation_path)

    case = 'CASE' + '%03d' % indi.case
    case_path = generation_path + case + '/'
    #print('Case path: ' + case_path)

    case_file = case_path + case + '.DATA'
    individual.case_file_path = Path(case_file)
    #print('Case file: ' + case_file)

    # Create folder
    if not os.path.exists(case_path):
        os.makedirs(case_path)

    # add end of the line slashes to .DATA file
    perm_string = perm_string + ('/')
    poro_string = poro_string + ('/')

    # Generate Eclipse file from template
    with open(case_file, 'w+') as f:

    # Write the Porosity and Permiabilty to the file
        with open(Path(top_file), 'r') as r:
            f.write(r.read())
            r.close()
        f.write('PORO\n')						    #PORO
        f.write(poro_string)
        f.write('\n\nPERMX\n')						#PERMX
        f.write(perm_string)
        f.write('\n\nPERMY\n')						#PERMY
        f.write(perm_string)
        f.write('\n\nPERMZ\n')						#PERMZ
        f.write(perm_string)
        f.write('\n')

        # Write the last part of the file from the bottom template
        with open(bottom_file, 'r') as r:
            f.write(r.read())
            r.close()

        with open(time_file, 'r') as r:
            f.write(r.read())
            r.close()

        # End the file
        f.write('\n\nEND')

        f.close()

    return individual
