#!/bin/env python
"""
moref:  more for FASTA files
"""
import sys
import os
from argparse import ArgumentParser
from Bio import SeqIO

def get_args():
    """Parses input and returns arguments"""
    parser = ArgumentParser(description='Pretty-print sequence data')
    parser.add_argument('--start-codons', dest='start_codons',
                        action='store_true',
                        help='Highlight any start codons in DNA/RNA output')
    parser.add_argument('--stop-codons', dest='stop_codons',
                        action='store_true',
                        help='Highlight any stop codons in DNA/RNA output')
    parser.add_argument('file', help='File containing sequence data.')
    args = parser.parse_args()
    return args

def main():
    """moref main"""
    # Check for input file
    args = get_args()
    if not 'file' in args:
        print("No input file specified")
        sys.exit()
    filepath = os.path.expanduser(args.file)
    
    if not os.path.isfile(filepath):
        print("No input file specified")
        sys.exit()
        
    # Read in FASTA file
    seqs = SeqIO.parse(filepath, 'fasta')
    
    # Generate list of colors to use for printing, ex:
    # regular    - \033[032m
    # emphasized - \033[1;032m
    # bright     - \033[092m
    colors = ['\033[0%dm' % i for i in range(91, 95)]
    
    # DNA
    dna = dict((x, colors[i] + x) for i, x in enumerate(('A', 'C', 'G', 'T')))
    
    # Use custom colors if specified
    config_file = os.path.expanduser("~/.morefrc")
    if os.path.isfile(config_file):
        # read config file
        import ConfigParser
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        #config.readfp(open(config_file, 'r+'))
        
        # override color choices
        for k,v in config.items('dna'):
            dna[k.upper()] = "\033%s%s" % (v, k.upper())

    # start/stop codons
    stop_codons = [
        dna['T'] + dna['A'] + dna['G'],
        dna['T'] + dna['A'] + dna['A'],
        dna['T'] + dna['G'] + dna['A']
    ]
            
    # for x in range(1,10):
    # print "\033[03%dmTEST   \033[09%dmTEST" % (x,x)

    # bold text
    regular = '\033[0;090m'
    bold = '\033[1;090m'    
    
    # loop through and print seqs
    # @NOTE - could pause here after each record if desired
    for seq in seqs:
        print(bold + seq.description)
        
        pretty = regular
        for letter in seq.seq:
            pretty += dna[letter]
            
        # check for stop codons if requested
        if 'stop_codon' in args and args.stop_codon:
            for codon in stop_codons:
                pretty.replace(codon, '\033[0;041mSTOP') 
            
        print(pretty + "\n")

if __name__ == "__main__":
    main()
