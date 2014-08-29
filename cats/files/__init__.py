"""
File input and output.
"""
def detect_format(filepath, supported_formats):
    """A simple method for determining filetype"""
    import os

    ext = os.path.basename(filepath).split('.').pop().lower()

    # Ignore gzip portion for now
    if filepath.endswith('.gz'):
        filepath.replace('.gz', '')

    # next, check rest of known file types
    for file_format,file_extensions in supported_formats.items():
        if ext in file_extensions:
            return file_format

    # Otherwise raise an exception
    raise UnrecognizedInput("Unsupported file format")
