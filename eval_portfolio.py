#!/usr/bin/env python

import argparse
import csv


def calculate_value(stocks_file, quotes_file):
    with open(stocks_file) as f_stock:
        lines = csv.reader(f_stock, delimiter='\t')
        stocks = {line[0]: int(line[1]) for line in lines}

    with open(quotes_file) as f_quote:
        lines = csv.reader(f_quote, delimiter='\t')
        quotes = {line[0]: float(line[1]) for line in lines}

    acc = 0
    for stock in stocks:
        amount = stocks[stock]
        if stock not in quotes:
            raise RuntimeError(f"Stock '{stock}' not found among the list of available quotes.")
        price = quotes[stock]
        acc += amount * price
    return acc


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the value of  your portfolio.')
    parser.add_argument("-s", "--stocks", required=True, help="File with amount of stock entries")
    parser.add_argument("-q", "--quotes", required=True, help="File with stock quotes")

    args = parser.parse_args()
    val = calculate_value(args.stocks, args.quotes)
    print(val)
