"""
A test file.
"""
from lib import Controller, command, argument


@Controller
class Ctrl(object):

    @command
    @argument('arg1', 'int')
    @argument('arg2', str)
    def cmd1(self, arg1=1, arg2='b'):
        print "cmd1: {0} {1}".format(repr(arg1), repr(arg2))

    @command
    @argument('third', 'float')
    def cmd2(self, arg1=10, arg2='BB', third=3.14):
        print "cmd2: {0} {1} {2}".format(repr(arg1), repr(arg2), repr(third))

    @command
    def cmd3(self, firstreq, secondreq, third=3.14):
        print "cmd3: {0} {1} {2}".format(repr(firstreq), repr(secondreq),
                                         repr(third))


if __name__ == "__main__":
    ctrl = Ctrl()