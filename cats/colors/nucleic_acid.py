"""
DNA/RNA color mapping
"""

# Generate list of colors to use for printing, ex:
# regular    - \033[032m
# emphasized - \033[1;032m
# bright     - \033[092m
_colors = ['\033[0%dm' % i for i in range(91, 95)]

# DNA
dna = dict((x, _colors[i] + x) for i, x in enumerate(('A', 'C', 'G', 'T')))
