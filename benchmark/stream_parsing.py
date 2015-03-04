#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Stream parsing benchmark
Keith (03/04/2015)

The purpose of this benchmark is compare the performance of different
approaches for handling input streams of various types.

Two methods will be compared, both of which are capable of dealing with file
and STDIN streams, and provide lookahead capabilities.

In some simple testing, it appears that the built-in BufferedReader class for
which sys.stdin.buffer and the file handler are both instances, the peek
function returns 4096 bytes at a time, which must then be decoded. Since this
is much more than what is needed to detect the filetype, this may be overkill.
The Peeker class attempts to get around this by only returning what is needed,
at the cost of some additional overhead.

Results
-------

For both STDIN and file stream parsing, the built-in classes were about twice
as fast as using the Peeker. Tested with Python 3.4.3.

"""
import sys
import io
import os
import string
import time
import timeit
import random

def main():
    """Main"""
    # number and length of lines in test file
    NUM_LINES = 1000
    LINE_LENGTH = 80

    # First, generate a test file
    with open('test_input.txt', 'w') as fp:
        for i in range(NUM_LINES):
            fp.write("".join(random.sample(string.ascii_letters * 2,
                                           LINE_LENGTH)) + "\n")

    # If STDIN specified, compare performance for parsing STDIN
    # Since the stdin buffer does not support seeking, it is not possible
    # to use timeit to benchmark this. Instead a single time will be
    # provided and it should be rerun from the shell multiple times to
    # compare performance
    if not sys.stdin.isatty():
        # Test 1
        #timeit.timeit(s)
        #timeit.timeit("peeker_test()", setup='from __main__ import peeker_test')

        #builtin_stdin_test()
        peeker_stdin_test()
    else:
        # Otherwise, compare performance for reading files
        t = timeit.timeit("builtin_file_test()", 
                          setup='from __main__ import builtin_file_test')
        print("Built-in file stream test (1,000,000 reps): %f" % t)

        t = timeit.timeit("peeker_file_test()", 
                          setup='from __main__ import Peeker,peeker_file_test')
        print("Peeker file stream test (1,000,000 reps): %f" % t)
        
def builtin_file_test():
    fp = open('test_input.txt', 'rb')
    trash = fp.peek()[:300].decode()
    trash = fp.read().decode()

def peeker_file_test():
    fp = open('test_input.txt')
    x = Peeker(fp)
    trash = [x.peekline() for i in range(3)]
    trash = x.read()

def builtin_stdin_test():
    t1 = time.time()
    x = sys.stdin.buffer
    trash = x.peek()[:300]
    trash = x.read()
    t2 = time.time()

    print("Built-in STDIN performance: %f" % (t2 - t1))

def peeker_stdin_test():
    t1 = time.time()
    x = Peeker(sys.stdin)
    trash = [x.peekline() for i in range(3)]
    trash = x.read()
    t2 = time.time()

    print("Peeker STDIN performance: %f" % (t2 - t1))

class Peeker(object):
    """
    IO Stream peeker.

    A wrapper around sys.stdin and other streams to enable peeking at the
    stream contents.

    Source: http://stackoverflow.com/questions/14283025/python-3-reading-bytes-from-stdin-pipe-with-readahead
    """
    def __init__(self, fileobj):
        import io
        self.fileobj = fileobj
        #self.buf = io.BytesIO()
        self.buf = io.StringIO()

        self.mode = self.fileobj.mode
        self.name = self.fileobj.name

    def _append_to_buf(self, contents):
        oldpos = self.buf.tell()
        self.buf.seek(0, os.SEEK_END)
        self.buf.write(contents)
        self.buf.seek(oldpos)

    def __iter__(self):
        return self

    def __next__(self):
        line = self.readline()
        if line == '':
            raise StopIteration
        else:
            return line

    def peek(self, size):
        contents = self.fileobj.read(size)
        self._append_to_buf(contents)
        return contents

    def peekline(self):
        contents = self.fileobj.readline()
        self._append_to_buf(contents)
        return contents

    def read(self, size=None):
        if size is None:
            return self.buf.read() + self.fileobj.read()
        contents = self.buf.read(size)
        if len(contents) < size:
            contents += self.fileobj.read(size - len(contents))
        return contents

    def readable(self):
        return self.fileobj.readable()

    def readline(self):
        line = self.buf.readline()
        if not line.endswith('\n'):
            line += self.fileobj.readline()
        return line

    def seekable(self):
        return self.fileobj.seekable()

if __name__ == "__main__":
    main()

