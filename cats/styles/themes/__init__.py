#
# Shared theme elements
#

# Amino Acid sequences
_amino_acid_mapping = {
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
                        k, v in list(_amino_acid_mapping.items()))
amino_acids['\n'] = '\n'

# grep highlighting
GREP_HIGHLIGHT_COLOR = "\033[38;05;%dm" % (226) # Yellow

