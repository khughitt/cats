"""
SeqRecord formatter.
"""
class SeqRecordFormatter(object):
    """Formatter for BioPython SeqRecord objects"""
    def __init__(self):
        """Creates a new SeqRecordFormatter instance"""
        import os
        import ConfigParser
        from cats.styles.sequence import SequenceFormatter

        # Use custom colors if specified
        config_file = os.path.expanduser("~/.catsrc")

        # Load config file
        config = ConfigParser.ConfigParser()
        if os.path.isfile(config_file):
            config.read(config_file)

        dna_colors = {}
        if config.has_section('dna'):
            dna_colors = config.items('dna')

        # Load sequence formatter
        self.seq_formatter = SequenceFormatter(dna_colors)

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
        for seq in seqs:
            # Reset formatting
            buffer += RESET

            # Print description
            if kwargs['color']:
                buffer += BOLD

            buffer += ">" + seq.description + "\n"

            # line width
            width = kwargs['line_width']

            # Protein
            if kwargs['translate']:

                # determine frame to use
                frame = abs(kwargs['translation_frame']) - 1
                dna_str = seq.seq[frame:]

                if kwargs['translation_frame'] < 0:
                    dna_str = seq.seq.reverse_complement()[frame:]

                table = kwargs['translation_table']
                translated = str(dna_str.translate(table=table))

                # format and append to output buffer
                if kwargs['color']:
                    _seq = self._fill(translated, width)
                    buffer += self.seq_formatter.format_protein(_seq)
                else:
                    buffer += self._fill(translated, width)

            # DNA
            else:
                if kwargs['color']:
                    _seq = self._fill(str(seq.seq), width)
                    buffer += self.seq_formatter.format_dna(_seq,
                                                         kwargs['stop_codons'],
                                                         kwargs['cpg'])
                else:
                    buffer += self._fill(str(seq.seq), width)

        # Return result
        return buffer

    #def _fill(self, text, width=70):
        #"""
        #Faster text-wrapping for long strings
        #source: http://stackoverflow.com/questions/2657693/insert-a-newline-character-every-64-characters-using-python/2657733#2657733
        #"""
        #return '\n'.join(text[i:i+width] for i in range(0, len(text), width))

    def _fill(self, text, width=70):
        """
        ANSI-intelligent text-wrapping.
        """
        # convert string to an iterable
        string = iter(text)

        output = ''

        for i, char in enumerate(string):
            # ansi escape sequence
            if char == '\x1b':
                # find matching escape sequence
                output += '\x1b'
                next_char = next(string)
                output += next_char

                while next_char != "\x1b":
                    next_char = next(string)
                    output += next_char

                # last two characters ([K)
                output += next(string)
                output += next(string)
            else:
                # otherwise add char and wrap at specified width
                output += char
                if i > 0 and i % width == 0:
                    output += '\n'

        # return wrapped string
        return output


class UnrecognizedInput(IOError):
    """Unrecognized input error"""
    pass
