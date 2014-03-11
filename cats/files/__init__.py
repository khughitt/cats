"""
File input and output.
"""
def detect_format(filepath):
    """A simple method for determining filetype"""
    import os

    # File extensions
    mapping = {
        'fasta': ['fa', 'fasta'],
        'fastq': ['fastq'],
        'gff': ['gff', 'gff3']
    }

    ext = os.path.basename(filepath).split('.').pop().lower()

    # first check for .fastq.gz
    if filepath.endswith('.fastq.gz'):
        return 'fastq'

    # next, check rest of known file types
    for file_format,file_extensions in mapping.items():
        if ext in file_extensions:
            return file_format

    # Otherwise raise an exception
    raise UnrecognizedInput("Unsupported file format")
