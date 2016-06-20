"""
GFF formatter
"""
class GFFFormatter(object):
    """Formatter for GFF files"""
    def __init__(self, theme):
        """Creates a new GFFFormatter instance"""
        self._theme = theme

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
    
            # Print comment
            if line.startswith("#"):
                # Comment
                outbuffer.write(colors.WHITE + line)
                continue

            # Select colors for entry
            if '\tgene\t' in line:
                cols = [colors.BLUE_DARK, colors.BLUE]
            elif '\tmRNA\t' in line:
                cols = [colors.YELLOW_DARK, colors.YELLOW]
            elif '\tCDS\t' in line:
                cols = [colors.MAGENTA_DARK, colors.MAGENTA]
            else:
                cols = [colors.GREEN_DARK, colors.GREEN]

            # Print fields across line
            fields = line.split('\t')

            for i,field in enumerate(fields):
                if i % 2 == 0:
                    outbuffer.write(cols[1] + field)
                else:
                    outbuffer.write(cols[0] + field)
                if i < len(fields) - 1:
                    outbuffer.write('\t')

