"""
cats
"""
__version__ = 0.1

import cats.styles
import cats.data
import cats.formatters

def format(input_, *args, **kwargs):
    """Formats bioinformatics related data for display on the console."""
    import os
    from io import TextIOWrapper
    from Bio import SeqIO
    from Bio import Seq, SeqRecord
    from Bio.Alphabet import IUPAC
    from cats.files import detect_format

    # Check input type
    if isinstance(input_, basestring):
        if os.path.isfile(input_):
            file_format = detect_format(input_)

            # Sequence recoreds (e.g. FASTA)
            if (file_format in ['fasta']):
                seqs = SeqIO.parse(input_, file_format)
            # GFF
            if (file_format is 'gff'):
                formatter = cats.formatters.GFFFormatter()

                # Ignore GFFParser induced deprecation warnings
                import warnings
                from Bio import BiopythonDeprecationWarning
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore",
                                          category=BiopythonDeprecationWarning)
                    return formatter.format(input_, **kwargs)
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
    elif isinstance(input_, TextIOWrapper):
        # Input from STDIN
        formatter = cats.formatters.FASTAFormatter()
        return formatter.format(input_, **kwargs)
    else:
        raise UnrecognizedInput

    # Default to SeqRecord formatter
    #formatter = cats.formatters.SeqRecordFormatter()

    return formatter.format(seqs, **kwargs)

