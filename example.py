"""
An example file demonstrating the basic functionality of cp.
"""
import os

from lib import Controller, command, argument, reader


@Controller
class Ctrl(object):
    def __init__(self):
        fnames = ['cmd1.txt', 'cmd2.txt', 'cmd3.txt', 'hi_paul.txt']
        for fname in fnames:
            try:
                os.remove(fname)
            except OSError:
                pass

    @command
    @reader('HexReader')
    def cmd1(self, arg1=1, arg2='5'):
        """cmd1's docstring!"""
        print "cmd1: {0} {1}".format(repr(arg1), repr(arg2))
        fname = 'cmd1.txt'
        self.dec_write(fname, [arg1, arg2], append=True)
        return fname

    @command
    def cmd2(self, arg1=10, arg2=512, third=314):
        print "cmd2: {0} {1} {2}".format(repr(arg1), repr(arg2), repr(third))
        fname = 'cmd2.txt'
        self.dec_write(fname, [arg1, arg2, third], append=True)
        return fname

    @command
    def cmd3(self, firstreq, secondreq, third=3.14):
        """cmd3 docstring
        blah blah blah


        blah
        """
        print "cmd3: {0} {1} {2}".format(repr(firstreq), repr(secondreq),
                                         repr(third))
        fname = 'cmd3.txt'
        return fname

    def hex_write(self, fname, values, append=False):
        fmtstr = "{0:04X}"
        hexstrvals = [fmtstr.format(int(val)) for val in values]
        towrite = ' '.join(hexstrvals) + '\n'
        fmt = 'a' if append else 'w'
        with open(fname, fmt) as f:
            f.write(towrite)

    def dec_write(self, fname, values, append=False):
        fmtstr = "{0:04}"
        decstrvalues = [fmtstr.format(int(val)) for val in values]
        towrite = ', '.join(decstrvalues) + '\n'
        fmt = 'a' if append else 'w'
        with open(fname, fmt) as f:
            f.write(towrite)



if __name__ == "__main__":
    ctrl = Ctrl()