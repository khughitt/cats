"""
Annotation file formatters
"""
class GFFFormatter(object):
    """Formatter for GFF annotation files"""
    def __init__(self):
        """Creates a new GFFFormater instance"""
        pass

    def format(self, input_file, **kwargs):
        """Format and print GFF file contents"""
        from BCBio import GFF
        from cats.styles import colors
        from io import StringIO

        fp = open(input_file)

        # string and output buffers
        contents = StringIO()
        output = ""

        # Read contents of file into a string buffer
        contents.write(fp.read())
        contents.seek(0)
        fp.seek(0)

        # Output templates
        #_gene = colors.BLUE + "[%s] %s (%d features)\n"
        #_mrna = colors.CYAN + "%s: %s (%d features)\n"
        #_feat = colors.RED + "%s %d - %d\n"

        # Output file contents, using GFFParser to navigate hierarchy
        for entry in GFF.parse(fp):
            for gene in entry.features:
                #output += _gene % (gene.type, gene.id, len(gene.sub_features))
                output += colors.BLUE + contents.readline()
                for mrna in gene.sub_features:
                    #output += _mrna % (mrna.type, mrna.id, 
                    #                   len(mrna.sub_features))
                    output += colors.CYAN + contents.readline()
                    for feature in mrna.sub_features:
                        #loc = feature.location
                        #output += _feat % (feature.type, loc.start, loc.end)
                        output += colors.RED + contents.readline()

        # close file and string handles
        fp.close()
        contents.close()

        return output

