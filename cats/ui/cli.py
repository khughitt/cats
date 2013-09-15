#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
cats: cat for sequence data

Keith Hughitt <khughitt@umd.edu>

TODO:
    *support for piping colored output into head/tail
    *support for specifying input file format
    *generalizing highlight support (can keep --cpg, etc as convenience methods
     which use the highlight functionality)
    *alternate color schemes (e.g. http://www.ugr.es/~proyecto08173/qbiofisica/PROGRAMAS%20DE%20ORDENADOR/Analisis%20grafico%20de%20macromoleculas%20-%20Rastop%202.2/help/colour.htm)
"""
def main():
    """Main"""
    import sys
    import os
    from cats import formatter

    # If not arguments specified dispay help
    if (len(sys.argv) == 1) or ("-h" in sys.argv) or ("--help" in sys.argv):
        _print_logo()

    # Check for input file
    args = _get_args()

    filepath = os.path.expanduser(args['file'])

    if not os.path.isfile(filepath):
        print("No input specified")
        sys.exit()

    # Get default args
    kwargs = _defaults()
    kwargs.update(args)

    formatter.format(filepath, **kwargs)

def _get_args():
    """Parses input and returns arguments"""
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Pretty-print sequence data')
    parser.add_argument('--no-color', dest='color', 
                        action='store_false')
    parser.add_argument('--start-codons', dest='start_codons',
                        action='store_true',
                        help='Highlight any start codons in DNA/RNA output')
    parser.add_argument('--stop-codons', dest='stop_codons',
                        action='store_true',
                        help='Highlight any stop codons in DNA/RNA output')
    parser.add_argument('--cpg', dest='cpg',
                        action='store_true',
                        help='Highlight CpG dinucleotides')
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
        "color": True,
        "start_codons": False,
        "stop_codons": False,
        "translate": False,
        "translation_table": 1,
        "translation_frame": 1,
        "line_width": 80
    }

def _print_logo():
    """Print cats logo
    Based on an ascii art version of nyan cat from an unknown source. 
    """
    print("\n\033[38;05;196m`·.A,¸,.·A`·.,¸,.T··.\033[0m╭━━━━━╮\n"
          "\033[38;05;220m`·.T,¸,.·A`·.,¸,.T··.\033[0m|:::: /\_/\    "
          "\033[38;05;196mc\033[38;05;220ma\033[38;05;46mt\033[38;05;93ms\n"
          "\033[38;05;46m`·.G,¸,.·C`·.,¸,.T·\033[0m╰ |::::(◕ ω ◕)   biological sequence printer\n"
          "\033[38;05;93m`·.A,¸,.·A`·.,¸,.T·`·.\033[0mu-u━━-u--u\n")
