"""
cats
"""
__version__ = 0.2

import cats.styles
import cats.data
import cats.formatters

def format(input_, *args, **kwargs):
    """Formats bioinformatics related data for display on the console."""
    import os
    import sys
    from io import TextIOWrapper
    from Bio import SeqIO
    from Bio import Seq, SeqRecord
    from Bio.Alphabet import IUPAC
    from cats.files import detect_format

    # Check input type
    if isinstance(input_, basestring):
        if os.path.isfile(input_):
            file_format = detect_format(input_)

            # FASTA
            if (file_format in ['fasta']):
                # If not translating sequences, use faster FASTAFormatter
                if(not kwargs['translate']):
                    formatter = cats.formatters.FASTAFormatter()
                    formatter.format(open(input_), **kwargs)
                    sys.exit()
                else:
                    # Otherwise use SeqRecord formatter
                    seqs = SeqIO.parse(input_, file_format)
                    formatter = cats.formatters.SeqRecordFormatter()
                    return formatter.format(seqs, **kwargs)
            # FASTQ
            if (file_format in ['fastq']):
                formatter = cats.formatters.FASTQFormatter()
                if input_.endswith('.gz'):
                    import gzip
                    fp = gzip.open(input_, 'rb')
                else:
                    fp = open(input_)
                formatter.format(fp, **kwargs)
                sys.exit()
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
            # Sequence string
            try:
                seqs = [SeqRecord.SeqRecord(
                           Seq.Seq(input_, IUPAC.IUPACUnambiguousDNA()))]
                formatter = cats.formatters.SeqRecordFormatter()
                return formatter.format(seqs, **kwargs)
            except:
                raise UnrecognizedInput
    elif isinstance(input_, SeqRecord.SeqRecord):
        # SeqRecord
        formatter = cats.formatters.SeqRecordFormatter()
        return formatter.format([input_], **kwargs)
    elif isinstance(input_, Seq.Seq):
        # Seq
        formatter = cats.formatters.SeqRecordFormatter()
        return formatter.format([SeqRecord.SeqRecord(input_)], **kwargs)
    elif isinstance(input_, TextIOWrapper):
        # STDIN
        formatter = cats.formatters.FASTAFormatter()
        return formatter.format(input_, **kwargs)
    else:
        raise UnrecognizedInput

