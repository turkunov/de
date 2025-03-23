#!/usr/bin/env python3

import sys
import re

pattern = re.compile(r'\[([^]]+)\]')

for line in sys.stdin:
    log_line = line.strip()
    matches = re.findall(pattern, line)
    if len(matches) > 1:
        if 'thread' in matches[1].lower():
            try:
                thread_type = matches[1]
                if " - " in thread_type:
                    dash_position = thread_type.find(" - ")
                    thread_name = thread_type[: dash_position + 3]
                else:
                    parts = thread_type.split()
                    if parts:
                        thread_name = parts[0]
                    else:
                        continue
                print("{fname}\t{num}".format(fname = thread_name, num = 1))
            except:
                continue