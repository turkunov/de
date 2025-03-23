#!/usr/bin/env python3

import sys
import argparse

# read number of days for averaging
parser = argparse.ArgumentParser()
parser.add_argument("--numdays", type=str)
args = parser.parse_args()
num_days = int(args.numdays)

current_key = None
sum_count = 0
key_count = {}
for line in sys.stdin:
    try:
        key, count = line.strip().split('\t', 1)
        count = int(count)
    except ValueError as e:
        continue
    if current_key != key:
        if current_key:
            key_count[current_key] = sum_count
            print("{thread}\t{av}".format(thread=current_key,av=sum_count/num_days))
        sum_count = 0
        current_key = key
    sum_count += count

if current_key:
    print("{thread}\t{av}".format(thread=current_key,av=sum_count/num_days))
