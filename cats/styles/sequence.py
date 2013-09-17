"""
Nucleic acid/protein sequence formatter
"""
class SequenceFormatter(object):
    def __init__(self, custom_colors=None):
        self._load_nucleic_acid_mapping(custom_colors)
        self._load_amino_acid_mapping()

    def _load_nucleic_acid_mapping(self, custom_colors):
        """Loads nucleic acid mapping"""
        from cats.styles import colors

        # Generate list of colors to use for printing, ex:
        dna_colors = [colors.RED, colors.GREEN, colors.BLUE, colors.MAGENTA]

        # DNA
        self.dna = dict((x, dna_colors[i] + x) for i, x in
                         enumerate(('A', 'C', 'G', 'T')))

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
                                   k, v in amino_acid_colors.items())

    def format_dna(self, seq, color_stop_codons=False, color_cpg=False):
        """Format a string of DNA nucleotides"""
        output = ""

        # For DNA, read bases three at a time
        # For now, assume reading frame starts from index 0
        for codon in self._chunks(seq, 3):
            # (Optional) If stop codon is encountered, highlight it
            if color_stop_codons and str(codon) in stop_codons:
                output += stop_codons[str(codon)]
            else:
                for letter in codon:
                    output += self.dna[letter]

        # (Optional) Highlight CpG dinucleotides
        if color_cpg:
            output = output.replace(self.dna['C'] + self.dna['G'], 
                                    '\033[0;044m\033[1;038mCG\033[0m')

        return output

    def format_protein(self, seq, line_width=80):
        """Formats a protein sequence"""
        output = ""
        for i, residue in enumerate(seq, start=1):
             output += self.amino_acid[residue]

             # Add new lines to ensure desired line width
             if i % line_width == 0:
                 seq += "\n"

        return output

    def _chunks(self, seq, n):
        """Yield successive n-sized chunks from seq."""
        for i in range(0, len(seq), n):
            yield seq[i:i + n]


