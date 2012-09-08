moref
=====

more-like tool to pretty-print FASTA sequence files.

Installation
------------
moref depends on the BioPython, which can be installed using pip, e.g.:

    sudo pip install biopython

Next, install moref using the standard setup.py installation:

    sudo python setup.py install
    
Done!

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