"""
SeqRecord formatter.
"""
class SeqRecordFormatter(object):
    """Formatter for BioPython SeqRecord objects"""
    def __init__(self):
        """Creates a new SeqRecordFormatter instance"""
        import os
        import ConfigParser
        from cats.styles.nucleic_acid import NucleicAcidFormatter
        from cats.styles.protein import amino_acid

        # Use custom colors if specified
        config_file = os.path.expanduser("~/.catsrc")

        # Load config file
        config = ConfigParser.ConfigParser()
        if os.path.isfile(config_file):
            config.read(config_file)

        dna_colors = {}
        if config.has_section('dna'):
            dna_colors = config.items('dna')

        # Store mappings
        self.amino_acid = amino_acid
        self.dna_formtter = NucleicAcidFormatter(dna_colors)

    def format(self, seqs, **kwargs):
        """Format sequence records"""
        # output buffer
        buffer = ""

        # for x in range(1,10):
        # print "\033[03%dmTEST   \033[09%dmTEST" % (x,x)

        # default/bold text
        RESET = '\033[0m'
        BOLD = '\033[1m'

        # For now only display amino acids when translate requested
        # @TODO: automatically detect/allow user to specify

        # select translation table
        # see: ftp://ftp.ncbi.nlm.nih.gov/entrez/misc/data/gc.prt

        # Iterate through and format each sequence record
        for x in seqs:
            # Reset formatting
            seq = RESET

            # Print description
            if kwargs['color']:
                seq += BOLD

            # Protein
            if kwargs['translate']:
                # determine frame to use
                frame = abs(kwargs['translation_frame']) - 1
                dna_str = x.seq[frame:]

                if kwargs['translation_frame'] < 0:
                    dna_str = x.seq.reverse_complement()[frame:]
                translated = dna_str.translate(table=kwargs['translation_table'])

                # format and append to output buffer
                if kwargs['color']:
                    for i, residue in enumerate(translated, start=1):
                         seq += self.amino_acid[residue]
                         # Add new lines to ensure desired line width
                         if i % kwargs['line_width'] == 0:
                             seq += "\n"
                    print(seq)
                else:
                    print("\n".join(textwrap.wrap(translated,
                                                  kwargs['line_width'])))
            # DNA
            else:
                if kwargs['color']:
                    seq += self.dna_formatter.format_dna(x.seq,
                                          kwargs['stop_codons'], kwargs['cpg'])
                else:
                    seq += x.seq

            # Append formatted sequence to output buffer
            buffer += seq

        # Return result
        return buffer

class UnrecognizedInput(IOError):
    """Unrecognized input error"""
    pass
