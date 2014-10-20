import matplotlib
matplotlib.interactive(False)
matplotlib.use('WXAgg')

import wx

from mainframe import MainFrame
from graphframe import GraphFrame


class CPApp(wx.App):
    def __init__(self, controller):
        self.controller = controller
        wx.App.__init__(self)

    def OnInit(self):
        # Make the MainFrame
        print "CONSTRUCTING: MainFrame" #DELME
        fMainFrame = MainFrame(self.controller)
        fMainFrame.Show()
        self.SetTopWindow(fMainFrame)
        self.fMainFrame = fMainFrame

        # Make the GraphFrame
        print "CONSTRUCTING: GraphFrame" #DELME
        fGraphFrame = GraphFrame()
        fGraphFrame.Show()
        self.fGraphFrame = fGraphFrame

        self.fMainFrame.app = self
        self.fGraphFrame.app = self

        return 1


if __name__ == '__main__':
    app = CPApp(0)
    app.MainLoop()
