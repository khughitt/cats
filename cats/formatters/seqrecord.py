"""
SeqRecord formatter.
"""
class SeqRecordFormatter(object):
    """Formatter for BioPython SeqRecord objects"""
    def __init__(self, theme):
        """Creates a new SeqRecordFormatter instance"""
        from cats.styles.sequence import SequenceFormatter

        # Load sequence formatter
        self.seq_formatter = SequenceFormatter(theme)

    def format(self, seqs, outbuffer=None, **kwargs):
        """Format sequence records"""
        # default to STDOUT for output
        if outbuffer is None:
            import sys
            outbuffer = sys.stdout

        # for x in range(1,10):
        # print "\033[03%dmTEST   \033[09%dmTEST" % (x,x)

        # default/bold text
        RESET = '\033[0m'
        BOLD = '\033[1m'

        # select translation table
        # see: ftp://ftp.ncbi.nlm.nih.gov/entrez/misc/data/gc.prt

        # Iterate through and format each sequence record
        for seq in seqs:
            # Reset formatting
            outbuffer.write(RESET)

            # Print description
            if kwargs['color']:
                outbuffer.write(BOLD)

            outbuffer.write(">" + seq.description + "\n")

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
                    outbuffer.write(self.seq_formatter.format_protein(_seq))
                else:
                    outbuffer.write(self._fill(translated, width))

            # DNA
            else:
                if kwargs['color']:
                    _seq = self._fill(str(seq.seq), width)
                    outbuffer.write(self.seq_formatter.format_nucleic_acid(_seq,
                                                         kwargs['stop_codons'],
                                                         kwargs['cpg']))
                else:
                    outbuffer.write(self._fill(str(seq.seq), width))

    def _fill(self, text, width=70):
        """
        Faster text-wrapping for long strings
        source: http://stackoverflow.com/questions/2657693/insert-a-newline-character-every-64-characters-using-python/2657733#2657733
        """
        return '\n'.join(text[i:i+width] for i in range(0, len(text), width))

class UnrecognizedInput(IOError):
    """Unrecognized input error"""
    pass
