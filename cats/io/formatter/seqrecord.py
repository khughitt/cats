"""
SeqRecord formatter.
"""
class SeqRecordFormatter(object):
    """Formatter for BioPython SeqRecord objects"""
    def __init__(self):
        """Creates a new SeqRecordFormatter instance"""
        import os
        from cats.styles.nucleic_acid import dna
        from cats.styles.protein import amino_acid

        # Store mappings
        self.dna = dna
        self.amino_acid = amino_acid

        # Use custom colors if specified
        config_file = os.path.expanduser("~/.catsrc")

        if os.path.isfile(config_file):
            # read config file
            import ConfigParser
            config = ConfigParser.ConfigParser()
            config.read(config_file)

            # override color choices
            for k,v in config.items('dna'):
                mod_color = "\033%s%s" % (v, k.upper())
                self.dna[k.upper()] = mod_color

            return

    def format(self, seqs, **kwargs):
        """Format sequence records"""
        # start/stop codons
        stop_template = '\033[0;041m\033[1;038m%s\033[0m'

        stop_codons = {
            "TAG": stop_template % "TAG",
            "TAA": stop_template % "TAA",
            "TGA": stop_template % "TGA"
        }

        # for x in range(1,10):
        # print "\033[03%dmTEST   \033[09%dmTEST" % (x,x)

        # bold text
        reset = '\033[0m'
        bold = '\033[1m'

        # For now only display amino acids when translate requested
        # @TODO: automatically detect/allow user to specify
        if kwargs['translate']:
            # determine frame to use
            frame = abs(kwargs['translation_frame']) - 1

            # select translation table
            # see: ftp://ftp.ncbi.nlm.nih.gov/entrez/misc/data/gc.prt

            # print without colors
            if not kwargs['color']:
                for seq in seqs:
                    print(">" + seq.description)
                    # forward frames
                    if kwargs['translation_frame'] > 0:
                        translated = str(seq.seq[frame:].translate(
                            table=kwargs['translation_table'])
                    )
                    # complemented frames
                    else:
                        reverse_comp = seq.seq.reverse_complement()[frame:]
                        translated = str(reverse_comp.translate(
                            table=kwargs['translation_table'])
                        )
                    print("\n".join(textwrap.wrap(translated, kwargs['line_width'])))
            else:
                # Amino Acids
                for seq in seqs:
                    pretty = reset

                    # Print description
                    print(bold + ">" + seq.description)

                    # print seq.seq[frame:]
                    # Translate and add stylized residues to otput string
                    if kwargs['translation_frame'] > 0:
                        translated = seq.seq[frame:].translate(
                            table=kwargs['translation_table']
                        )
                    else:
                        reverse_comp = seq.seq.reverse_complement()[frame:]
                        translated = str(reverse_comp.translate(
                            table=kwargs['translation_table']
                        ))

                    for i, residue in enumerate(translated, start=1):
                         pretty += self.amino_acid[residue]
                         # Add new lines to ensure desired line width
                         if i % kwargs['line_width'] == 0:
                             pretty += "\n"

                    print(pretty)
        else:
            # Nuceotides
            # loop through and print seqs
            # @NOTE - could pause here after each record if desired
            if not kwargs['color']:
                for seq in seqs:
                    print(">" + seq.description)
                    print(seq.seq)
            else:
                for seq in seqs:
                    print(bold + ">" + seq.description)

                    # For DNA, read bases three at a time
                    # For now, assume reading frame starts from index 0
                    pretty = reset
                    for codon in self._chunks(seq.seq, 3):
                        # If stop codon is encountered, highlight it
                        if kwargs['stop_codons'] and str(codon) in stop_codons:
                            pretty += stop_codons[str(codon)]

                        # otherwise add colored bases
                        else:
                            for letter in codon:
                                pretty += self.dna[letter]

                    # Highlight CpG dinucleotides
                    if kwargs['cpg']:
                        pretty = pretty.replace(self.dna['C'] + self.dna['G'],
                                                '\033[0;044m\033[1;038mCG\033[0m')

                    print(pretty)

    def _chunks(self, seq, n):
        """Yield successive n-sized chunks from seq."""
        for i in range(0, len(seq), n):
            yield seq[i:i + n]

class UnrecognizedInput(IOError):
    """Unrecognized input error"""
    pass
