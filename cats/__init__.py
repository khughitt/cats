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
    from io import BufferedReader
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

    # Formats with variable sequence type
    seq_type_needed = ['fasta', 'fastq']

    # Check input type
    if isinstance(input_, str):
        if os.path.isfile(input_):
            # Open file
            if input_.endswith('.gz'):
                import gzip
                fp = gzip.open(input_, 'rb')
            else:
                fp = open(input_, 'rb')

            # If format specified, check to make sure it is supported
            if ('format' in kwargs and kwargs['format'] not in
                list(supported_formats.keys())):
                    raise UnrecognizedInput("Unsupported file format")

            # Otherwise, attempt to guess format and sequence type if needed
            kwargs['format'] = detect_format(input_, supported_formats)

            if ((kwargs['format'] is None) or (kwargs['format'] in
                    seq_type_needed and 'seq_type' not in kwargs)):
                # Wrap with helper class allow us to guess the type
                file_format,seq_type = _guess_format(fp)

                # Set format and sequence type
                if kwargs['format'] is None:
                    kwargs['format'] = file_format
                if 'seq_type' not in kwargs:
                    kwargs['seq_type'] = seq_type
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
    elif isinstance(input_, BufferedReader):
        # STDIN
        if 'format' not in kwargs or 'seq_type' not in kwargs:
            # wrap with helper class allow us to guess the type
            file_format,seq_type = _guess_format(input_)

            if 'format' not in kwargs:
                kwargs['format'] = file_format
            if 'seq_type' not in kwargs:
                kwargs['seq_type'] = seq_type
        fp = input_
    else:
        raise UnrecognizedInput

    # Sequence string
    if kwargs['format'] == 'sequence_string':
        formatter = cats.formatters.SeqStringFormatter(theme)
        formatter.format(fp, **kwargs)
        if kwargs['_entry_point'] == 'cli':
            sys.exit()

    # FASTA
    if kwargs['format'] == 'fasta':
        # If not translating sequences, use faster FASTAFormatter
        if(not kwargs['translate']):
            formatter = cats.formatters.FASTAFormatter(theme)
            formatter.format(fp, **kwargs)
            if kwargs['_entry_point'] == 'cli':
                sys.exit()
        else:
            # Otherwise use SeqRecord formatter
            seqs = SeqIO.parse(fp, kwargs['format'])
            formatter = cats.formatters.SeqRecordFormatter(theme)
            return formatter.format(seqs, **kwargs)
    # FASTQ
    if (kwargs['format'] in ['fastq']):
        formatter = cats.formatters.FASTQFormatter(theme)
        formatter.format(fp, **kwargs)
        if kwargs['_entry_point'] == 'cli':
            sys.exit()
    # GFF
    if (kwargs['format'] is 'gff'):
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
    lines = handler.peek()[:500].decode().split('\n')

    # FASTQ
    if lines[0].startswith("@"):
        format = ("fastq",)
    elif lines[0].startswith(">"):
        # determine type
        format = ("fasta", _determine_sequence_type(lines[1]))
    elif lines[0].startswith("##gff"):
        format = ("gff",)
    else:
        # check to see if it is a simple sequence string
        seq_type = _determine_sequence_type(lines[0])

        if seq_type not in ['nucleic_acid', 'protein']:
            print("Unrecognized Input:")
            #print(set(escaped))
            #print(str(set(escaped)))
            #fp = open('error.out', 'w')
            #fp.writelines(lines)

            #fp = open('error_escaped.out', 'w')
            #fp.writelines(escaped)
            raise UnrecognizedInput

        format = ("sequence_string", seq_type)

    return format

def _strip_ansi_escapes(string):
    """Removes any grep, etc. associated escape sequences found in a string"""
    import re
    from cats.styles.colors import GREP_HIGHLIGHT_START,GREP_HIGHLIGHT_STOP

    # stripping color-related ansi escape sequences
    # http://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python
    # ansi_escape = re.compile(r'\x1b[^m]*m(\x1b\[K)?')
    # ansi_escape.sub('', x)

    # escape any byte characters resulting from grep
    return(re.sub(GREP_HIGHLIGHT_STOP, '',
                  re.sub(GREP_HIGHLIGHT_START, '', string)).strip())

def _determine_sequence_type(string):
    """Attempts to determine if a sequence is either nucleic acid or protein"""
    escaped = _strip_ansi_escapes(string)

    if set(escaped).issubset(set('AGCTURY')):
        return 'nucleic_acid'
    elif set(escaped).issubset(set('ARNDCQEGHILKMFPSTWYV*')):
        return 'protein'

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

