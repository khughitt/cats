#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
cats: cat for sequence data

Keith Hughitt <khughitt@umd.edu>

TODO:
    * convert to class?
"""
def main():
    """Main"""
    import sys
    import os
    import cats
    import pydoc
    import types

    # Get default args
    kwargs = cats._load_config(entry_point='cli')

    # update default arguments with user-specified settings
    parser = _get_args()

    # convert to a python dict and return without 
    args = parser.parse_args()
    args = dict((k, v) for k, v in list(vars(args).items()) if v is not None)

    kwargs.update(args)

    # @TODO Refactor
    if not sys.stdin.isatty():
        try:
            stream_formatter = cats.format(sys.stdin.buffer, **kwargs)
            sys.exit()
        except BrokenPipeError:
            sys.exit()
        except KeyboardInterrupt:
            sys.exit()

    # If not arguments specified dispay help
    if (len(sys.argv) == 1) or ("-h" in sys.argv) or ("--help" in sys.argv):
        _print_logo()
        parser.print_help()
        sys.exit()

    # Check for input file
    filepath = os.path.expanduser(args['file'])

    if not os.path.isfile(filepath):
        print("Invalid filepath specified")
        sys.exit()

    try:
        output = cats.format(filepath, **kwargs)
    except BrokenPipeError:
        sys.exit()
    except KeyboardInterrupt:
        sys.exit()

    # output results
    try:
        if isinstance(output, str):
            print(output)
        else:
            outbuffer = sys.stdout
            for line in output:
                outbuffer.write(line)
        sys.exit()
    except BrokenPipeError:
        sys.exit()
    except KeyboardInterrupt:
        sys.exit()

    # output pager
    #pager_cmd = 'less -R'
    #if (args['chop']):
    #    pager_cmd += "S"
    #pydoc.pipepager(output, cmd=pager_cmd)

def _get_args():
    """Parses input and returns arguments"""
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Pretty-print sequence data')
    parser.add_argument('-f', '--format',
                        help=('Input file format. Will attempt to autodetect '
                              'format if none is specified.'))
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
    parser.add_argument('file', help='File containing sequence data.',
                        nargs='?')
    parser.add_argument('-s', '--seq-type', dest='seq_type',
                        help='Manually specify sequence type: dna,rna, or protein')
    parser.add_argument('-S', '--chop-long-lines', dest='chop', 
                        action='store_true',
                        help='Causes lines longer  than  the screen width ' +
                        'to be chopped (truncated) rather than wrapped.')
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
                        help='Number of characters to limit sequence lines ' +
                             'to (default: 70)', dest='line_width')

    return parser

def _print_logo():
    """Print cats logo

    Based on an ascii art version of nyan cat from an unknown source.
    """
    print("\n\033[38;05;196m`·.A,¸,.·A`·.,¸,.T··.\033[0m╭━━━━━╮\n"
          "\033[38;05;220m`·.T,¸,.·A`·.,¸,.T··.\033[0m|:::: /\_/\    "
          "\033[38;05;196mc\033[38;05;220ma\033[38;05;46mt\033[38;05;99ms\n"
          "\033[38;05;46m`·.G,¸,.·C`·.,¸,.T·\033[0m╰ |::::(◕ ω ◕)   biological sequence printer\n"
          "\033[38;05;99m`·.A,¸,.·A`·.,¸,.T·`·.\033[0mu-u━━-u--u\n")

