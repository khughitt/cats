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
    stop_template = '\033[0;041m\033[1;038m%s\033[0m'
    
    stop_codons = {
        "TAG": stop_template % "TAG",
        "TAA": stop_template % "TAA",
        "TGA": stop_template % "TGA"
    }
            
    # for x in range(1,10):
    # print "\033[03%dmTEST   \033[09%dmTEST" % (x,x)

    # bold text
    reset = '\033[0m'
    bold = '\033[1m'    
    
    # loop through and print seqs
    # @NOTE - could pause here after each record if desired
    for seq in seqs:
        print(bold + seq.description)
        
        # highlight stop codons?
        highlight_stop_codons = 'stop_codons' in args and args.stop_codons
        
        # For DNA, read bases three at a time
        # For now, assume reading frame starts from index 0
        pretty = reset
        for codon in chunks(seq.seq, 3):
            # If stop codon is encountered, highlight it
            if highlight_stop_codons and str(codon) in stop_codons:
                pretty += stop_codons[str(codon)]
            # otherwise add colored bases
            else:
                for letter in codon:
                    pretty += dna[letter]
            
        print(pretty + "\n")
        
def chunks(seq, n):
    """Yield successive n-sized chunks from seq."""
    for i in range(0, len(seq), n):
        yield seq[i:i + n]

if __name__ == "__main__":
    main()
