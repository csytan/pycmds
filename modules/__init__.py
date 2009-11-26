import os
import sys

# Load all modules in directory
path = os.path.dirname(__file__)
for file in os.listdir(path):
    if not file.startswith('__init__') and file.endswith('.py'):
        modname = file.rsplit('.py')[0]
        __import__(__name__ + '.' + modname)
