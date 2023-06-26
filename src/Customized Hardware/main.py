import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from Register import register
from Memory import memory

# class for simulation of hardwired RISC-V processor instructions
class hardwired:
    def __init__(self):
        pass

    
