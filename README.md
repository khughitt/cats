cats
====

pretty print and other basic manipulations for sequence data.

Screenshot

----------
![cats screenshot](https://raw.github.com/khughitt/cats/master/doc/screenshot.png)

Installation

------------
*pre-requisites*
* [BioPython](http://biopython.org/wiki/Biopython)
* [bcbio-gff](https://github.com/chapmanb/bcbb/tree/master/gff)

*installation:*

    sudo python setup.py install

Usage
-----

Basic usage:

    cats <input file>

Some more examples:

    cats --translate -translations-offset -1 sample.fasta
    cats -t -n sample.fasta
    cats -w 80 sample.fasta
    cats --stop-codons 80 sample.fasta

You can also pipe the output into less to page through output:

    cats sample.fasta | less

Or grep for an interesting feature and pipe the output into cats:

    grep --color='always' "AAUAA" input.fastq | cats

Gzipped files are also supported:

    zgrep --color='always' "AAAAA$" input.fastq.gz | cats

TODO
----
1. RNA
2. Seq record range (e.g. cats test.fasta 1 20)
3. Options to highlight/bolden interesting features
4. Built-in mechanism to display x lines at a time? (more/less style)
5. Add option to print available colors
6. Support for specifying offset when highlighting nt stop codons
7. simpler customization (e.g. using integers for colors)
8. Man page
9. Fix GFF parsing and switch to parsing stdin directly instead of using
   the GFF parse to avoid having to read entire file at once.
10. Add color themes modelled after popular software/conventions.
11. Add unit tests to cover types of input, output, etc. (use a set color theme
    to ensure consistency between test runs)
12. Add option to show quality scores as a color bar (e.g. red => green)

