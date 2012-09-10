moref
=====

more-like tool to pretty-print FASTA sequence files.

Screenshot
----------
![moref screenshot](https://raw.github.com/khughitt/moref/master/doc/screenshot.png)

Installation
------------
*pre-requisites*
* [BioPython](http://biopython.org/wiki/Biopython)

*installation:*

    sudo python setup.py install

Usage
-----

Basic usage:

    moref <input file>
    
Some more examples:

    moref --translate -translations-offset -1 sample.fasta
    moref -t -n sample.fasta
    moref -w 80 sample.fasta
    moref --stop-codons 80 sample.fasta
    
You can also pipe the output into less to page through output:
    
    moref sample.fasta | less -FRX
    
TODO
----
1. RNA
2. Seq record range (e.g. moref test.fasta 1 20)
3. Options to highlight/bolden interesting features
4. Built-in mechanism to display x lines at a time? (more/less style)
5. Add option to print available colors
6. Support for specifying offset when highlighting nt stop codons
7. non-fasta input formats
8. simpler customization (e.g. using integers for colors)
