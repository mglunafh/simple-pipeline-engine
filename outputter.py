#!/usr/bin/env python

import argparse
import re
import sys

PATTERN = re.compile("[0-9]+[e|o]")
OUT = "OUT"
ERR = "ERR"
TEMPLATE = "{channel}: Line number #{n}"


def validate(value):
    result = PATTERN.match(value)
    if not result:
        raise RuntimeError(f"Could not parse option '{value}'")
    return result


def get_number_and_output(value):
    n = int(value[:-1])
    channel = OUT if value[-1] == 'o' else ERR
    return n, channel


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Script which outputs a given number of lines into either "
                                     "stdout or stderr.")
    parser.add_argument("lines", nargs='+',
                        help="Commands of form [N]e / [N]o, where N is a number.")
    parser.add_argument("-o", "--outfile", required=False, help="Redirect stdout to this file.")
    parser.add_argument("-e", "--errfile", required=False, help="Redirect stderr to this file.")

    args = parser.parse_args()
    for option in args.lines:
        validate(option)

    out_channel = open(args.outfile, 'w') if args.outfile else sys.stdout
    err_channel = open(args.errfile, 'w') if args.errfile else sys.stderr

    try:
        counter = 1
        for option in args.lines:
            n, direction = get_number_and_output(option)
            channel = out_channel if direction == OUT else err_channel
            for i in range(n):
                message = TEMPLATE.format(channel=direction, n=counter + i)
                print(message, file=channel)
            counter += n
    finally:
        if args.outfile:
            out_channel.close()
        if args.errfile:
            err_channel.close()
