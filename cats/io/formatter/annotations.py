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

        fp = open(input_file)

        # output buffer
        buffer = ""

        # Output templates
        _gene = colors.BLUE + "[%s] %s (%d features)\n"
        _mrna = colors.CYAN + "%s: %s (%d features)\n"
        _feat = colors.RED + "%s %d - %d\n"

        # parse each entry in GFF file
        for entry in GFF.parse(fp):
            buffer += colors.BLUE_DARK + entry.id + "\n"
            for gene in entry.features:
                buffer += _gene % (gene.type, gene.id, len(gene.sub_features))
                for mrna in gene.sub_features:
                    buffer += _mrna % (mrna.type, mrna.id, 
                                       len(mrna.sub_features))
                    for feature in mrna.sub_features:
                        loc = feature.location
                        buffer += _feat % (feature.type, loc.start, loc.end)

        # close file handle
        fp.close()

        return buffer
