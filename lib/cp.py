import inspect
import types
from functools import wraps

# import matplotlib
# matplotlib.interactive(False)
# matplotlib.use('WXAgg')
# import wx
# import  wx.lib.scrolledpanel as scrolled

from lib.gui.app import CPApp


def Controller(cls):
    """
    Specifies that this class will be a controller and starts the GUI when it is
    created.
    """
    @wraps(cls)
    def _controller(*args, **kwargs):
        ctrl = cls(*args, **kwargs)
        global app
        app = CPApp(ctrl)
        app.MainLoop()
    return _controller

def command(f):
    """
    Specifies that the method is to be used as a command.
    """
    f.command = True
    try:
        f.argspec
    except AttributeError:
        f.argspec = inspect.getargspec(f)
    @wraps(f)
    def _command(self, *args, **kwargs):
        return f(self, *args, **kwargs)
    return _command

argfuncdict = {'float': float,
               'string': str,
               'int': int,
               'bool': bool,
               'list': list,
               'dict': dict,
               'eval': eval}

def argument(argname, argtype, **kwargs):
    """
    Specifies how a particular argument should be treated.
    """
    def _decorator(f):
        try:
            f.argspec
        except AttributeError:
            f.argspec = inspect.getargspec(f)
        if isinstance(argtype, types.StringTypes):
            afunc = argfuncdict.get(argtype, str)
        elif callable(argtype):
            afunc = argtype
        arg = {'afunc': afunc}
        arg.update(kwargs)
        try:
            f.argdict[argname] = arg
        except AttributeError:
            f.argdict = {argname: arg}
        @wraps(f)
        def _argument(self, *args, **kwargs):
            return f(self, *args, **kwargs)
        return _argument
    return _decorator

