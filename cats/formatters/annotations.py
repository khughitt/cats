"""
Annotation file formatters
"""
class GFFFormatter(object):
    """Formatter for GFF annotation files"""
    def __init__(self, theme):
        """Creates a new GFFFormater instance"""
        self._theme = theme

    def format(self, inbuffer, outbuffer=None, **kwargs):
        """Format and print GFF file contents"""
        from BCBio import GFF
        from cats.styles import colors
        from io import StringIO
        import sys

        # default to STDOUT for output
        if outbuffer is None:
            outbuffer = sys.stdout

        # string and output buffers
        contents = StringIO()

        # two buffers:
        #    contents - used for GFF parser (determine feature type)
        #    inbuffer - used to get original lines for printing

        # Read contents of file into a string buffer
        # contents.write(inbuffer.read().decode())
        contents.write(inbuffer.read())
        contents.seek(0)
        inbuffer.seek(0)
        
        # First print any commments
        last_loc = 0
        line = contents.readline()
        while line.startswith("#"):
            outbuffer.write(colors.WHITE + line)
            last_loc = contents.tell()
            line = contents.readline()
        inbuffer.seek(last_loc)

        # Output templates
        #_gene = colors.BLUE + "[%s] %s (%d features)\n"
        #_mrna = colors.CYAN + "%s: %s (%d features)\n"
        #_feat = colors.RED + "%s %d - %d\n"

        # Output file contents, using GFFParser to navigate hierarchy
        for entry in GFF.parse(inbuffer):
            for i, gene in enumerate(entry.features):
                #outbuffer.write(_gene % (gene.type, gene.id, len(gene.sub_features)))
                if i % 2 == 0:
                    outbuffer.write(colors.GREEN)
                else:
                    outbuffer.write(colors.GREEN_DARK)
                outbuffer.write(contents.readline() + colors.RESET)

                for mrna in gene.sub_features:
                    #outbuffer.write(_mrna % (mrna.type, mrna.id, 
                    #                   len(mrna.sub_features)))
                    outbuffer.write(colors.CYAN + contents.readline())
                    for feature in mrna.sub_features:
                        #loc = feature.location
                        #outbuffer.write(_feat % (feature.type, loc.start, loc.end))
                        outbuffer.write(colors.RED + contents.readline())

        # close file and string handles
        contents.close()

