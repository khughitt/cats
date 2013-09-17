"""
cats sample data files

Contents
--------
1. 328927009.fasta
   Homo sapiens EGF-like, fibronectin type III and laminin G domains (EGFLAM), 
   transcript variant 5, mRNA
   http://www.ncbi.nlm.nih.gov/nucleotide/328927009

2. transcripts.gff3
   Broad Institute Sample GFF3 file
   http://www.broadinstitute.org/annotation/gebo/help/gff3.html
"""
import os
import cats

__author__ = "Keith Hughitt"
__email__ = "khughitt@umd.edu"

rootdir = os.path.join(os.path.dirname(cats.__file__), "data", "sample") 

# FASTA
FASTA = os.path.abspath(os.path.join(rootdir, '328927009.fasta'))

# GFF
GFF = os.path.abspath(os.path.join(rootdir, 'transcripts.gff3'))

