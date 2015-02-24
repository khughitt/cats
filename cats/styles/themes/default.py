"""
Default colorscheme

Colorscheme is roughly based off of what I have seen used in other sequence
manipulation tools. So far I have not come across any conventions for
displaying sequence letter, otherwise that might be a reasonable default to
use.
"""
nucleic_acids = {
    "A": 28,
    "C": 12,
    "G": 166,
    "T": 196,
    "U": 196
}

amino_acids = {
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

GREP_HIGHLIGHT_COLOR = "\033[38;05;%dm" % (226) # Yellow
