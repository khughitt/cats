"""
SeqString formatter
"""
class SeqStringFormatter(object):
    """Formatter for sequence strings"""
    def __init__(self, theme):
        """Creates a new SeqStringFormatter instance"""
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
            for i, line in enumerate(inbuffer):
                # Reset formatting
                outbuffer.write(RESET)

                # Convert from byte-string if coming from gzip
                if type(line) is bytes:
                    line = line.decode('ascii')

                # Print description
                outbuffer.write(self.seq_formatter.format_nucleic_acid(line,
                                                        kwargs['stop_codons'],
                                                        kwargs['cpg']))
        else:
            for line in inbuffer:
                outbuffer.write(line)

class UnrecognizedInput(IOError):
    """Unrecognized input error"""
    pass
