#!/bin/env python
"""
cats: cat for sequence data

Keith Hughitt <khughitt@umd.edu>

TODO:
    *support for piping colored output into head/tail
    *support for specifying input file format
"""
def colorize(input_, **kwargs):
    """Colorizes the target sequence"""
    import os
    import textwrap
    from Bio import SeqIO
    from Bio import Seq, SeqRecord
    from Bio.Alphabet import IUPAC

    # Get default args
    args = _defaults()
    args.update(kwargs)

    # Check input type
    if isinstance(input_, basestring):
        if os.path.isfile(input_):
            # Read in FASTA file
            seqs = SeqIO.parse(input_, 'fasta')
        else:
            # Sequence string?
            try:
                seqs = [SeqRecord.SeqRecord(Seq.Seq(input_, IUPAC.IUPACUnambiguousDNA()))]
            except:
                raise UnrecognizedInput

    elif isinstance(input_, SeqRecord.SeqRecord):
        seqs = [input_]
    elif isinstance(input_, Seq.Seq):
        seqs = [SeqRecord.SeqRecord(input_)]
    else:
        raise UnrecognizedInput

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
    config_file = os.path.expanduser("~/.catsrc")
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
    if args['translate']:
        # determine frame to use
        frame = abs(args['translation_frame']) - 1

        # select translation table
        # see: ftp://ftp.ncbi.nlm.nih.gov/entrez/misc/data/gc.prt

        # print without colors
        if args['no_color']:
            for seq in seqs:
                print(">" + seq.description)
                # forward frames
                if args['translation_frame'] > 0:
                    translated = str(seq.seq[frame:].translate(
                        table=args['translation_table'])
                )
                # complemented frames
                else:
                    reverse_comp = seq.seq.reverse_complement()[frame:]
                    translated = str(reverse_comp.translate(
                        table=args['translation_table'])
                    )
                print("\n".join(textwrap.wrap(translated, args['line_width'])))
        else:
            # Amino Acids
            for seq in seqs:
                pretty = reset

                # Print description
                print(bold + ">" + seq.description)

                # print seq.seq[frame:]
                # Translate and add stylized residues to otput string
                if args['translation_frame'] > 0:
                    translated = seq.seq[frame:].translate(
                        table=args['translation_table']
                    )
                else:
                    reverse_comp = seq.seq.reverse_complement()[frame:]
                    translated = str(reverse_comp.translate(
                        table=args['translation_table']
                    ))
                
                for i, residue in enumerate(translated, start=1):
                     pretty += amino_acids[residue]
                     # Add new lines to ensure desired line width
                     if i % args['line_width'] == 0:
                         pretty += "\n"
                 
                print(pretty)
    else:
        # Nuceotides
        # loop through and print seqs
        # @NOTE - could pause here after each record if desired
        if args['no_color']:
            for seq in seqs:
                print(">" + seq.description)
                print(seq.seq)
        else:
            for seq in seqs:
                print(bold + ">" + seq.description)
                
                # For DNA, read bases three at a time
                # For now, assume reading frame starts from index 0
                pretty = reset
                for codon in _chunks(seq.seq, 3):
                    # If stop codon is encountered, highlight it
                    if args['stop_codons'] and str(codon) in stop_codons:
                        pretty += stop_codons[str(codon)]
                    # otherwise add colored bases
                    else:
                        for letter in codon:
                            pretty += dna[letter]
                print(pretty)

def _chunks(seq, n):
    """Yield successive n-sized chunks from seq."""
    for i in range(0, len(seq), n):
        yield seq[i:i + n]
def _get_args():
    """Parses input and returns arguments"""
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Pretty-print sequence data')
    parser.add_argument('-n', '--no-color', dest='no_color', 
                        action='store_true')
    parser.add_argument('--start-codons', dest='start_codons',
                        action='store_true',
                        help='Highlight any start codons in DNA/RNA output')
    parser.add_argument('--stop-codons', dest='stop_codons',
                        action='store_true',
                        help='Highlight any stop codons in DNA/RNA output')
    parser.add_argument('file', help='File containing sequence data.')
    parser.add_argument('-t', '--translate', action='store_true',
                        help='Translate a nucleotide sequence to an ' +
                             'amino acid sequence.', dest='translate')
    parser.add_argument('--translation-table', dest='translation_table',
                        help='NCBI translation table ' +
                        'to use (default=1)', metavar='NUMBER')
    parser.add_argument('-o', '--translation-frame', metavar='FRAME', 
                        type=int, dest='translation_frame',
                        help='Frame to use when translating to amino acids: ' +
                             'forward and reverse complement frames are ' +
                             'specified using 1, 2, 3, -1, -2, and -3. The ' + 
                             'default frame is 1 (first foward frame).')
    parser.add_argument('-w', '--line-width', type=int, metavar="WIDTH",
                        help='Number of characters to limit lines to ' + 
                             '(default: 80)', dest='line_width')
    args = parser.parse_args()

    # convert to a python dict and return without 
    return dict((k, v) for k, v in vars(args).iteritems() if v is not None)

def _defaults():
    """Returns a dictionary containing the default arguments to use during
    colorization."""
    return {
        "no_color": False,
        "start_codons": False,
        "stop_codons": False,
        "translate": False,
        "translation_table": 1,
        "translation_frame": 1,
        "line_width": 80
    }

class UnrecognizedInput(IOError):
    """Unrecognized input error"""
    pass

def main():
    """Main"""
    import sys
    import os

    # Check for input file
    kwargs = _get_args()

    if not 'file' in kwargs:
        print("No input file specified")
        sys.exit()
    filepath = os.path.expanduser(kwargs['file'])

    if not os.path.isfile(filepath):
        print("No input specified")
        sys.exit()

    colorize(filepath, **kwargs)

if __name__ == "__main__":
    import sys
    sys.exit(main())

