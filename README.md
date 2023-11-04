# cats

[![Build Status](https://travis-ci.org/khughitt/cats.svg?branch=master)](https://travis-ci.org/khughitt/cats)

Command-line tool for manipulating and displaying commonly used bioinformatic file formats.

![cats screenshot](https://raw.github.com/khughitt/cats/master/docs/screenshot-grep.png)

# Installation

**Using virtualenv**

First, create a new virtual environment in the desired location, e.g.:

```
python -m venv ~/venv/cats
```

Activate the virtual environment and install the required dependencies:

```
. ~/venv/cats/bin/activate
pip install biopython bcbio-gff
```

Next, clone and install cats:

```
git clone https://github.com/khughitt/cats
cd cats
pip install .
```

**Using conda**

No recipe for cats itself exists yet, but you can still use conda to easily isolate cats and install
the necessary dependencies.

[mamba](https://github.com/mamba-org/mamba) is used in place of conda below, as it is usually
faster when it comes to dependency resolution and downloads:

```
mamba create -n cats --file requirements.txt
mamba activate cats

git clone https://github.com/khughitt/cats
cd cats
pip install .
```

# Usage

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

# Running tests

To run the tests included with cats, install [pytest](https://docs.pytest.org/en/7.4.x/) in the
environment you install cats in run `pytest` from within the cloned cats repo directory.

# Depends on

* [BioPython](http://biopython.org/wiki/Biopython)
* [bcbio-gff](https://github.com/chapmanb/bcbb/tree/master/gff)

