"""
cats - text formatting
"""
def format(input_, color=True, line_width=80, **kwargs):
    """Formats the target sequence"""
    import os
    import textwrap
    from Bio import SeqIO
    from Bio import Seq, SeqRecord
    from Bio.Alphabet import IUPAC
    from cats.io.file import detect_format
    from cats.styles.nucleic_acid import dna
    from cats.styles.protein import amino_acid

    # Check input type
    if isinstance(input_, basestring):
        if os.path.isfile(input_):
            file_format = detect_format(input_)
            seqs = SeqIO.parse(input_, file_format)
        else:
            # Sequence string?
            try:
                seqs = [SeqRecord.SeqRecord(
                           Seq.Seq(input_, IUPAC.IUPACUnambiguousDNA()))]
            except:
                raise UnrecognizedInput

    elif isinstance(input_, SeqRecord.SeqRecord):
        seqs = [input_]
    elif isinstance(input_, Seq.Seq):
        seqs = [SeqRecord.SeqRecord(input_)]
    else:
        raise UnrecognizedInput

    # Use custom colors if specified
    config_file = os.path.expanduser("~/.catsrc")
    if os.path.isfile(config_file):
        # read config file
        import ConfigParser
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        #config.readfp(open(config_file, 'r+'))

        # override color choices
        for k,v in config.items('dna'):
            mod_color = "\033%s%s" % (v, k.upper())
            dna[k.upper()] = mod_color

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
    if args['translate']:
        # determine frame to use
        frame = abs(args['translation_frame']) - 1

        # select translation table
        # see: ftp://ftp.ncbi.nlm.nih.gov/entrez/misc/data/gc.prt

        # print without colors
        if args['no_color']:
            for seq in seqs:
                print(">" + seq.description)
                # forward frames
                if args['translation_frame'] > 0:
                    translated = str(seq.seq[frame:].translate(
                        table=args['translation_table'])
                )
                # complemented frames
                else:
                    reverse_comp = seq.seq.reverse_complement()[frame:]
                    translated = str(reverse_comp.translate(
                        table=args['translation_table'])
                    )
                print("\n".join(textwrap.wrap(translated, args['line_width'])))
        else:
            # Amino Acids
            for seq in seqs:
                pretty = reset

                # Print description
                print(bold + ">" + seq.description)

                # print seq.seq[frame:]
                # Translate and add stylized residues to otput string
                if args['translation_frame'] > 0:
                    translated = seq.seq[frame:].translate(
                        table=args['translation_table']
                    )
                else:
                    reverse_comp = seq.seq.reverse_complement()[frame:]
                    translated = str(reverse_comp.translate(
                        table=args['translation_table']
                    ))

                for i, residue in enumerate(translated, start=1):
                     pretty += amino_acid[residue]
                     # Add new lines to ensure desired line width
                     if i % args['line_width'] == 0:
                         pretty += "\n"

                print(pretty)
    else:
        # Nuceotides
        # loop through and print seqs
        # @NOTE - could pause here after each record if desired
        if args['no_color']:
            for seq in seqs:
                print(">" + seq.description)
                print(seq.seq)
        else:
            for seq in seqs:
                print(bold + ">" + seq.description)

                # For DNA, read bases three at a time
                # For now, assume reading frame starts from index 0
                pretty = reset
                for codon in _chunks(seq.seq, 3):
                    # If stop codon is encountered, highlight it
                    if args['stop_codons'] and str(codon) in stop_codons:
                        pretty += stop_codons[str(codon)]

                    # otherwise add colored bases
                    else:
                        for letter in codon:
                            pretty += dna[letter]

                # Highlight CpG dinucleotides
                if args['cpg']:
                    pretty = pretty.replace(dna['C'] + dna['G'],
                                            '\033[0;044m\033[1;038mCG\033[0m')

                print(pretty)

def _chunks(seq, n):
    """Yield successive n-sized chunks from seq."""
    for i in range(0, len(seq), n):
        yield seq[i:i + n]

class UnrecognizedInput(IOError):
    """Unrecognized input error"""
    pass
