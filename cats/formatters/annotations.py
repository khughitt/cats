"""
Annotation file formatters
"""
class GFFFormatter(object):
    """Formatter for GFF annotation files"""
    def __init__(self, theme):
        """Creates a new GFFFormater instance"""
        self._theme = theme

    def format(self, handler, **kwargs):
        """Format and print GFF file contents"""
        from BCBio import GFF
        from cats.styles import colors
        from io import StringIO

        # string and output buffers
        contents = StringIO()
        output = ""

        # Read contents of file into a string buffer
        contents.write(handler.read())
        contents.seek(0)
        handler.seek(0)
        
        # First print any commments
        last_loc = 0
        line = contents.readline()
        while line.startswith("#"):
            output += colors.WHITE + line
            last_loc = contents.tell()
            line = contents.readline()
        fp.seek(last_loc)

        # Output templates
        #_gene = colors.BLUE + "[%s] %s (%d features)\n"
        #_mrna = colors.CYAN + "%s: %s (%d features)\n"
        #_feat = colors.RED + "%s %d - %d\n"

        # Output file contents, using GFFParser to navigate hierarchy
        for entry in GFF.parse(handler):
            for i, gene in enumerate(entry.features):
                #output += _gene % (gene.type, gene.id, len(gene.sub_features))
                if i % 2 == 0:
                    output += colors.GREEN
                else:
                    output += colors.GREEN_DARK
                output += contents.readline() + colors.RESET

                for mrna in gene.sub_features:
                    #output += _mrna % (mrna.type, mrna.id, 
                    #                   len(mrna.sub_features))
                    output += colors.CYAN + contents.readline()
                    for feature in mrna.sub_features:
                        #loc = feature.location
                        #output += _feat % (feature.type, loc.start, loc.end)
                        output += colors.RED + contents.readline()

        # close file and string handles
        contents.close()

        return output

