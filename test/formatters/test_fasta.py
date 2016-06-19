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
        ('dna_grep.fasta', 'dna_grep.fasta'),
        ('dna.txt', 'dna.txt'),
        ('dna_grep.txt', 'dna_grep.txt'),
        ('dna_zgrep.txt', 'dna_zgrep.txt'),
        ('rna.txt', 'rna.txt'),
        ('rna_grep.txt', 'rna_grep.txt'),
        ('protein.fasta', 'protein.fasta')
    ])
    def test_format(self, input_file, output_file):
        """Test FASTA formatting"""
        testdir = os.path.abspath(os.path.join(os.getcwd(), 
                                               __file__, '..',  '..'))
        # input
        infile = os.path.join(testdir, 'input', input_file)

        # output
        output = io.StringIO()
        cats.format(infile, outbuffer=output, theme='default')
        output.seek(0)

        with open(os.path.join(testdir, 'output', output_file)) as fp:
            expected = fp.read()
            assert str(output.read()) == expected

    @pytest.mark.parametrize('input_file,output_file', [
        ('dna.fasta', 'dna.fasta-trans')
    ])
    def test_fasta_translate(self, input_file, output_file):
        """Test FASTA DNA->Protein translation"""
        testdir = os.path.abspath(os.path.join(os.getcwd(), 
                                               __file__, '..',  '..'))

        # input
        infile = os.path.join(testdir, 'input', input_file)

        # output
        output = io.StringIO()
        cats.format(infile, outbuffer=output, theme='default', translate=True)
        output.seek(0)

        with open(os.path.join(testdir, 'output', output_file)) as fp:
            expected = fp.read()
            assert str(output.read()) == expected


