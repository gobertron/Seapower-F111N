#!/usr/bin/env python3
"""Compatibility entrypoint for the current Version 9.0 release preview."""
import argparse
from preview_v9 import contact_sheet,main

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--contact-only',action='store_true')
    if parser.parse_args().contact_only:contact_sheet()
    else:main()
