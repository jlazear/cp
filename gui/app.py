import matplotlib
matplotlib.interactive(False)
matplotlib.use('WXAgg')

import wx

from pyoscope import PyOscope
from gui.mainframe import MainFrame
from gui.graphframe import GraphFrame
from gui.bindings import Binder

from wx.lib.mixins.inspection import InspectionMixin  #DELME


class CPApp(wx.App, InspectionMixin):
    def __init__(self, controller):
        self.controller = controller
        wx.App.__init__(self)

    def OnInit(self):
        self.Init()  #DELME For InspectionMixin

        # Make the MainFrame
        fMainFrame = MainFrame(self.controller)
        fMainFrame.Show()
        self.SetTopWindow(fMainFrame)
        self.fMainFrame = fMainFrame

        # Make the GraphFrame
        fGraphFrame = GraphFrame()
        fGraphFrame.Show()
        self.fGraphFrame = fGraphFrame

        # Make the PyOscope instance
        self.pyo = PyOscope(interactive=False)

        # Make the Binder
        self.binder = Binder(self.fMainFrame, self.fGraphFrame, self.pyo)

        # Make references to the app for all the objects
        self.fMainFrame.app = self
        self.fGraphFrame.app = self
        self.pyo.app = self
        self.binder.app = self

        # Bind the commands to the GUI
        self.binder.bind()

        return 1

if __name__ == '__main__':
    app = CPApp(0)
    app.MainLoop()
