"""
FASTAFormatter tests.
"""
import cats
import io
import os
import pytest

class TestFASTAFormatter:
    @pytest.mark.parametrize('input_file,output_file', [
        ('dna.fasta', 'dna.fasta'),
        ('dna_grep1.fasta', 'dna_grep1.fasta'),
        ('dna_grep2.fasta', 'dna_grep2.fasta'),
        ('dna_grep3.fasta', 'dna_grep3.fasta')
    ])

    def test_format(self, input_file, output_file):
        """Test FASTA formatting"""
        testdir = os.path.abspath(os.path.join(os.getcwd(), 
                                               __file__, '..',  '..'))
        # input
        infile = os.path.join(testdir, 'input', input_file)

        # output
        output = io.StringIO()
        cats.format(infile, outbuffer=output)
        output.seek(0)

        with open(os.path.join(testdir, 'output', output_file)) as fp:
            expected = fp.read()
            assert str(output.read()) == expected

