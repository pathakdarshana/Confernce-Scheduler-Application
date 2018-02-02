import sys
import os
cwd = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.abspath(os.path.join(cwd,".."))
sys.path.insert(0,parentDir)