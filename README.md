cats
====

[![Build Status](https://travis-ci.org/khughitt/cats.svg?branch=master)](https://travis-ci.org/khughitt/cats)

Command-line tool for manipulating and displaying commonly used bioinformatic file formats.

Screenshot
----------

![cats screenshot](https://raw.github.com/khughitt/cats/master/docs/screenshot-grep.png)

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

Gzipped files are also supported, using zgrep:

    zgrep --color='always' "AAAAA$" input.fastq.gz | cats

