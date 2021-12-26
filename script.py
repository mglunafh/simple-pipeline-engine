#!/usr/bin/env python

import argparse
from pipeline import SimplePipeline

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run a simple pipeline")
    parser.add_argument("data_folder", help="Data folder where to start processing")
    args = parser.parse_args()
    pl = SimplePipeline(args.data_folder)
    pl.run_simple_pipeline()
