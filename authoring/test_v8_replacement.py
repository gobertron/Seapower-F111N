#!/usr/bin/env python3
"""Compatibility entry point for the renamed Version 9.0 replacement tests."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from authoring.test_v9_replacement import *
if __name__=='__main__':
    unittest.main(verbosity=2)
