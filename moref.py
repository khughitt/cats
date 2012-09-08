#!/bin/env python
"""
moref:  more for FASTA files
"""
import sys
import os
from Bio import SeqIO

def main():
    """moref main"""
    # Check for input file
    if len(sys.argv) < 2:
        print("No input file specified")
        sys.exit()

    filepath = os.path.expanduser(sys.argv[1])
    
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
    
    # bold text
    regular = '\033[0;090m'
    bold = '\033[1;090m'    
    
    # loop through and print seqs
    for seq in seqs:
        print(bold + seq.description)
        
        pretty = regular
        for letter in seq.seq:
            pretty += dna[letter]
            
        print(pretty + "\n")

if __name__ == "__main__":
    main()
