import sys
import os

# Add root directory to sys.path so tests can import app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
