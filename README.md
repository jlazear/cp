cp
==

Facilitates the automatic generation of a GUI for controlling a hardware 
interface class.

Usage
-----

Provides a few simple decorators that may be added to a hardware interface
class and will generate a simple GUI when the class is instantiated. Also
provides a simple plotting utility (built upon pyoscope).

The decorators provided are:

- `Controller` -- Decorates the interface class. Responsible for actually
                  constructing the GUI and starting the GUI's event loop. No
                  GUI is created if the class is not decorated with 
                  `Controller`.
- `command`    -- Decorates a method of the interface class. Specifies that the
                  decorated method should generate a GUI command.
- `argument`   -- Decorates a method of the interface class. Specifies how the
                  input from the GUI (always in unicode string type) should be
                  conditioned before being used as an argument.
- `reader`     -- Decorates a method of the interface class. Specifies how the
                  data should be read. Must be of a the
                  `pyoscope.readers.ReaderInterface` type (may be duck-typed
                  rather than subclassed).


Example
-------

    from cp import Controller, command


    @Controller
    class Ctrl(object):
        @command
        def cmd1(self, arg1=1, arg2='5'):
            with open('cmd1.txt', 'a') as f:
                f.write('{0} {1}\r\n'.format(arg1, arg2))
            return 'cmd1.txt'


Installation
------------

Install directly from GitHub using `pip` with

    pip install git+git://github.com/jlazear/cp.git
    
This will install the PyPI version of 
[`pyoscope`](https://github.com/jlazear/pyoscope). The GitHub version of 
`pyoscope` may be installed directly from GitHub with  

    pip install git+git://github.com/jlazear/pyoscope.git
    
Note that `cp` requires [wxPython](http://www.wxpython.org). `pip` will 
attempt to install it, but you're probaby on your own for actually getting it
 to work.  

Author
------
Justin Lazear

jlazear@gmail.com

10/24/14