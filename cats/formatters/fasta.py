"""
FASTA formatter
"""
class FASTAFormatter(object):
    """Formatter for FASTA files"""
    def __init__(self):
        """Creates a new FASTAFormatter instance"""
        import os
        import configparser
        from cats.styles.sequence import SequenceFormatter

        # Load sequence formatter
        self.seq_formatter = SequenceFormatter()

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

                # DNA
                outbuffer.write(self.seq_formatter.format_dna(line,
                                                        kwargs['stop_codons'],
                                                        kwargs['cpg']))
        else:
            for line in inbuffer:
                outbuffer.write(line)

class UnrecognizedInput(IOError):
    """Unrecognized input error"""
    pass
