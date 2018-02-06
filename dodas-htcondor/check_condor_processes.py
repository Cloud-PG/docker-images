#!/usr/bin/env python
import psutil
from sys import argv, exit

def check_condor_processes(process_list):
    counter = 0
    for process in psutil.process_iter(attrs=["name", "exe", "cmdline"]):
        if process.info['name'] in process_list:
            counter += 1
    return counter == len(process_list)

if __name__ == "__main__":
    if check_condor_processes(argv[1:]):
        exit(0)
    else:
        exit(1)