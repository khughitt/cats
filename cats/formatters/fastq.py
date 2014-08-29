"""
FASTQ formatter
"""
class FASTQFormatter(object):
    """Formatter for FASTQ files"""
    def __init__(self):
        """Creates a new FASTQFormatter instance"""
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

        # FASTQ line types
        FASTQ_ID = 0
        FASTQ_SEQ = 1
        FASTQ_DESC = 2
        FASTQ_QUAL = 3

        # Iterate through and format each sequence record
        if kwargs['color']:
            for i, line in enumerate(inbuffer):
                # Reset formatting
                outbuffer.write(RESET)

                # Convert from byte-string if coming from gzip
                if type(line) is bytes:
                    line = line.decode('ascii')

                # Print description
                if i % 4 == FASTQ_ID:
                    outbuffer.write(BOLD + line)
                elif i % 4 == FASTQ_SEQ:
                    outbuffer.write(self.seq_formatter.format_dna(line,
                                                            kwargs['stop_codons'],
                                                            kwargs['cpg']))
                else:
                    outbuffer.write(line)
        else:
            for line in inbuffer:
                outbuffer.write(line)

class UnrecognizedInput(IOError):
    """Unrecognized input error"""
    pass
