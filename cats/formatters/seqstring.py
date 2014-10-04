"""
SeqString formatter
"""
class SeqStringFormatter(object):
    """Formatter for sequence strings"""
    def __init__(self):
        """Creates a new SeqStringFormatter instance"""
        import os
        import configparser
        from cats.styles.sequence import SequenceFormatter

        # Use custom colors if specified
        config_file = os.path.expanduser("~/.catsrc")

        # Load config file
        config = configparser.ConfigParser()
        if os.path.isfile(config_file):
            config.read(config_file)

        dna_colors = {}
        if config.has_section('dna'):
            dna_colors = config.items('dna')

        # Load sequence formatter
        self.seq_formatter = SequenceFormatter(dna_colors)

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
                outbuffer.write(self.seq_formatter.format_dna(line,
                                                        kwargs['stop_codons'],
                                                        kwargs['cpg']))
        else:
            for line in inbuffer:
                outbuffer.write(line)

class UnrecognizedInput(IOError):
    """Unrecognized input error"""
    pass
