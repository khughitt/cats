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

    moref <input file>
    
You can also pipe the output into less to page through output:
    
    moref sample.fasta | less -FRX
    
TODO
----
1. RNA/Proteins
2. Translations
3. Seq record range (e.g. moref test.fasta 1 20)
4. Options to highlight/bolden interesting features
5. Built-in mechanism to display x lines at a time? (more/less style)