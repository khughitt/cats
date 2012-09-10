#!/bin/env python
"""
moref:  more for FASTA files

TODO:
    *support for piping colored output into head/tail
    *support for specifying input file format
"""
import sys
import os
import textwrap
from argparse import ArgumentParser
from Bio import SeqIO

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
    
    # RNA
    
    # Protein
    # @TODO: Order by electronegativity?
    amino_acid_colors = {
        # Positively charged side chains (blue)
        "R": 75,
        "H": 69,
        "K": 63,
        # Negatively charged side chains (red)
        "D": 168,
        "E": 160,
        # Polar uncharged side chains (purple)
        "S": 189,
        "T": 183,
        "N": 177,
        "Q": 171,
        # Special cases (yellow)
        "C": 190,
        "U": 191,
        "G": 192,
        "P": 193,
        # Hydrophobic side chains (green)
        "A": 121,
        "V": 120,
        "I": 119,
        "L": 118,
        "M": 85,
        "F": 84,
        "Y": 83,
        "W": 82,
        "*": 255,
        "-": 255
    }

    amino_acids = dict((k, '\033[38;05;%dm%s' % (v, k)) for 
                       k, v in amino_acid_colors.items())
    
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
    
    # For now only display amino acids when translate requested
    # @TODO: automatically detect/allow user to specify
    try:
        if args.translate:
            # determine frame offset to use
            offset = abs(args.translation_offset) - 1

            # print without colors
            if args.no_color:
                for seq in seqs:
                    print(">" + seq.description)
                    # forward frames
                    if args.translation_offset > 0:
                        translated = str(seq.seq[offset:].translate())
                    # complemented frames
                    else:
                        reverse_comp = seq.seq.reverse_complement()[offset:]
                        translated = str(reverse_comp.translate())
                    print("\n".join(textwrap.wrap(translated, args.line_width)))
            else:
                # Amino Acids
                for seq in seqs:
                    pretty = reset
        
                    # Print description
                    print(bold + ">" + seq.description)
                    
                    # Translate and add stylized residues to otput string
                    if args.translation_offset > 0:
                        translated = seq.seq[offset:].translate()
                    else:
                        reverse_comp = seq.seq.reverse_complement()[offset:]
                        translated = str(reverse_comp.translate())
                    
                    for i, residue in enumerate(translated, start=1):
                         pretty += amino_acids[residue]
                         # Add new lines to ensure desired line width
                         if i % args.line_width == 0:
                             pretty += "\n"
                     
                    print(pretty)
        else:
            # Nuceotides
            # loop through and print seqs
            # @NOTE - could pause here after each record if desired
            if args.no_color:
                for seq in seqs:
                    print(">" + seq.description)
                    print(seq.seq)
            else:
                for seq in seqs:
                    print(bold + ">" + seq.description)
                    
                    # For DNA, read bases three at a time
                    # For now, assume reading frame starts from index 0
                    pretty = reset
                    for codon in chunks(seq.seq, 3):
                        # If stop codon is encountered, highlight it
                        if args.stop_codons and str(codon) in stop_codons:
                            pretty += stop_codons[str(codon)]
                        # otherwise add colored bases
                        else:
                            for letter in codon:
                                pretty += dna[letter]
                        
                    print(pretty)
    except IOError, e:
        pass
    
def chunks(seq, n):
    """Yield successive n-sized chunks from seq."""
    for i in range(0, len(seq), n):
        yield seq[i:i + n]
        
def get_args():
    """Parses input and returns arguments"""
    parser = ArgumentParser(description='Pretty-print sequence data')
    parser.add_argument('-n', '--no-color', dest='no_color', 
                        action='store_true', default=False)
    parser.add_argument('--start-codons', dest='start_codons',
                        action='store_true', default=False,
                        help='Highlight any start codons in DNA/RNA output')
    parser.add_argument('--stop-codons', dest='stop_codons',
                        action='store_true', default=False,
                        help='Highlight any stop codons in DNA/RNA output')
    parser.add_argument('file', help='File containing sequence data.')
    parser.add_argument('-t', '--translate', action='store_true',
                        help='Translate a nucleotide sequence to an ' +
                             'amino acid sequence.',
                        dest='translate', default=False)
    parser.add_argument('-o', '--translation-offset', metavar='OFFSET', 
                        type=int, default=1, dest='translation_offset',
                        help='Offset to use when translating to amino acids: ' +
                             'forward and reverse complement frames are ' +
                             'specified using 1, 2, 3, -1, -2, and -3. The ' + 
                             'default offset is 1 (first foward frame).')
    parser.add_argument('-w', '--line-width', type=int, metavar="WIDTH",
                        help='Number of characters to limit lines to ' + 
                             '(default: 60)', default=60, dest='line_width')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
