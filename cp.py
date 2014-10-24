"""
cp.py
jlazear
2014-10-24

Automatic hardware interface GUI creator.

Provides a few simple decorators that may be added to a hardware interface
class and will generate a simple GUI when the class is instantiated. Also
provides a simple plotting utility (built upon pyoscope).

The decorators provided are:

`Controller` -- Decorates the interface class. Responsible for actually
                constructing the GUI and starting the GUI's event loop. No
                GUI is created if the class is not decorated with `Controller`.
`command`    -- Decorates a method of the interface class. Specifies that the
                decorated method should generate a GUI command.
`argument`   -- Decorates a method of the interface class. Specifies how the
                input from the GUI (always in unicode string type) should be
                conditioned before being used as an argument.
`reader`     -- Decorates a method of the interface class. Specifies how the
                data should be read. Must be of a the
                `pyoscope.readers.ReaderInterface` type (may be duck-typed
                rather than subclassed).

Refer to the README or the individual decorators' docstrings for details
about how to use each decorator.

Example:

See `example.py` for an example usage.
"""

import inspect
import types
from functools import wraps

import readers

from gui.app import CPApp


def Controller(cls):
    """
    Specifies that this class will be a controller and starts the GUI when it is
    created.

    :Usage:
        No arguments. Will construct, initialize, and start the GUI once the
        decorated class is instantiated.

    :Example:
        @Controller
        class MyControllerClass(object):
            ...

        >>> mcc = MyControllerClass()
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

    Usage:
        No arguments. Adds some metadata to the method to indicate to the
        `Controller` decorator that this method should generate a GUI
        command. The method's docstring is used as the tooltip for the GUI
        command.

    :Example:
        @Controller
        class MyController(object):
            @command
            def command(self, arg1=1., arg2='a'):
                ...
    """
    f.command = True
    # Check if the argspec has been cached and cache if not yet done
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
               'hex': lambda x: int(x, 16),
               'bool': bool,
               'list': list,
               'dict': dict,
               'eval': eval}


def argument(argname, argtype, **kwargs):
    """
    Specifies how a particular argument should be treated.

    :Usage:
        Requires at least 2 arguments. The first argument specifies the name
        (as a string) of the argument that is to be conditioned. The second
        argument specifies what function will be used to perform the
        conditioning. The second argument may be one of a few valid strings:

            'float' -> float(arg)
            'string' -> str(arg)
            'int' -> int(arg)
            'hex' -> int(arg, 16)
            'bool' -> bool(arg)
            'list' -> list(arg)
            'dict' -> dict(arg)
            'eval' -> eval(arg)

        or a function object. If it is a function object, this object will be
        used as the conditioning function.

        Arguments in a method that do not have a corresponding `argument`
        decorator simply do not condition the argument values before being
        passed into the function.

        Additional keyword arguments may be included. These will simply be
        added to the method's metadata dictionary. The base cp does not
        utilize them.

    :Example:
        @Controller
        class MyController(object):
            @command
            @argument('arg1', 'float')
            @argument('arg2', lambda x: str(int(x**2)))
            def command(self, arg1=1.2, arg2='5'):
                ...
    """
    def _decorator(f):
        # Check if the argspec has been cached and cache if not yet done
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


def reader(readername, *args, **kwargs):
    """
    Specifies what reader should be used to read the output file.

    The GUI attempts to open the output of the decorated method as a file and
    plot the contents of it. It uses the reader to interpret the file. If the
    method's return value does not correspond to a file, the return value is
    simply printed and returned.

    :Usage:
        Requires at least one argument. The first argument may be a string
        specifying which of the built-in `pyoscope` readers should be used.
        Alternatively, it may be a reader class. See
        `pyoscope.readers.ReaderInterface` for what methods the class must
        implement to qualify.

        Subsequent positional and keyword arguments are passed into the reader
        when the reader is instantiated.

    :Example:
        @Controller
        class MyController(object):
            @command
            @argument('arg1', 'hex')
            @argument('arg2', 'hex')
            @reader('HexReader')
            def command1(self, arg1='A', arg2='12FF'):
                with open('testfile.txt', 'a') as f:
                    f.write(' '.join([arg1, arg2]) + '\n')
    """
    def _decorator(f):
        # Check if the argspec has been cached and cache if not yet done
        try:
            f.argspec
        except AttributeError:
            f.argspec = inspect.getargspec(f)
        if isinstance(readername, types.StringTypes):
            readerdict = dict(inspect.getmembers(readers, inspect.isclass))
            readerfunc = readerdict[readername]
        else:
            readerfunc = readername
        arg = {'reader': readerfunc, 'args': args, 'kwargs': kwargs}
        try:
            f.argdict['_reader'] = arg
        except AttributeError:
            f.argdict = {'_reader': arg}
        @wraps(f)
        def _reader(self, *args2, **kwargs2):
            return f(self, *args2, **kwargs2)
        return _reader
    return _decorator
