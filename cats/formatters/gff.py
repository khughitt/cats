"""
GFF formatter
"""
class GFFFormatter(object):
    """Formatter for GFF files"""
    def __init__(self, theme):
        """Creates a new GFFFormatter instance"""
        # load theme
        import sys

        theme_module = 'cats.styles.themes.%s' % theme
        __import__(theme_module)
        self._theme = sys.modules[theme_module]

    def format(self, inbuffer, outbuffer=None, **kwargs):
        """Format sequence records"""
        import sys
        from cats.styles import colors

        # default/bold text
        RESET = '\033[0m'
        BOLD = '\033[1m'

        # default to STDOUT for output
        if outbuffer is None:
            outbuffer = sys.stdout

        # if not color desired, print as-is
        if not kwargs['color']:
            outbuffer.write(inbuffer.read().decode())
            return

        # Iterate through and format each sequence record
        for line in inbuffer:
            line = line.decode()

            # Reset formatting
            outbuffer.write(RESET)
    
            # Print comment / metadata
            if line.startswith("#"):
                # Comment
                outbuffer.write(self._theme.gff_colors['meta'] + line)
                continue

            # Select colors for entry
            if '\toperon\t' in line or '\tchromosome\t' in line:
                cols = [self._theme.gff_colors['1a'], self._theme.gff_colors['1b']]
            elif '\tgene\t' in line:
                cols = [self._theme.gff_colors['2a'], self._theme.gff_colors['2b']]
            elif '\tmRNA\t' in line:
                cols = [self._theme.gff_colors['3a'], self._theme.gff_colors['3b']]
            elif '\tCDS\t' in line:
                cols = [self._theme.gff_colors['4a'], self._theme.gff_colors['4b']]
            elif '\texon\t' in line:
                cols = [self._theme.gff_colors['5a'], self._theme.gff_colors['5b']]
            else:
                cols = [self._theme.gff_colors['6a'], self._theme.gff_colors['6b']]

            # Print fields across line
            fields = line.split('\t')

            for i,field in enumerate(fields):
                if i % 2 == 0:
                    outbuffer.write(cols[1] + field)
                else:
                    outbuffer.write(cols[0] + field)
                if i < len(fields) - 1:
                    outbuffer.write('\t')

