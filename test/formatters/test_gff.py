"""
GFFFormatter tests.
"""
import cats
import io
import os
import pytest

class TestGFFFormatter:
    @pytest.mark.parametrize('filename', [
        'gff3_nested.gff'
    ])
    def test_format(self, filename):
        """Test GFF formatting"""
        testdir = os.path.abspath(os.path.join(os.getcwd(), 
                                               __file__, '..',  '..'))
        # input
        infile = os.path.join(testdir, 'input', filename)

        # output
        output = io.StringIO()
        cats.format(infile, outbuffer=output, theme='default')
        output.seek(0)

        with open(os.path.join(testdir, 'output', filename)) as fp:
            expected = fp.read()
            assert str(output.read()) == expected

