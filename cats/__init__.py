"""
cats
"""
__version__ = 0.1

import cats.styles
import cats.io
import cats.data

def format(input_, *args, **kwargs):
    """Formats bioinformatics related data for display on the console."""
    import os
    import textwrap
    from Bio import SeqIO
    from Bio import Seq, SeqRecord
    from Bio.Alphabet import IUPAC
    from cats.io.file import detect_format

    # Check input type
    if isinstance(input_, basestring):
        if os.path.isfile(input_):
            file_format = detect_format(input_)

            # Sequence recoreds (e.g. FASTA)
            if (file_format in ['fasta']):
                seqs = SeqIO.parse(input_, file_format)
        else:
            # Sequence string?
            try:
                seqs = [SeqRecord.SeqRecord(
                           Seq.Seq(input_, IUPAC.IUPACUnambiguousDNA()))]
            except:
                raise UnrecognizedInput
    elif isinstance(input_, SeqRecord.SeqRecord):
        seqs = [input_]
    elif isinstance(input_, Seq.Seq):
        seqs = [SeqRecord.SeqRecord(input_)]
    else:
        raise UnrecognizedInput

    # Default to SeqRecord formatter
    formatter = cats.io.formatter.SeqRecordFormatter()
    return formatter.format(seqs, **kwargs)

