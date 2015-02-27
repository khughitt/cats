"""
cats
"""
__version__ = 0.3

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

    # Load config
    if '_config_loaded' not in kwargs:
        config = _load_config()
        config.update(kwargs)
        kwargs = config

    # Theme to use
    theme = kwargs['theme']
    
    # Supported file formats
    supported_formats = {
        'fasta': ['fa', 'fasta'],
        'fastq': ['fastq'],
        'gff': ['gff', 'gtf', 'gff3']
    }

    # Check input type
    if isinstance(input_, str):
        if os.path.isfile(input_):
            # Open file
            if input_.endswith('.gz'):
                import gzip
                fp = gzip.open(input_, 'rb')
            else:
                fp = open(input_)

            # Determine file type to use
            if 'format' not in kwargs:
                file_format = detect_format(input_, supported_formats)

                # if file extension is not recognized, attempt to guess format
                if file_format is None:
                    # wrap with helper class allow us to guess the type
                    from .util import Peeker
                    fp = Peeker(fp)
                    file_format = _guess_format(fp)
            else:
                file_format = kwargs['format']

                if file_format not in list(supported_formats.keys()):
                    raise UnrecognizedInput("Unsupported file format")

        else:
            # Sequence string
            try:
                seqs = [SeqRecord.SeqRecord(
                           Seq.Seq(input_, IUPAC.IUPACUnambiguousDNA()))]
                formatter = cats.formatters.SeqRecordFormatter(theme)
                return formatter.format(seqs, **kwargs)
            except:
                raise UnrecognizedInput
    elif isinstance(input_, SeqRecord.SeqRecord):
        # SeqRecord
        formatter = cats.formatters.SeqRecordFormatter(theme)
        return formatter.format([input_], **kwargs)
    elif isinstance(input_, Seq.Seq):
        # Seq
        formatter = cats.formatters.SeqRecordFormatter(theme)
        return formatter.format([SeqRecord.SeqRecord(input_)], **kwargs)
    elif isinstance(input_, TextIOWrapper):
        # STDIN
        if 'format' in kwargs:
            file_format = kwargs['format']
        else:
            # wrap with helper class allow us to guess the type
            from .util import Peeker
            input_ = Peeker(input_)
            file_format = _guess_format(input_)
        fp = input_
    else:
        raise UnrecognizedInput

    # Sequence string
    if (file_format in ['nucleic_acid_string', 'amino_acid_string']):
        formatter = cats.formatters.SeqStringFormatter(theme)
        formatter.format(fp, **kwargs)
        if kwargs['_entry_point'] == 'cli':
            sys.exit()

    # FASTA
    if (file_format in ['fasta']):
        # If not translating sequences, use faster FASTAFormatter
        if(not kwargs['translate']):
            formatter = cats.formatters.FASTAFormatter(theme)
            formatter.format(fp, **kwargs)
            if kwargs['_entry_point'] == 'cli':
                sys.exit()
        else:
            # Otherwise use SeqRecord formatter
            seqs = SeqIO.parse(fp, file_format)
            formatter = cats.formatters.SeqRecordFormatter(theme)
            return formatter.format(seqs, **kwargs)
    # FASTQ
    if (file_format in ['fastq']):
        formatter = cats.formatters.FASTQFormatter(theme)
        formatter.format(fp, **kwargs)
        if kwargs['_entry_point'] == 'cli':
            sys.exit()
    # GFF
    if (file_format is 'gff'):
        formatter = cats.formatters.GFFFormatter(theme)

        # Ignore GFFParser induced deprecation warnings
        import warnings
        from Bio import BiopythonDeprecationWarning
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore",
                                    category=BiopythonDeprecationWarning)
            return formatter.format(fp, **kwargs)

def _guess_format(handler):
    """
    Attempts to guess the input stream type from some common formats.
    
    This is very basic at the moment and will need to be improved as more
    varied formats are encountered.
    """

    # Grab few first lines
    lines = [handler.peekline() for x in range(3)]

    # FASTQ
    if lines[0].startswith("@"):
        format = "fastq"
    elif lines[0].startswith(">"):
        format = "fasta"
    elif lines[0].startswith("##gff"):
        format.co= "gff"
    else:
        import re
        from cats.styles.colors import GREP_HIGHLIGHT_START,GREP_HIGHLIGHT_STOP

        # escape any byte characters resulting from grep
        escaped = re.sub(GREP_HIGHLIGHT_STOP, '',
                         re.sub(GREP_HIGHLIGHT_START, '', lines[0])).strip()

        # check to see if it is a simple sequence string

        # DEBUGGING
        # zgrep -e
        #In [2]: x = fp.read()

        #In [3]: set(x)
        #Out[3]: {'\n', '\x1b', '0', '1', '2', '3', ';', 'A', 'C', 'G', 'K', 'T', '[', 'm'}

        # grep
        #In [4]: fp2 = open('/home/keith/test.grep')

        #In [5]: x2 = fp2.read()

        #In [6]: set(x2)
        #Out[6]: {'\n', '\x1b', '1', '2', '3', ';', 'A', 'C', 'G', 'K', 'T', '[', 'm

        if set(escaped).issubset(set('AGCTURY')):
            format = 'nucleic_acid_string'
        elif set(escaped).issubset(set('ARNDCQEGHILKMFPSTWYV*')):
            format = 'amino_acid_string'
        else:
            print("Unrecognized Input:")
            #print(set(escaped))
            #print(str(set(escaped)))
            #fp = open('error.out', 'w')
            #fp.writelines(lines)

            #fp = open('error_escaped.out', 'w')
            #fp.writelines(escaped)
            raise UnrecognizedInput

    return format

def _load_config(entry_point='library'):
    """Loads user configuration if one exists"""
    import os
    import configparser

    # Default configuration options
    config = _defaults()
    config['_entry_point'] = entry_point

    # Load config file if it exists
    config_file = os.path.expanduser("~/.catsrc")

    if os.path.isfile(config_file):
        parser = configparser.ConfigParser()
        parser.read(config_file)

        config.update(dict(parser['general']))

    return config

# Default options
def _defaults():
    """Gets a dictionary of default options"""
    return {
        "color": True,
        "start_codons": False,
        "stop_codons": False,
        "translate": False,
        "cpg": False,
        "translation_table": 1,
        "translation_frame": 1,
        "line_width": 70,
        "theme": "default",
        "_config_loaded": True
    }

