# Python GA for Uncertainty Analysis

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
Python 3

## USE
Template folder hold the files that build the case files. 
	top.include holds the eclipse file above the permeability and porosity
	bottom.include hold the eclipse file information below the permeability and porosity
	time.include stores the time information in the same way as the eclipse file
	rock_types.csv is the permeability and porosity of the rock types that can be selected during a simulation run
	standard_cases contains cases that should be included as generation zero
