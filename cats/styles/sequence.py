"""
Nucleic acid/protein sequence formatter
"""
import re

class SequenceFormatter(object):
    def __init__(self, custom_colors=None):
        self._load_nucleic_acid_mapping(custom_colors)
        self._load_amino_acid_mapping()

    def _load_nucleic_acid_mapping(self, custom_colors):
        """Loads nucleic acid mapping"""
        from cats.styles import colors

        # Generate list of colors to use for printing, ex:
        dna_colors = [colors.RED, colors.GREEN, colors.BLUE, colors.MAGENTA,
                      colors.WHITE]

        # DNA
        self.dna = dict((x, dna_colors[i] + x) for i, x in
                         enumerate(('A', 'C', 'G', 'T', 'N')))
        self.dna['\n'] = '\n'

        # Apply any custom color settings
        if custom_colors is not None:
            for k,v in custom_colors:
                mod_color = "\033%s%s" % (v, k.upper())
                self.dna[k.upper()] = mod_color

        # start/stop codons
        stop_template = '\033[0;041m\033[1;038m%s\033[0m'

        self.stop_codons = {
            "TAG": stop_template % "TAG",
            "TAA": stop_template % "TAA",
            "TGA": stop_template % "TGA"
        }

    def _load_amino_acid_mapping(self):
        """Loads amino acid style mapping"""
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

        self.amino_acid = dict((k, '\033[38;05;%dm%s' % (v, k)) for
                                   k, v in list(amino_acid_colors.items()))
        self.amino_acid['\n'] = '\n'

    def format_dna(self, seq, color_stop_codons=False, color_cpg=False):
        """Format a string of DNA nucleotides"""
        from cats.styles import colors

        output = ""

        # Check for pre-existing highlighting (e.g. grep)
        #highlight_ranges = []

        #for match in re.finditer(colors.GREP_HIGHLIGHT_RANGE, seq):
        #    highlight_ranges.append((match.
        for i, part in enumerate(re.split(colors.GREP_HIGHLIGHT_RANGE, str(seq))):
            if i % 2 == 0:
                output += "".join([self.dna[letter] for letter in part])
            else:
                #output += '\033[38;05;227m%s\033[0m' % part
                output += colors.YELLOW + part + colors.RESET

        # Colorize sequence
        #output = "".join([self.dna[letter] for letter in str(seq)])

        # (Optional) Highlight stop codons
        if color_stop_codons:
            for stop in ['TAG', 'TAA', 'TGA']:
                output = output.replace("".join([self.dna[x] for x in stop]))

        # (Optional) Highlight CpG dinucleotides
        if color_cpg:
            output = output.replace(self.dna['C'] + self.dna['G'], 
                                    '\033[0;044m\033[1;038mCG\033[0m')

        return output

    def format_protein(self, seq):
        """Formats a protein sequence"""
        output = ""
        for i, residue in enumerate(str(seq), start=1):
             output += self.amino_acid[residue]

        return output

