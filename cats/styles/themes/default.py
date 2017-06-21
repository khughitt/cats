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

