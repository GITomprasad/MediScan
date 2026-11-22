"""
MediScan AI - Root Entry for Seeding Demo Data
"""
import os
import sys

# Ensure backend directory is in python path
backend_dir = os.path.join(os.path.dirname(__file__), "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from seed_demo_data import seed

if __name__ == "__main__":
    seed()
