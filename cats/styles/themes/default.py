"""
Default colorscheme

Colorscheme is roughly based off of what I have seen used in other sequence
manipulation tools. So far I have not come across any conventions for
displaying sequence letter, otherwise that might be a reasonable default to
use.
"""
from cats.styles.themes import amino_acids,GREP_HIGHLIGHT_COLOR

# DNA/RNA sequences
_nucleotide_mapping = {
    "A": 28,
    "C": 12,
    "G": 166,
    "T": 196,
    "U": 196
}

nucleotides = dict((k, '\033[38;05;%dm%s' % (v, k)) for
                        k, v in list(_nucleotide_mapping.items()))
nucleotides['\n'] = '\n'

# GFF files
# \033[38;05;%dm
gff_colors = {
    'meta': '\033[38;05;250m',
    '1a': '\033[38;05;184m',
    '1b': '\033[38;05;220m',
    '2a': '\033[38;05;41m',
    '2b': '\033[38;05;77m',
    '3a': '\033[38;05;45m',
    '3b': '\033[38;05;117m',
    '4a': '\033[38;05;250m',
    '4b': '\033[38;05;251m',
    '5a': '\033[38;05;252m',
    '5b': '\033[38;05;253m',
    '6a': '\033[38;05;254m',
    '6b': '\033[38;05;255m'
}

