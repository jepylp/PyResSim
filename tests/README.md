#For testing on ubuntu 
This ensures that the import paths work without having to set a path
Otherwise the file would require:

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

For the imports to work correctly from the source files and pylint throws a warning message that it can't find the import.

so:

#Clone the repo
git clone -b v2 https://github.com/jepylp/PyResSim.git

#Install 
pip3 install --editable .


