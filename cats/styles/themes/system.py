"""
Theme incorporating system colors
"""
from cats.styles import colors
from cats.styles.themes import amino_acids,GREP_HIGHLIGHT_COLOR

# DNA/RNA
nucleotides = {
    "A": colors.RED + "A",
    "C": colors.GREEN + "C",
    "G": colors.BLUE + "G",
    "T": colors.MAGENTA + "T",
    "U": colors.MAGENTA + "U",
    "N": colors.WHITE + "N",
    "\n": "\n"
}

# GFF files
gff_colors = {
    'meta': colors.LIGHTGREY,
    '1a': colors.RED_DARK,
    '1b': colors.RED,
    '2a': colors.BLUE_DARK,
    '2b': colors.BLUE,
    '3a': colors.YELLOW_DARK,
    '3b': colors.YELLOW,
    '4a': colors.MAGENTA_DARK,
    '4b': colors.MAGENTA,
    '5a': colors.CYAN_DARK,
    '5b': colors.CYAN,
    '6a': colors.GREEN_DARK,
    '6n': colors.GREEN
}

