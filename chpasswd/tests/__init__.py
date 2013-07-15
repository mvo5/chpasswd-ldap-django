import glob
import os

# auto import all test stuff
for f in glob.glob(os.path.join(os.path.dirname(__file__), "test_*.py")):
    name = os.path.splitext(os.path.basename(f))[0]
    exec("from .%s import *" % name)
