"""
FASTA formatter
"""
class FASTAFormatter(object):
    """Formatter for FASTA files"""
    def __init__(self, theme):
        """Creates a new FASTAFormatter instance"""
        import os
        from cats.styles.sequence import SequenceFormatter

        # Load sequence formatter
        self.seq_formatter = SequenceFormatter(theme)

    def format(self, inbuffer, outbuffer=None, **kwargs):
        """Format sequence records"""
        import sys

        # default/bold text
        RESET = '\033[0m'
        BOLD = '\033[1m'

        # default to STDOUT for output
        if outbuffer is None:
            outbuffer = sys.stdout

        # Iterate through and format each sequence record
        if kwargs['color']:
            for line in inbuffer:
                # Reset formatting
                outbuffer.write(RESET)

                # Print description
                if line.startswith('>'):
                    outbuffer.write(BOLD + line)
                    continue

                # DNA/RNA
                if kwargs['seq_type'] in ['dna', 'rna', 'nucleic_acid']:
                    outbuffer.write(self.seq_formatter.format_nucleic_acid(
                        line, kwargs['stop_codons'], kwargs['cpg']
                    ))
                else:
                    # Protein
                    outbuffer.write(self.seq_formatter.format_protein(line))
        else:
            for line in inbuffer:
                outbuffer.write(line)

class UnrecognizedInput(IOError):
    """Unrecognized input error"""
    pass
