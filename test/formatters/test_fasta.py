"""
FASTAFormatter tests.
"""
import cats
import io
import os
import pytest

class TestFASTAFormatter:
    def test_format(self):
        # base test directory
        testdir = os.path.abspath(os.path.join( os.getcwd(), __file__, '..',  '..'))

        # output
        output = io.StringIO()
        cats.format(os.path.join(testdir, 'input/dna.fasta'),
                outbuffer=output)
        output.seek(0)

        with open(os.path.join(testdir, 'output/dna.fasta')) as fp:
            expected = fp.read()
            assert str(output.read()) == expected
