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

    cats sample.fasta | less -FRX

TODO
----
1. RNA
2. Seq record range (e.g. cats test.fasta 1 20)
3. Options to highlight/bolden interesting features
4. Built-in mechanism to display x lines at a time? (more/less style)
5. Add option to print available colors
6. Support for specifying offset when highlighting nt stop codons
7. non-fasta input formats
8. simpler customization (e.g. using integers for colors)
9. Man page

