"""
Miscellaneous utility functions and classes
"""
import os

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
        self.buf = io.StringIO()

        # if coming from a TextIOWrapper, mode will have been lost
        if hasattr(fileobj, 'mode'):
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

