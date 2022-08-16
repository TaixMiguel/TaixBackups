#!/usr/bin/python3

import getopt
import requests
import sys

if __name__ == '__main__':
    long_options = ["id_backup="]
    argumentList = sys.argv[1:]
    id_backup: str = None
    options = "i:"

    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)

        for currentArgument, currentValue in arguments:
            if currentArgument in ("-i", "--id_backup"):
                id_backup = currentValue
    except getopt.error as err:
        print(str(err))

    if id_backup:
        url: str = "http://127.0.0.1:5000/execBackup/" + id_backup
        requests.get(url)
