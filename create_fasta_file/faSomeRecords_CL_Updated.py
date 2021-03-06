#!/usr/bin/env python
"""
Author: santiagosnchez
Updated for current project by Claire LeBlanc
Last updated: 12/14/2021

Overview: Creates a fasta file containing sequences for desired genes. 
""" 

import argparse, textwrap
import sys
from re import match
import gzip
from random import choice

# parse arguments
parser = argparse.ArgumentParser(prog="FaSomeRecords.py",
    formatter_class=argparse.RawTextHelpFormatter,
    description="Retrieves some FASTA records provided a FASTA file and a list or records.",
    epilog=textwrap.dedent('''\
Records can be sepcified providing a list file with --list/-l
or one by one in the command line using --records/-r.

The elements in the list must be an exact match as those in the
master FASTA file, and may or may not include the ">" character at
the begining of the header.

Example of list file:
sequence1
sequence2
sequence3
...
sequenceN
'''))
parser.add_argument(
'--fasta', '-f', metavar='FASTA_FILE', type=str, required=True,
help='FASTA file where all the sequences are stored.')
parser.add_argument(
'--list', '-l', metavar='LIST', type=str,
help='file name of the list.')
parser.add_argument(
'--records', '-r', metavar='RECORD', nargs="*", type=str,
help='individual FASTA records.')
parser.add_argument(
'--outfile', '-o', default="records.fasta", nargs="?", type=str,
help='name for output file (default: %(default)s)')
parser.add_argument(
'--stdout', '-s', action="store_true", default=False,
help='if sequences should be printed to screen.')
parser.add_argument(
'--keep', '-k', action="store_true", default=False,
help="keep the order in the list.")
args = parser.parse_args()
if args.list == None and args.records == None:
    parser.print_usage()
    sys.exit("FaSomeRecords.py: error: argument --list/-l or --records/-r is required")
if args.list is not None:
    with open(args.list, "r") as l:
        heads = l.read().splitlines()
    if ">" not in heads[0]:
        heads = [ ">" + h for h in heads ]
    heads = [h for h in heads ]
elif args.records is not None:
    heads = args.records
    if ">" not in heads[0]:
        heads = [ ">" + h for h in heads ]
requested = len(heads)
joinheads = "# ".join(heads) + "#"
found = 0
not_found = []
if args.keep:
    store = {}
    with open(args.fasta, "r") as f:
        for line in f:
            if line[0] == ">":
                if (line[:-1] + "#") in joinheads:  
                    h = line[:-1]
                    seq = 1
                    store[h] = ''
                    found += 1
                elif (line[:-1] + "#") in joinheads: #ADDED PART
                    h = line[:-3]
                    seq = 1
                    store[h] = ''
                    found += 1
                else:
                    seq = 0
            else:
                if seq == 1:
                    store[h] += line
    if found == 0:
        print "No sequences found"
    else:
        if args.stdout:
            for h in heads:
                if store.get(h):
                    sys.stdout.write(h+"\n"+store[h])
                else:
                    sys.stdout.write(h+"\n"+"#not found\n")
                    not_found += [h]
        else:
            with open(args.outfile, "w") as o:
                for h in heads:
                    if store.get(h):
                        o.write(h+"\n"+store[h])
                    else:
                        sys.stdout.write(h+"\n"+"#not found\n")
                        not_found += [h]
            print "Found {} sequence(s)".format(found)
            if found > requested:
                print "Found {} sequence(s) more than requested".format(found-requested)
            elif requested > found:
                print "Could not find {} sequence(s)".format(requested-found)
                print "\n".join(not_found)
            print "Sequences saved to: "+args.outfile
else:    
    if args.stdout:
        with open(args.fasta, "r") as f:
            for line in f:
                if line[0] == ">":
                    if (line[:-1] + "#" or line[:-3] + "#") in joinheads: #ADDED PART
                        seq = 1
                        sys.stdout.write(line)
                        found += 1
                    else:
                        not_found += [line[:-1]] 
                        seq = 0
                else:
                    if seq == 1:
                        sys.stdout.write(line)
        if found == 0:
            print "No sequences found"
    else:
        with open(args.outfile, "w") as o:
            with open(args.fasta, "r") as f:
                for line in f:
                    if line[0] == ">":
                        if (line[:-1] + "#" or line[:-3] + "#") in joinheads: #ADDED PART
                            seq = 1
                            o.write(line)
                            found += 1
                        else:
                            not_found += [line[1:-1]]
                            seq = 0
                    else:
                        if seq == 1:
                            o.write(line)
        if found == 0:
            print "No sequences found"
        else:
            print "Found {} sequence(s)".format(found)
            if found > requested:
                print "Found {} sequence(s) more than requested".format(found-requested)
            elif requested > found:
                print "Could not find {} sequence(s)".format(requested-found)
                print "\n".join(not_found) #this prints out all genes from genome file not found, instead of all sequences from name file
            print "Sequences saved to "+args.outfile
