#!/usr/bin/env python

import argparse
from pipeline import SimplePipeline

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run a simple pipeline")
    parser.add_argument("data_folder", help="Data folder where to start processing")
    parser.add_argument("-v", "--verbose", action='store_true', help="Add a verbosity")
    args = parser.parse_args()
    pl = SimplePipeline(args.data_folder)
    pl.run_simple_pipeline(verbose=args.verbose)
