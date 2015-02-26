"""
Nucleic acid/protein sequence formatter
"""
import re
import sys

class SequenceFormatter(object):
    def __init__(self, theme='default'):
        # load theme
        theme_module = 'cats.styles.themes.%s' % theme
        __import__(theme_module)
        self._theme = sys.modules[theme_module]

        self.dna = self._theme.nucleic_acids
        self.amino_acid = self._theme.amino_acids

        # start/stop codons
        stop_template = '\033[0;041m\033[1;038m%s\033[0m'

        self.stop_codons = {
            "TAG": stop_template % "TAG",
            "TAA": stop_template % "TAA",
            "TGA": stop_template % "TGA"
        }

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
                output += self._theme.GREP_HIGHLIGHT_COLOR + part + colors.RESET

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

