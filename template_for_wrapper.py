#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: <data>
#@author: <name>
#@contact: <email>

import sys
import argparse


def main(settings):
    ''' Function description.
    '''
    pass


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Program description.')
    parser.add_argument('-i','--input', help='Input file', required=True)
    parser.add_argument('-o','--output', help='Ouput file', required=True)
    parser.add_argument('-c','--cutoff', help='Cutoff value', required=False, default=100)
    args = vars(parser.parse_args())
    
    input_file = args["input"]
    output_file = args["output"]
    cutoff = int(args["cutoff"])


    settings = {
        "input_file": input_file,
        "output_file": output_file,
        "cutoff": cutoff,
    }

    main(settings)