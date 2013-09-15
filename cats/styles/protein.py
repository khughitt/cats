"""
Amino acid color mapping
"""
# Protein
# @TODO: Order by electronegativity?
_amino_acid_colors = {
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

amino_acid = dict((k, '\033[38;05;%dm%s' % (v, k)) for 
                   k, v in _amino_acid_colors.items())


