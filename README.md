# Python GA for Uncertainty Analysis

## UPDATE
Update currently in progress to move this to python 3 and refactor the code for better readability.

## CONTENT
PyResSim uses a modified genetic algorithm with objective functions for uncertainty analysis. 

Using the open source reservoir simulator from opm-project.org, and ecl (https://github.com/equinor/ecl) the program will generate individuals and run them through the simulator to try and find some history matches. Then the program will explore the economic viability of the well for both best and worst case scenarios.

## LICENSE
GNU General Public License, version 3 or later (GPLv3+).

## PLATFORMS
The opm-simulators module is Designed to run on Linux platforms. So, this program has been built and test on Linux

## REQUIREMENTS
Opm-simulator (opm-porject.org or opm-project.org/?page_id=245)
ecl (https://github.com/equinor/ecl)
Python 2

## USE
Template folder hold the files that build the case files. 
	top.include holds the eclipse file above the permeability and porosity
	bottom.include hold the eclipse file information below the permeability and porosity
	time.include stores the time information in the same way as the eclipse file
	rock_types.csv is the permeability and porosity of the rock types that can be selected during a simulation run
	standard_cases contains cases that should be included as generation zero
	
Example run "python pyResGen.py -m test1 -g 3 -p 4 -r 0.05 -t 5 -d 2 -n 0.1"

3 generations per objective function (3 for to find history match, 3 to find NPV extremes)
4 pairings per generation
5% chance for mutation
5 top individuals tracked
2 genes must be different to be included in the top individual list
10% discount rate used for NPV
