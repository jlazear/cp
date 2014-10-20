import inspect

import wx
import  wx.lib.scrolledpanel as scrolled


class NoDefault(object):
    def __str__(self):
        return 'NoDefault'


class MainFrame(wx.Frame):
    """
    The main frame that holds all of the others. Really just an
    expandable container for the notebook.
    """
    def __init__(self, controller):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Controller",
                          size=(700, 500))

        self.controller = controller

        # Stores information relevant to executing the command methods with
        # the specified aguments.
        self.cmddict = {}

        self.make_menubar()

        self.panel = scrolled.ScrolledPanel(self)

        self.timer = wx.Timer(self)  # Timer for plot updating
        self.timer.Start(200)  # 200 ms = 5 Hz = 5 fps

        self.bsMain = wx.BoxSizer(wx.VERTICAL)
        self.populate_commands()

        self.panel.SetSizer(self.bsMain)
        self.panel.SetupScrolling()

        self.Layout()

        self.Bind(wx.EVT_CLOSE, self.onClose, self)

    def populate_commands(self):
        """
        Populate the main sizer with the commands specified in the
        controller.
        """
        methodslist = inspect.getmembers(self.controller, inspect.ismethod)
        for name, method in methodslist:
            try:
                if method.command:
                    bCmd = wx.Button(self.panel, wx.ID_ANY, name, size=(150,
                                                                        50))
                    bsCmd, args = self.create_command(method)
                    bsCmd.Prepend(bCmd, 0, wx.EXPAND)
                    bCmd.Bind(wx.EVT_BUTTON, self.onCommand)
                    self.cmddict[name] = args
                    self.bsMain.Add(bsCmd, 0, wx.EXPAND, 5)
                    sl = wx.StaticLine(self.panel, size=(2, 2),
                                       style=wx.LI_HORIZONTAL)
                    self.bsMain.Add(sl, 0, wx.EXPAND, 5)
            except AttributeError:
                pass

    def create_command(self, method):
        bsCmd = wx.BoxSizer(wx.HORIZONTAL)
        arglist = self.make_arglist(method)

        args = {}

        for d in arglist[1:]:
            argname = d['name']
            default = d['default']
            lbl = wx.StaticText(self.panel, wx.ID_ANY, argname,
                                style=wx.ALIGN_CENTER)
            font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
            lbl.SetFont(font)

            txt = wx.TextCtrl(self.panel, wx.ID_ANY, str(default))
            bsArg = wx.BoxSizer(wx.VERTICAL)
            bsArg.Add(lbl, 0, 15)
            bsArg.Add(txt, 0, 15)
            bsCmd.Add(bsArg, 1, wx.ALIGN_CENTER, 6)
            args[argname] = txt
        retdict = {'method': method, 'args': args}
        return bsCmd, retdict

    def make_arglist(self, method):
        """Makes a list of (arg, default) pairs for the method."""
        argspec = method.argspec
        arglist = []
        for i in range(len(argspec.args)):
            arg = argspec.args[-(i+1)]
            try:
                default = argspec.defaults[-(i+1)]
            except IndexError:
                default = NoDefault()
            argdict = {'name': arg, 'default': default}
            arglist.append(argdict)
        arglist.reverse()

        return arglist

    def make_menubar(self):
        self.menuBar = wx.MenuBar()
        self.menus = []

        self.mFile = wx.Menu()
        self.miQuit = self.mFile.Append(wx.ID_EXIT, '&Quit', 'Quit')
        self.menus.append(self.mFile)

        self.menuBar.Append(self.mFile, "&File")

        self.SetMenuBar(self.menuBar)

        self.Bind(wx.EVT_MENU, self.onClose, self.miQuit)

    def onClose(self, event):
        self.app.fGraphFrame.onClose(event)
        self.Destroy()

    # This event handler can't be moved to bindings.py since controls bind to
    # it dynamically as MainFrame is intitialized.
    def onCommand(self, event):
        bCmd = event.GetEventObject()
        name = bCmd.GetLabel()
        cmd = self.cmddict[name]
        method = cmd['method']
        args = cmd['args']
        argdict = {}
        for argname, argctrl in args.items():
            try:
                afunc = method.argdict[argname]['afunc']
            except (AttributeError, KeyError):
                afunc = lambda x: x
            argdict[argname] = afunc(argctrl.GetValue())
        method(**argdict)


