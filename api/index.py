import sys
import os

# Append root directory to sys.path to resolve module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
